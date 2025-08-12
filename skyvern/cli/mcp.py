import json
import os
import shutil

from dotenv import load_dotenv
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from skyvern.config import settings
from skyvern.forge import app
from skyvern.forge.sdk.db.enums import OrganizationAuthTokenType
from skyvern.library import Skyvern
from skyvern.utils import detect_os, get_windows_appdata_roaming

from .console import console


async def setup_local_organization() -> str:
    skyvern_agent = Skyvern(base_url=settings.SKYVERN_BASE_URL, api_key=settings.SKYVERN_API_KEY)
    organization = await skyvern_agent.get_organization()
    org_auth_token = await app.DATABASE.get_valid_org_auth_token(
        organization_id=organization.organization_id,
        token_type=OrganizationAuthTokenType.api,
    )
    return org_auth_token.token if org_auth_token else ""


# ----- Helper paths and checks -----


def get_claude_config_path(host_system: str) -> str:
    if host_system == "darwin":
        return os.path.expanduser("~/Library/Application Support/Claude/claude_desktop_config.json")
    elif host_system == "windows":
        # Windows-specific path for Claude Desktop
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Claude" / "claude_desktop_config.json")
        else:
            # Fallback to user directory
            return os.path.expanduser("~\\AppData\\Roaming\\Claude\\claude_desktop_config.json")
    elif host_system == "wsl":
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Claude" / "claude_desktop_config.json")
        else:
            raise RuntimeError("Could not locate Windows AppData\\Roaming path from WSL")
    else:
        return os.path.expanduser("~/.config/claude/claude_desktop_config.json")


def get_cursor_config_path(host_system: str) -> str:
    if host_system == "darwin":
        return os.path.expanduser("~/Library/Application Support/Cursor/User/globalStorage/continue.continue/continue_config.json")
    elif host_system == "windows":
        # Windows-specific path for Cursor
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Cursor" / "User" / "globalStorage" / "continue.continue" / "continue_config.json")
        else:
            # Fallback to user directory
            return os.path.expanduser("~\\AppData\\Roaming\\Cursor\\User\\globalStorage\\continue.continue\\continue_config.json")
    elif host_system == "wsl":
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Cursor" / "User" / "globalStorage" / "continue.continue" / "continue_config.json")
        else:
            raise RuntimeError("Could not locate Windows AppData\\Roaming path from WSL")
    else:
        return os.path.expanduser("~/.config/Cursor/User/globalStorage/continue.continue/continue_config.json")


def get_windsurf_config_path(host_system: str) -> str:
    if host_system == "darwin":
        return os.path.expanduser("~/Library/Application Support/Windsurf/config.json")
    elif host_system == "windows":
        # Windows-specific path for Windsurf
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Windsurf" / "config.json")
        else:
            # Fallback to user directory
            return os.path.expanduser("~\\AppData\\Roaming\\Windsurf\\config.json")
    elif host_system == "wsl":
        roaming_path = get_windows_appdata_roaming()
        if roaming_path:
            return str(roaming_path / "Windsurf" / "config.json")
        else:
            raise RuntimeError("Could not locate Windows AppData\\Roaming path from WSL")
    else:
        return os.path.expanduser("~/.config/windsurf/config.json")


def setup_mcp_config() -> str:
    """Set up MCP configuration and return the path to the .env file."""
    load_dotenv()
    path_to_env = os.path.abspath(".env")
    
    if not os.path.exists(path_to_env):
        console.print("[red]No .env file found. Please run 'skyvern init' first.[/red]")
        raise typer.Exit(1)
    
    return path_to_env


def setup_claude_desktop_config(host_system: str, path_to_env: str) -> bool:
    """Set up Claude Desktop MCP configuration."""
    config_path = get_claude_config_path(host_system)
    
    if not os.path.exists(config_path):
        console.print(f"[yellow]Claude Desktop config not found at: {config_path}[/yellow]")
        console.print("[italic]Please install Claude Desktop first.[/italic]")
        return False
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        console.print(f"[red]Error reading Claude Desktop config at: {config_path}[/red]")
        return False
    
    # Load environment variables
    load_dotenv(path_to_env)
    skyvern_api_key = os.getenv("SKYVERN_API_KEY")
    skyvern_base_url = os.getenv("SKYVERN_BASE_URL", "http://localhost:8000")
    
    if not skyvern_api_key:
        console.print("[red]SKYVERN_API_KEY not found in .env file.[/red]")
        return False
    
    # Add Skyvern MCP server to Claude Desktop config
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["Skyvern"] = {
        "command": "skyvern",
        "args": ["run", "mcp"],
        "env": {
            "SKYVERN_API_KEY": skyvern_api_key,
            "SKYVERN_BASE_URL": skyvern_base_url,
        },
    }
    
    # Create backup
    backup_path = config_path + ".backup"
    shutil.copy2(config_path, backup_path)
    
    # Write updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    console.print(f"✅ [green]Claude Desktop MCP configuration updated at:[/green] [link]{config_path}[/link]")
    console.print(f"📋 [yellow]Backup created at:[/yellow] [link]{backup_path}[/link]")
    
    return True


