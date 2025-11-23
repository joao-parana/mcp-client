#!/usr/bin/env python3
"""Test script to verify multi-server configuration functionality.

This script tests the new server configuration loading and selection features.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp_client.config import ServerConfigLoader


def test_config_loading():
    """Test configuration file loading."""
    print("=" * 60)
    print("Testing Configuration Loading")
    print("=" * 60)

    try:
        loader = ServerConfigLoader()
        print("✓ Configuration file loaded successfully")
        print(f"  Location: {loader.config_path}")
        return loader
    except FileNotFoundError as e:
        print(f"✗ Configuration file not found: {e}")
        return None
    except Exception as e:
        print(f"✗ Error loading configuration: {e}")
        return None


def test_list_servers(loader):
    """Test listing available servers."""
    print("\n" + "=" * 60)
    print("Testing Server Listing")
    print("=" * 60)

    if loader is None:
        print("✗ Cannot test - loader not initialized")
        return False

    try:
        servers = loader.list_servers()
        print(f"✓ Found {len(servers)} configured servers:")
        for name in servers:
            print(f"  • {name}")
        return True
    except Exception as e:
        print(f"✗ Error listing servers: {e}")
        return False


def test_get_server(loader):
    """Test retrieving server configurations."""
    print("\n" + "=" * 60)
    print("Testing Server Retrieval")
    print("=" * 60)

    if loader is None:
        print("✗ Cannot test - loader not initialized")
        return False

    servers = loader.list_servers()
    if not servers:
        print("✗ No servers to test")
        return False

    # Test first server
    test_server = servers[0]
    try:
        config = loader.get_server(test_server)
        print(f"✓ Retrieved configuration for '{test_server}':")
        print(f"  Name: {config.name}")
        print(f"  Description: {config.description}")
        print(f"  Command: {config.command}")
        print(f"  Args: {' '.join(config.args[:3])}...")
        print(f"  Transport: {config.transport}")
        print(f"  Docker Image: {config.docker.get('image', 'N/A')}")
        return True
    except Exception as e:
        print(f"✗ Error retrieving server '{test_server}': {e}")
        return False


def test_invalid_server(loader):
    """Test error handling for invalid server names."""
    print("\n" + "=" * 60)
    print("Testing Invalid Server Handling")
    print("=" * 60)

    if loader is None:
        print("✗ Cannot test - loader not initialized")
        return False

    try:
        loader.get_server("nonexistent-server")
        print("✗ Should have raised KeyError for invalid server")
        return False
    except KeyError as e:
        print(f"✓ Correctly raised KeyError: {e}")
        return True
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


def test_server_details(loader):
    """Test detailed server configuration access."""
    print("\n" + "=" * 60)
    print("Testing Server Details")
    print("=" * 60)

    if loader is None:
        print("✗ Cannot test - loader not initialized")
        return False

    servers = loader.list_servers()
    if not servers:
        print("✗ No servers to test")
        return False

    success_count = 0
    for server_name in servers:
        try:
            config = loader.get_server(server_name)

            # Verify required fields
            assert config.name == server_name
            assert isinstance(config.command, str)
            assert isinstance(config.args, list)
            assert isinstance(config.docker, dict)

            # Check if Docker image is specified
            if config.command == "docker":
                assert "image" in config.docker
                print(
                    f"✓ {server_name}: "
                    f"Docker image = {config.docker['image']}"
                )
            else:
                print(f"✓ {server_name}: Non-Docker server")

            success_count += 1
        except AssertionError as e:
            print(f"✗ {server_name}: Invalid configuration - {e}")
        except Exception as e:
            print(f"✗ {server_name}: Error - {e}")

    print(f"\nValidated {success_count}/{len(servers)} servers")
    return success_count == len(servers)


def test_table_printing(loader):
    """Test formatted table printing."""
    print("\n" + "=" * 60)
    print("Testing Table Printing")
    print("=" * 60)

    if loader is None:
        print("✗ Cannot test - loader not initialized")
        return False

    try:
        loader.print_servers_table()
        print("\n✓ Table printed successfully")
        return True
    except Exception as e:
        print(f"✗ Error printing table: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MCP Client Multi-Server Configuration Tests")
    print("=" * 60)
    print()

    tests = [
        ("Configuration Loading", test_config_loading),
    ]

    results = {}
    loader = None

    # Run initial test
    loader = tests[0][1]()
    results[tests[0][0]] = loader is not None

    if loader is not None:
        # Run remaining tests
        tests.extend(
            [
                ("Server Listing", lambda: test_list_servers(loader)),
                ("Server Retrieval", lambda: test_get_server(loader)),
                (
                    "Invalid Server Handling",
                    lambda: test_invalid_server(loader),
                ),
                ("Server Details", lambda: test_server_details(loader)),
                ("Table Printing", lambda: test_table_printing(loader)),
            ]
        )

        for name, test_func in tests[1:]:
            results[name] = test_func()

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    print("-" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
