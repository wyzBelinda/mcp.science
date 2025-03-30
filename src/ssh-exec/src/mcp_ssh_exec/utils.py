import os
import re
from typing import List, Optional


def validate_command(
    command: str,
    allowed_commands: List[str],
    allowed_paths: List[str],
    commands_blacklist: List[str],
    arguments_blacklist: List[str]
) -> Optional[str]:
    """Validate if a command is allowed to be executed

    Args:
        command: Command to validate
        allowed_commands: List of allowed commands
        allowed_paths: List of allowed paths
        commands_blacklist: List of blacklisted commands
        arguments_blacklist: List of blacklisted arguments

    Returns:
        None if the command is valid, otherwise an error message
    """
    # Strip the command of any leading/trailing whitespace
    command = command.strip()

    # Check if the command is empty
    if not command:
        return "Command cannot be empty"

    # Split the command into parts (command and arguments)
    parts = command.split()
    base_command = parts[0]

    # Check if the command is in the blacklist
    for blacklisted_cmd in commands_blacklist:
        if base_command == blacklisted_cmd or base_command.endswith(f"/{blacklisted_cmd}"):
            return f"Command '{base_command}' is blacklisted"

    # Check for blacklisted arguments
    for arg in parts[1:]:
        for blacklisted_arg in arguments_blacklist:
            if arg == blacklisted_arg:
                return f"Argument '{arg}' is blacklisted"

    # If allowed_commands is provided, check if the command is in the list
    if allowed_commands:
        is_allowed = False
        for allowed_cmd in allowed_commands:
            if command.startswith(allowed_cmd):
                is_allowed = True
                break

        if not is_allowed:
            return f"Command '{command}' is not in the allowed commands list"

    # If allowed_paths is provided, check if the command operates on allowed paths
    if allowed_paths and any(path_arg for path_arg in parts[1:] if not path_arg.startswith("-")):
        # Extract potential path arguments (those not starting with -)
        potential_paths = [arg for arg in parts[1:] if not arg.startswith("-")]

        for path_arg in potential_paths:
            path_allowed = False

            # Check if the path is within any of the allowed paths
            for allowed_path in allowed_paths:
                if path_arg.startswith(allowed_path) or os.path.abspath(path_arg).startswith(allowed_path):
                    path_allowed = True
                    break

            if not path_allowed:
                return f"Path '{path_arg}' is not in the allowed paths list"

    return None
