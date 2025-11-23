import argparse
import pathlib


def parse_args():
    """Parse command line arguments and return parsed args."""
    parser = argparse.ArgumentParser(
        description="A minimal MCP client with OpenAI and Ollama support"
    )

    # Server selection - mutually exclusive
    server_group = parser.add_mutually_exclusive_group()
    server_group.add_argument(
        "server_path",
        type=pathlib.Path,
        nargs="?",
        help="path to the MCP server script (legacy mode)",
    )
    server_group.add_argument(
        "--server",
        "-s",
        type=str,
        help="name of configured MCP server from conf/mcp-servers.json",
    )
    server_group.add_argument(
        "--list-servers",
        action="store_true",
        help="list all configured MCP servers and exit",
    )

    # Action group
    action_group = parser.add_mutually_exclusive_group()
    action_group.add_argument(
        "--members",
        action="store_true",
        help="list the MCP server's tools, prompts, and resources",
    )
    action_group.add_argument(
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

    # Docker-specific options
    parser.add_argument(
        "--docker-verbose",
        action="store_true",
        help="show verbose Docker output (for debugging)",
    )

    args = parser.parse_args()

    # Validation: if not listing servers, need either server_path or --server
    if not args.list_servers:
        if not args.server_path and not args.server:
            parser.error(
                "either server_path or --server must be specified "
                "(or use --list-servers)"
            )
        # Also need an action
        if not args.members and not args.chat:
            parser.error(
                "one of --members or --chat is required "
                "(unless using --list-servers)"
            )

    return args