def setup_cursor_config(host_system: str, path_to_env: str) -> bool:
    """Set up Cursor MCP configuration."""
    config_path = get_cursor_config_path(host_system)
    
    if not os.path.exists(config_path):
        console.print(f"[yellow]Cursor config not found at: {config_path}[/yellow]")
        console.print("[italic]Please install Cursor first.[/italic]")
        return False
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        console.print(f"[red]Error reading Cursor config at: {config_path}[/red]")
        return False
    
    # Load environment variables
    load_dotenv(path_to_env)
    skyvern_api_key = os.getenv("SKYVERN_API_KEY")
    skyvern_base_url = os.getenv("SKYVERN_BASE_URL", "http://localhost:8000")
    
    if not skyvern_api_key:
        console.print("[red]SKYVERN_API_KEY not found in .env file.[/red]")
        return False
    
    # Add Skyvern MCP server to Cursor config
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["Skyvern"] = {
        "command": "skyvern",
        "args": ["run", "mcp"],
        "env": {
            "SKYVERN_API_KEY": skyvern_api_key,
            "SKYVERN_BASE_URL": skyvern_base_url,
        },
    }
    
    # Create backup
    backup_path = config_path + ".backup"
    shutil.copy2(config_path, backup_path)
    
    # Write updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    console.print(f"✅ [green]Cursor MCP configuration updated at:[/green] [link]{config_path}[/link]")
    console.print(f"📋 [yellow]Backup created at:[/yellow] [link]{backup_path}[/link]")
    
    return True


def setup_windsurf_config(host_system: str, path_to_env: str) -> bool:
    """Set up Windsurf MCP configuration."""
    config_path = get_windsurf_config_path(host_system)
    
    if not os.path.exists(config_path):
        console.print(f"[yellow]Windsurf config not found at: {config_path}[/yellow]")
        console.print("[italic]Please install Windsurf first.[/italic]")
        return False
    
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        console.print(f"[red]Error reading Windsurf config at: {config_path}[/red]")
        return False
    
    # Load environment variables
    load_dotenv(path_to_env)
    skyvern_api_key = os.getenv("SKYVERN_API_KEY")
    skyvern_base_url = os.getenv("SKYVERN_BASE_URL", "http://localhost:8000")
    
    if not skyvern_api_key:
        console.print("[red]SKYVERN_API_KEY not found in .env file.[/red]")
        return False
    
    # Add Skyvern MCP server to Windsurf config
    if "mcpServers" not in config:
        config["mcpServers"] = {}
    
    config["mcpServers"]["Skyvern"] = {
        "command": "skyvern",
        "args": ["run", "mcp"],
        "env": {
            "SKYVERN_API_KEY": skyvern_api_key,
            "SKYVERN_BASE_URL": skyvern_base_url,
        },
    }
    
    # Create backup
    backup_path = config_path + ".backup"
    shutil.copy2(config_path, backup_path)
    
    # Write updated config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    console.print(f"✅ [green]Windsurf MCP configuration updated at:[/green] [link]{config_path}[/link]")
    console.print(f"📋 [yellow]Backup created at:[/yellow] [link]{backup_path}[/link]")
    
    return True


def setup_mcp() -> None:
    console.print(Panel("[bold green]MCP Server Setup[/bold green]", border_style="green"))
    host_system = detect_os()
    path_to_env = setup_mcp_config()

    if Confirm.ask("Would you like to set up MCP integration for Claude Desktop?", default=True):
        setup_claude_desktop_config(host_system, path_to_env)

    if Confirm.ask("Would you like to set up MCP integration for Cursor?", default=True):
        setup_cursor_config(host_system, path_to_env)

    if Confirm.ask("Would you like to set up MCP integration for Windsurf?", default=True):
        setup_windsurf_config(host_system, path_to_env)

    console.print("\n🎉 [bold green]MCP server configuration completed.[/bold green]")
    console.print("[bold]To use MCP with your AI applications:[/bold]")
    console.print("1. [green]Start the Skyvern MCP server:[/green] [code]skyvern run mcp[/code]")
    console.print("2. [green]Restart your AI application[/green]")
    console.print("3. [green]The Skyvern MCP server will be available as a tool[/green]")
