import asyncio
import sys

from mcp_client.cli import parse_args
from mcp_client.config import ServerConfigLoader
from mcp_client.mcp_client import MCPClient


async def main() -> None:
    """Run the MCP client with the specified options."""
    args = parse_args()

    # Handle --list-servers
    if args.list_servers:
        try:
            loader = ServerConfigLoader()
            loader.print_servers_table()
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print(
                "\nNo configuration file found. "
                "Expected: conf/mcp-servers.json"
            )
            sys.exit(1)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            sys.exit(1)
        return

    # Load server configuration if using --server
    config = None
    server_path = None

    if args.server:
        try:
            loader = ServerConfigLoader()
            config = loader.get_server(args.server)
            print(f"Using configured server: {args.server}")
            print(f"Description: {config.description}")
        except FileNotFoundError as e:
            print(f"Error: {e}")
            print(
                "\nConfiguration file not found. "
                "Expected: conf/mcp-servers.json"
            )
            sys.exit(1)
        except KeyError as e:
            print(f"Error: {e}")
            print("\nUse --list-servers to see available servers")
            sys.exit(1)
        except Exception as e:
            print(f"Error loading server configuration: {e}")
            sys.exit(1)
    else:
        # Legacy mode: direct server path
        server_path = str(args.server_path)
        if not args.server_path.exists():
            print(
                f"Error: Server script '{args.server_path}' not found"
            )
            sys.exit(1)

    # Create and run client
    try:
        async with MCPClient(
            server_path=server_path,
            provider=args.provider,
            model=args.model,
            config=config,
            verbose=args.docker_verbose,
        ) as client:
            if args.members:
                await client.list_all_members()
            elif args.chat:
                await client.run_chat()
    except RuntimeError as e:
        print(e)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)


def cli_main():
    """Entry point for the mcp-client CLI app."""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
