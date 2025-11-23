import sys
from contextlib import AsyncExitStack
from typing import Any, Awaitable, Callable, ClassVar, Self

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mcp_client import chat
from mcp_client.config import ServerConfig
from mcp_client.handlers import create_query_handler


class MCPClient:
    """MCP client to interact with MCP server.

    Supports both direct Python script servers and Docker-based servers.

    Usage:
        async with MCPClient(server_path) as client:
            # Call client methods here...

        # Or with server config:
        async with MCPClient(config=server_config) as client:
            # Call client methods here...
    """

    client_session: ClassVar[ClientSession]

    def __init__(
        self,
        server_path: str | None = None,
        provider: str | None = None,
        model: str | None = None,
        config: ServerConfig | None = None,
        verbose: bool = False,
    ):
        """Initialize MCP client.

        Args:
            server_path: Path to Python MCP server script (legacy mode)
            provider: LLM provider (openai or ollama)
            model: Model name to use
            config: ServerConfig object for Docker-based servers
            verbose: Show verbose output
        """
        if server_path is None and config is None:
            raise ValueError(
                "Either server_path or config must be provided"
            )

        self.server_path = server_path
        self.config = config
        self.provider = provider
        self.model = model
        self.verbose = verbose
        self.exit_stack = AsyncExitStack()

    async def __aenter__(self) -> Self:
        cls = type(self)
        cls.client_session = await self._connect_to_server()
        return self

    async def __aexit__(self, *_) -> None:
        await self.exit_stack.aclose()

    def _build_server_params(self) -> StdioServerParameters:
        """Build server parameters based on configuration."""
        if self.config:
            # Docker-based server
            command = self.config.command
            args = self.config.args.copy()

            # Add verbose flag if requested
            if self.verbose and command == "docker":
                # Docker doesn't have a verbose flag, but we can log
                print(f"Starting Docker container: {' '.join(args)}")

            return StdioServerParameters(
                command=command,
                args=args,
                env=self.config.env if self.config.env else None,
            )
        else:
            # Legacy Python script server
            return StdioServerParameters(
                command="sh",
                args=[
                    "-c",
                    f"{sys.executable} {self.server_path} 2>/dev/null",
                ],
                env=None,
            )

    async def _connect_to_server(self) -> ClientSession:
        """Connect to MCP server via stdio."""
        try:
            server_params = self._build_server_params()

            if self.verbose:
                server_name = (
                    self.config.name if self.config else self.server_path
                )
                print(f"Connecting to server: {server_name}")
                print(
                    f"Command: {server_params.command} "
                    f"{' '.join(server_params.args)}"
                )

            read, write = await self.exit_stack.enter_async_context(
                stdio_client(server=server_params)
            )
            client_session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await client_session.initialize()

            if self.verbose:
                print("✓ Connected successfully")

            return client_session
        except Exception as e:
            error_msg = f"Error: Failed to connect to server: {e}"
            if self.config and self.config.command == "docker":
                error_msg += (
                    f"\n\nDocker troubleshooting:\n"
                    f"1. Ensure Docker is running: docker info\n"
                    f"2. Check if image exists: docker images | grep {self.config.docker.get('image', 'mcp')}\n"
                    f"3. Pull image if needed: docker pull {self.config.docker.get('image', 'mcp/unknown')}\n"
                )
            raise RuntimeError(error_msg) from e

    async def list_all_members(self) -> None:
        """List all available tools, prompts, and resources."""
        if self.config:
            print(f"MCP Server: {self.config.name}")
            print(f"Description: {self.config.description}")
            print("=" * 50)
        else:
            print("MCP Server Members")
            print("=" * 50)

        sections = {
            "tools": self.client_session.list_tools,
            "prompts": self.client_session.list_prompts,
            "resources": self.client_session.list_resources,
        }
        for section, listing_method in sections.items():
            await self._list_section(section, listing_method)

        print("\n" + "=" * 50)

    async def _list_section(
        self,
        section: str,
        list_method: Callable[[], Awaitable[Any]],
    ) -> None:
        try:
            items = getattr(await list_method(), section)
            if items:
                print(f"\n{section.upper()} ({len(items)}):")
                print("-" * 30)
                for item in items:
                    description = item.description or "No description"
                    print(f" > {item.name} - {description}")
            else:
                print(f"\n{section.upper()}: None available")
        except Exception as e:
            print(f"\n{section.upper()}: Error - {e}")

    async def run_chat(self) -> None:
        """Start interactive chat with MCP server using configured LLM."""
        try:
            handler = create_query_handler(
                self.client_session,
                provider=self.provider,
                model=self.model,
            )
            provider_name = type(handler).__name__.replace(
                "QueryHandler", ""
            )
            model_name = getattr(handler, "model", "unknown")

            if self.config:
                print(f"\nServer: {self.config.name}")
                print(f"Description: {self.config.description}")
            print(f"LLM: {provider_name} with model: {model_name}")

            await chat.run_chat(handler)
        except RuntimeError as e:
            print(e)
