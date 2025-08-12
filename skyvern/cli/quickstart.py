"""Quickstart command for Skyvern CLI."""

import asyncio
import subprocess

import typer
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Import console after skyvern.cli to ensure proper initialization
from skyvern.cli.console import console
from skyvern.cli.init_command import init  # init is used directly
from skyvern.cli.utils import start_services
from skyvern.utils import detect_os

quickstart_app = typer.Typer(help="Quickstart command to set up and run Skyvern with one command.")


def check_docker() -> bool:
    """Check if Docker is installed and running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


def install_playwright_browser() -> bool:
    """Install Playwright browser with Windows-specific handling."""
    host_system = detect_os()
    
    try:
        if host_system == "windows":
            # Windows-specific Playwright installation
            console.print("[bold blue]Installing Chromium browser for Windows...[/bold blue]")
            result = subprocess.run(
                ["playwright", "install", "chromium"],
                capture_output=True,
                text=True,
                shell=True,  # Use shell on Windows for better compatibility
            )
        else:
            # Unix-like systems
            result = subprocess.run(
                ["playwright", "install", "chromium"],
                capture_output=True,
                text=True,
            )
        
        if result.returncode == 0:
            console.print("✅ [green]Chromium installation complete.[/green]")
            return True
        else:
            console.print(f"[yellow]Warning: Failed to install Chromium: {result.stderr}[/yellow]")
            return False
    except subprocess.CalledProcessError as e:
        console.print(f"[yellow]Warning: Failed to install Chromium: {e.stderr}[/yellow]")
        return False
    except FileNotFoundError:
        console.print("[yellow]Warning: Playwright not found. Please install it first.[/yellow]")
        return False


@quickstart_app.callback(invoke_without_command=True)
def quickstart(
    ctx: typer.Context,
    no_postgres: bool = typer.Option(False, "--no-postgres", help="Skip starting PostgreSQL container"),
    skip_browser_install: bool = typer.Option(
        False, "--skip-browser-install", help="Skip Chromium browser installation"
    ),
    server_only: bool = typer.Option(False, "--server-only", help="Only start the server, not the UI"),
) -> None:
    
    # Check Docker
    with console.status("Checking Docker installation...") as status:
        if not check_docker():
            console.print(
                Panel(
                    "[bold red]Docker is not installed or not running.[/bold red]\n"
                    "Please install Docker and start it before running quickstart.\n"
                    "Get Docker from: [link]https://www.docker.com/get-started[/link]",
                    border_style="red",
                )
            )
            raise typer.Exit(1)
        status.update("✅ Docker is installed and running")

    # Run initialization
    console.print(Panel("[bold green]🚀 Starting Skyvern Quickstart[/bold green]", border_style="green"))

    try:
        # Initialize Skyvern
        console.print("\n[bold blue]Initializing Skyvern...[/bold blue]")
        init(no_postgres=no_postgres)

        # Skip browser installation if requested
        if not skip_browser_install:
            with Progress(
                SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True, console=console
            ) as progress:
                progress.add_task("[bold blue]Installing Chromium browser...", total=None)
                install_playwright_browser()
        else:
            console.print("⏭️ [yellow]Skipping Chromium installation as requested.[/yellow]")

        # Start services
        console.print("\n[bold blue]Starting Skyvern services...[/bold blue]")
        asyncio.run(start_services(server_only=server_only))

    except KeyboardInterrupt:
        console.print("\n[bold yellow]Quickstart process interrupted by user.[/bold yellow]")
        raise typer.Exit(0)
    except Exception as e:
        console.print(f"[bold red]Error during quickstart: {str(e)}[/bold red]")
        raise typer.Exit(1)
