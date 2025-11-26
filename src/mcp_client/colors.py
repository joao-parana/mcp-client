"""Color utilities for terminal output.

This module provides color formatting for terminal output using colorama.
"""

from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)


class Colors:
    """ANSI color codes for terminal output."""

    # User input colors
    USER = Fore.YELLOW
    USER_BOLD = Fore.YELLOW + Style.BRIGHT

    # Assistant response colors
    ASSISTANT = Fore.GREEN
    ASSISTANT_BOLD = Fore.GREEN + Style.BRIGHT

    # Tool/action colors
    TOOL = Fore.CYAN
    TOOL_BOLD = Fore.CYAN + Style.BRIGHT

    # Error colors
    ERROR = Fore.RED
    ERROR_BOLD = Fore.RED + Style.BRIGHT

    # Info colors
    INFO = Fore.BLUE
    INFO_BOLD = Fore.BLUE + Style.BRIGHT

    # Warning colors
    WARNING = Fore.MAGENTA
    WARNING_BOLD = Fore.MAGENTA + Style.BRIGHT

    # Reset
    RESET = Style.RESET_ALL


def colorize(text: str, color: str) -> str:
    """Apply color to text.

    Args:
        text: Text to colorize
        color: Color code from Colors class

    Returns:
        Colored text string
    """
    return f"{color}{text}{Colors.RESET}"


def user_prompt(text: str = "You: ") -> str:
    """Format user prompt with yellow color.

    Args:
        text: Prompt text (default: "You: ")

    Returns:
        Colored prompt string
    """
    return colorize(text, Colors.USER_BOLD)


def assistant_prefix(text: str = "Assistant: ") -> str:
    """Format assistant prefix with green color.

    Args:
        text: Prefix text (default: "Assistant: ")

    Returns:
        Colored prefix string
    """
    return colorize(text, Colors.ASSISTANT_BOLD)


def tool_message(text: str) -> str:
    """Format tool/action message with cyan color.

    Args:
        text: Tool message text

    Returns:
        Colored message string
    """
    return colorize(text, Colors.TOOL)


def error_message(text: str) -> str:
    """Format error message with red color.

    Args:
        text: Error message text

    Returns:
        Colored message string
    """
    return colorize(text, Colors.ERROR_BOLD)


def info_message(text: str) -> str:
    """Format info message with blue color.

    Args:
        text: Info message text

    Returns:
        Colored message string
    """
    return colorize(text, Colors.INFO)


def warning_message(text: str) -> str:
    """Format warning message with magenta color.

    Args:
        text: Warning message text

    Returns:
        Colored message string
    """
    return colorize(text, Colors.WARNING)


def print_user(text: str) -> None:
    """Print user message with yellow color.

    Args:
        text: Message text
    """
    print(colorize(text, Colors.USER))


def print_assistant(text: str) -> None:
    """Print assistant message with green color.

    Args:
        text: Message text
    """
    print(colorize(text, Colors.ASSISTANT))


def print_tool(text: str) -> None:
    """Print tool message with cyan color.

    Args:
        text: Message text
    """
    print(colorize(text, Colors.TOOL))


def print_error(text: str) -> None:
    """Print error message with red color.

    Args:
        text: Error message text
    """
    print(colorize(text, Colors.ERROR_BOLD))


def print_info(text: str) -> None:
    """Print info message with blue color.

    Args:
        text: Info message text
    """
    print(colorize(text, Colors.INFO))


def print_warning(text: str) -> None:
    """Print warning message with magenta color.

    Args:
        text: Warning message text
    """
    print(colorize(text, Colors.WARNING))
