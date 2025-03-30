from dotenv import load_dotenv
import argparse
import asyncio
import logging
import os
import sys
from typing import List, Optional

from .server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    style="{"
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
# Get the directory of the current file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)
logger.info(f"Loaded environment variables from {dotenv_path}")


def main():
    """Entry point for the SSH execution MCP server"""
    import uvicorn

    # Parse command line arguments
    parser = argparse.ArgumentParser(description="SSH execution MCP server")

    # Server configuration
    parser.add_argument(
        "--host", "-H",
        type=str,
        default="127.0.0.1",
        help="Host to bind the server to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", "-P",
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)"
    )
    parser.add_argument(
        "--reload", "-r",
        action="store_true",
        help="Enable auto-reload for development"
    )

    # SSH connection configuration
    parser.add_argument(
        "--ssh-host", "-sh",
        type=str,
        help="SSH host to connect to (overrides SSH_HOST environment variable)"
    )
    parser.add_argument(
        "--ssh-port", "-sp",
        type=int,
        help="SSH port to connect to (overrides SSH_PORT environment variable)"
    )
    parser.add_argument(
        "--ssh-username", "-su",
        type=str,
        help="SSH username (overrides SSH_USERNAME environment variable)"
    )

    # Security configuration arguments
    parser.add_argument(
        "--allowed-commands", "-ac",
        type=str,
        help="Comma-separated list of commands that are allowed to be executed"
    )
    parser.add_argument(
        "--allowed-paths", "-ap",
        type=str,
        help="Comma-separated list of paths that are allowed for command execution"
    )
    parser.add_argument(
        "--commands-blacklist", "-cb",
        type=str,
        default="rm,mv,dd,mkfs,fdisk,format",
        help="Comma-separated list of commands that are not allowed (default: rm,mv,dd,mkfs,fdisk,format)"
    )
    parser.add_argument(
        "--arguments-blacklist", "-ab",
        type=str,
        default="-rf,-fr,--force",
        help="Comma-separated list of arguments that are not allowed (default: -rf,-fr,--force)"
    )

    args = parser.parse_args()

    # Set environment variables from command-line arguments if provided
    if args.ssh_host:
        os.environ["SSH_HOST"] = args.ssh_host

    if args.ssh_port:
        os.environ["SSH_PORT"] = str(args.ssh_port)

    if args.ssh_username:
        os.environ["SSH_USERNAME"] = args.ssh_username

    if args.allowed_commands:
        os.environ["SSH_ALLOWED_COMMANDS"] = args.allowed_commands

    if args.allowed_paths:
        os.environ["SSH_ALLOWED_PATHS"] = args.allowed_paths

    if args.commands_blacklist:
        os.environ["SSH_COMMANDS_BLACKLIST"] = args.commands_blacklist

    if args.arguments_blacklist:
        os.environ["SSH_ARGUMENTS_BLACKLIST"] = args.arguments_blacklist

    # Log server startup
    logger.info("Starting SSH execution MCP server on {host}:{port}",
                host=args.host, port=args.port)

    # Use get() to safely access environment variables that might not be set
    ssh_host = os.environ.get('SSH_HOST', 'Not set')
    ssh_port = os.environ.get('SSH_PORT', 'Not set')
    ssh_username = os.environ.get('SSH_USERNAME', 'Not set')
    allowed_commands = os.environ.get('SSH_ALLOWED_COMMANDS', '')
    allowed_paths = os.environ.get('SSH_ALLOWED_PATHS', '')
    commands_blacklist = os.environ.get('SSH_COMMANDS_BLACKLIST', '')
    arguments_blacklist = os.environ.get('SSH_ARGUMENTS_BLACKLIST', '')

    logger.info("SSH connection details: {ssh_host}:{ssh_port}",
                ssh_host=ssh_host, ssh_port=ssh_port)
    logger.info("SSH username: {ssh_username}", ssh_username=ssh_username)
    logger.info("Allowed commands: {allowed_commands}",
                allowed_commands=allowed_commands)
    logger.info("Allowed paths: {allowed_paths}", allowed_paths=allowed_paths)
    logger.info("Commands blacklist: {commands_blacklist}",
                commands_blacklist=commands_blacklist)
    logger.info("Arguments blacklist: {arguments_blacklist}",
                arguments_blacklist=arguments_blacklist)

    # Start the FastMCP server using Uvicorn
    uvicorn.run(
        "mcp_ssh_exec.ssh_exec:mcp",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
