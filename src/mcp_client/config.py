"""Configuration module for MCP servers.

This module handles loading and managing MCP server configurations
from the conf/mcp-servers.json file.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ServerConfig:
    """Configuration for a single MCP server."""

    name: str
    description: str
    command: str
    args: list[str]
    transport: str
    env: dict[str, str]
    docker: dict[str, Any]
    capabilities: dict[str, Any]
    mounted_directories: list[dict[str, str]] | None = None
    options: dict[str, Any] | None = None


class ServerConfigLoader:
    """Loads and manages MCP server configurations."""

    def __init__(self, config_path: Path | None = None):
        """Initialize the config loader.

        Args:
            config_path: Path to mcp-servers.json. If None, uses default location.
        """
        if config_path is None:
            # Try to find config in project root
            current = Path(__file__).parent
            project_root = current.parent.parent
            config_path = project_root / "conf" / "mcp-servers.json"

        self.config_path = config_path
        self._servers: dict[str, ServerConfig] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load server configurations from JSON file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}"
            )

        try:
            with open(self.config_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON in {self.config_path}: {e}"
            ) from e

        servers_data = data.get("mcpServers", {})
        for name, config in servers_data.items():
            self._servers[name] = ServerConfig(
                name=name,
                description=config.get("description", ""),
                command=config.get("command", ""),
                args=config.get("args", []),
                transport=config.get("transport", "stdio"),
                env=config.get("env", {}),
                docker=config.get("docker", {}),
                capabilities=config.get("capabilities", {}),
                mounted_directories=config.get("mounted_directories"),
                options=config.get("options"),
            )

    def list_servers(self) -> list[str]:
        """Return list of available server names."""
        return sorted(self._servers.keys())

    def get_server(self, name: str) -> ServerConfig:
        """Get configuration for a specific server.

        Args:
            name: Server name

        Returns:
            ServerConfig object

        Raises:
            KeyError: If server name not found
        """
        if name not in self._servers:
            available = ", ".join(self.list_servers())
            raise KeyError(
                f"Server '{name}' not found. Available: {available}"
            )
        return self._servers[name]

    def get_all_servers(self) -> dict[str, ServerConfig]:
        """Return all server configurations."""
        return self._servers.copy()

    def print_servers_table(self) -> None:
        """Print a formatted table of available servers."""
        if not self._servers:
            print("No servers configured")
            return

        print("\n" + "=" * 80)
        print("Available MCP Servers")
        print("=" * 80)

        # Header
        print(f"{'Name':<15} {'Image':<20} {'Description':<45}")
        print("-" * 80)

        # Servers
        for name, config in sorted(self._servers.items()):
            image = config.docker.get("image", "N/A")
            desc = config.description[:42] + "..." if len(
                config.description
            ) > 45 else config.description
            print(f"{name:<15} {image:<20} {desc:<45}")

        print("=" * 80)
        print(
            f"\nTotal servers configured: {len(self._servers)}"
        )
        print(
            "\nUsage: python3 -m mcp_client --server <name> --chat"
        )
        print("       python3 -m mcp_client --server <name> --members")
        print("\n")
