import argparse
import pathlib


def parse_args():
    """Parse command line arguments and return parsed args."""
    parser = argparse.ArgumentParser(
        description="A minimal MCP client with OpenAI and Ollama support"
    )
    parser.add_argument(
        "server_path",
        type=pathlib.Path,
        help="path to the MCP server script",
    )

    # Action group
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--members",
        action="store_true",
        help="list the MCP server's tools, prompts, and resources",
    )
    group.add_argument(
        "--chat",
        action="store_true",
        help="start an AI-powered chat with MCP server integration",
    )

    # LLM configuration
    parser.add_argument(
        "--provider",
        choices=["openai", "ollama"],
        help="LLM provider to use (auto-detected if not specified)",
    )
    parser.add_argument(
        "--model",
        help=(
            "Model name to use. "
            "For OpenAI: gpt-4o-mini (default), gpt-4o, etc. "
            "For Ollama: qwen2.5:7b (default), llama3.2:3b, phi4:14b, etc."
        ),
    )

    return parser.parse_args()
