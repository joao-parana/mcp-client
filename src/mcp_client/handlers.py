"""Query handlers for different LLM providers."""

import json
import os
from abc import ABC, abstractmethod
from typing import Any

from mcp import ClientSession
from openai import OpenAI

MAX_TOKENS = 1000


class BaseQueryHandler(ABC):
    """Abstract base class for query handlers."""

    def __init__(self, client_session: ClientSession):
        self.client_session = client_session

    @abstractmethod
    async def process_query(self, query: str) -> str:
        """Process a query using the LLM and available MCP tools."""
        pass

    async def _get_tools(self) -> list[dict[str, Any]]:
        """Get MCP tools formatted for OpenAI-compatible APIs."""
        response = await self.client_session.list_tools()
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description or "No description",
                    "parameters": getattr(
                        tool,
                        "inputSchema",
                        {"type": "object", "properties": {}},
                    ),
                },
            }
            for tool in response.tools
        ]

    async def _execute_tool(self, tool_call) -> dict[str, Any]:
        """Execute an MCP tool call and return formatted result."""
        tool_name = tool_call.function.name
        tool_args = json.loads(tool_call.function.arguments or "{}")

        try:
            result = await self.client_session.call_tool(
                tool_name,
                tool_args,
            )
            content = result.content[0].text if result.content else ""
            log = f"[Used {tool_name}({tool_args})]"
        except Exception as e:
            content = f"Error: {e}"
            log = f"[{content}]"

        return {
            "log": log,
            "message": {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": content,
            },
        }


class OpenAIQueryHandler(BaseQueryHandler):
    """Handle OpenAI API interaction and MCP tool execution."""

    def __init__(
        self,
        client_session: ClientSession,
        model: str = "gpt-4o-mini",
    ):
        super().__init__(client_session)
        if not (api_key := os.getenv("OPENAI_API_KEY")):
            raise RuntimeError(
                "Error: OPENAI_API_KEY environment variable not set",
            )
        self.openai = OpenAI(api_key=api_key)
        self.model = model

    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available MCP tools."""
        messages = [{"role": "user", "content": query}]
        initial_response = self.openai.chat.completions.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            messages=messages,
            tools=await self._get_tools(),
        )

        current_message = initial_response.choices[0].message
        result_parts = []

        if current_message.content:
            result_parts.append(current_message.content)

        if tool_calls := current_message.tool_calls:
            messages.append(
                {
                    "role": "assistant",
                    "content": current_message.content or "",
                    "tool_calls": tool_calls,
                }
            )

            for tool_call in tool_calls:
                tool_result = await self._execute_tool(tool_call)
                result_parts.append(tool_result["log"])
                messages.append(tool_result["message"])

            final_response = self.openai.chat.completions.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                messages=messages,
            )

            if content := final_response.choices[0].message.content:
                result_parts.append(content)

        return "Assistant: " + "\n".join(result_parts)


class OllamaQueryHandler(BaseQueryHandler):
    """Handle Ollama local API interaction and MCP tool execution."""

    def __init__(
        self,
        client_session: ClientSession,
        model: str = "qwen2.5:7b",
        base_url: str = "http://localhost:11434",
    ):
        super().__init__(client_session)
        try:
            from ollama import Client
        except ImportError as exc:
            raise RuntimeError(
                "Error: ollama package not installed. "
                "Install with: pip install ollama"
            ) from exc

        self.ollama = Client(host=base_url)
        self.model = model
        self._verify_model()

    def _verify_model(self) -> None:
        """Verify that the specified model is available in Ollama."""
        try:
            models = self.ollama.list()
            available_models = [m["name"] for m in models.get("models", [])]
            if not any(
                self.model in m or m.startswith(self.model)
                for m in available_models
            ):
                print(
                    f"Warning: Model '{self.model}' not found locally. "
                    f"Ollama will attempt to pull it on first use."
                )
                print(f"Available models: {', '.join(available_models)}")
        except Exception as e:
            print(f"Warning: Could not verify Ollama models: {e}")

    async def process_query(self, query: str) -> str:
        """Process a query using Ollama and available MCP tools."""
        messages = [{"role": "user", "content": query}]
        tools = await self._get_tools()

        # Ollama's chat API with tools support
        initial_response = self.ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools,
            options={"num_predict": MAX_TOKENS},
        )

        current_message = initial_response["message"]
        result_parts = []

        if content := current_message.get("content"):
            result_parts.append(content)

        # Handle tool calls if present
        if tool_calls := current_message.get("tool_calls"):
            messages.append(current_message)

            for tool_call in tool_calls:
                tool_result = await self._execute_tool_ollama(tool_call)
                result_parts.append(tool_result["log"])
                messages.append(tool_result["message"])

            # Get final response after tool execution
            final_response = self.ollama.chat(
                model=self.model,
                messages=messages,
                options={"num_predict": MAX_TOKENS},
            )

            if content := final_response["message"].get("content"):
                result_parts.append(content)

        return "Assistant: " + "\n".join(result_parts)

    async def _execute_tool_ollama(
        self, tool_call: dict[str, Any]
    ) -> dict[str, Any]:
        """Execute an MCP tool call for Ollama format."""
        function = tool_call["function"]
        tool_name = function["name"]
        tool_args = function["arguments"]

        try:
            result = await self.client_session.call_tool(
                tool_name,
                tool_args,
            )
            content = result.content[0].text if result.content else ""
            log = f"[Used {tool_name}({tool_args})]"
        except Exception as e:
            content = f"Error: {e}"
            log = f"[{content}]"

        return {
            "log": log,
            "message": {
                "role": "tool",
                "content": content,
            },
        }


def create_query_handler(
    client_session: ClientSession,
    provider: str | None = None,
    model: str | None = None,
) -> BaseQueryHandler:
    """Factory function to create the appropriate query handler.

    Args:
        client_session: MCP client session
        provider: 'openai' or 'ollama'. If None, auto-detect based on env vars
        model: Model name to use. If None, use defaults

    Returns:
        Appropriate query handler instance

    Raises:
        RuntimeError: If no valid provider configuration is found
    """
    # Auto-detect provider if not specified
    if provider is None:
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
        else:
            provider = "ollama"

    if provider == "openai":
        model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return OpenAIQueryHandler(client_session, model=model)
    elif provider == "ollama":
        # Recommended models for MacBook M3
        default_model = "qwen2.5:7b"  # Best balance for M3
        model = model or os.getenv("OLLAMA_MODEL", default_model)
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return OllamaQueryHandler(
            client_session, model=model, base_url=base_url
        )
    else:
        raise RuntimeError(
            f"Error: Unknown provider '{provider}'. "
            "Valid options: 'openai', 'ollama'"
        )
