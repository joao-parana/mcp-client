"""Chat interface for MCP client."""

from mcp_client.colors import error_message, user_prompt


async def run_chat(handler) -> None:
    """Run an AI-handled chat session with colored prompts."""
    print("\nMCP Client's Chat Started!")
    print("Type your queries or 'quit' to exit.")

    while True:
        try:
            # Show colored user prompt
            query = input(f"\n{user_prompt()}").strip()

            if not query:
                continue

            if query.lower() == "quit":
                break

            # Process query and print response (handler formats the output)
            print("\n" + await handler.process_query(query))

        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            break
        except Exception as e:
            print(f"\n{error_message(f'Error: {str(e)}')}")

    print("\nGoodbye!")
