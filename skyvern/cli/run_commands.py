import asyncio
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any, List

import psutil
import typer
import uvicorn
from dotenv import load_dotenv, set_key
from mcp.server.fastmcp import FastMCP
from rich.panel import Panel
from rich.prompt import Confirm

from skyvern.cli.utils import start_services
from skyvern.config import settings
from skyvern.library.skyvern import Skyvern
from skyvern.utils import detect_os

from .console import console

run_app = typer.Typer(help="Commands to run Skyvern services such as the API server or UI.")

mcp = FastMCP("Skyvern")


@mcp.tool()
async def skyvern_run_task(prompt: str, url: str) -> dict[str, Any]:
    """Use Skyvern to execute anything in the browser. Useful for accomplishing tasks that require browser automation.

    This tool uses Skyvern's browser automation to navigate websites and perform actions to achieve
    the user's intended outcome. It can handle tasks like form filling, clicking buttons, data extraction,
    and multi-step workflows.

    It can even help you find updated data on the internet if your model information is outdated.

    Args:
        prompt: A natural language description of what needs to be accomplished (e.g. "Book a flight from
               NYC to LA", "Sign up for the newsletter", "Find the price of item X", "Apply to a job")
        url: The starting URL of the website where the task should be performed
    """
    skyvern_agent = Skyvern(
        base_url=settings.SKYVERN_BASE_URL,
        api_key=settings.SKYVERN_API_KEY,
    )
    res = await skyvern_agent.run_task(prompt=prompt, url=url, user_agent="skyvern-mcp", wait_for_completion=True)

    # TODO: It would be nice if we could return the task URL here
    output = res.model_dump()["output"]
    base_url = settings.SKYVERN_BASE_URL
    run_history_url = (
        "https://app.skyvern.com/history" if "skyvern.com" in base_url else "http://localhost:8080/history"
    )
    return {"output": output, "run_history_url": run_history_url}


def get_pids_on_port(port: int) -> List[int]:
    """Return a list of PIDs listening on the given port."""
    pids = []
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == "LISTEN":
            pids.append(conn.pid)
    return list(set(pids))


def kill_pids(pids: List[int]) -> None:
    """Kill the given list of PIDs in a cross-platform way."""
    host_system = detect_os()
    for pid in pids:
        try:
            if host_system in {"windows", "wsl"}:
                # Windows-specific process termination
                subprocess.run(f"taskkill /PID {pid} /F", shell=True, check=False)
            else:
                os.kill(pid, 9)
        except Exception:
            console.print(f"[red]Failed to kill process {pid}[/red]")


@run_app.command(name="server")
def run_server() -> None:
    """Run the Skyvern API server."""
    load_dotenv()
    console.print(Panel("[bold green]Starting Skyvern API Server[/bold green]", border_style="green"))
    console.print("🌐 [bold]Server will be available at:[/bold] [cyan]http://localhost:8000[/cyan]")
    console.print("📚 [bold]API documentation at:[/bold] [cyan]http://localhost:8000/docs[/cyan]")

    try:
        uvicorn.run(
            "skyvern.forge:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Server stopped by user.[/bold yellow]")


@run_app.command(name="ui")
def run_ui() -> None:
    """Run the Skyvern UI."""
    load_dotenv()
    console.print(Panel("[bold blue]Starting Skyvern UI[/bold blue]", border_style="blue"))
    console.print("🌐 [bold]UI will be available at:[/bold] [cyan]http://localhost:8080[/cyan]")

    # Check if the UI directory exists
    ui_dir = Path("skyvern-frontend")
    if not ui_dir.exists():
        console.print("[red]UI directory not found. Please make sure you're in the correct directory.[/red]")
        raise typer.Exit(1)

    # Check if node_modules exists
    node_modules = ui_dir / "node_modules"
    if not node_modules.exists():
        console.print("[yellow]Installing UI dependencies...[/yellow]")
        try:
            subprocess.run(["npm", "install"], cwd=ui_dir, check=True)
        except subprocess.CalledProcessError:
            console.print("[red]Failed to install UI dependencies. Please check your Node.js installation.[/red]")
            raise typer.Exit(1)

    try:
        # Start the UI development server
        subprocess.run(["npm", "run", "dev"], cwd=ui_dir, check=True)
    except subprocess.CalledProcessError:
        console.print("[red]Failed to start UI. Please check your Node.js installation.[/red]")
        raise typer.Exit(1)
    except KeyboardInterrupt:
        console.print("\n[bold yellow]UI stopped by user.[/bold yellow]")


@run_app.command(name="all")
def run_all() -> None:
    """Run both the Skyvern API server and UI."""
    console.print(Panel("[bold purple]Starting Skyvern (API Server + UI)[/bold purple]", border_style="purple"))
    asyncio.run(start_services())


@run_app.command(name="mcp")
def run_mcp() -> None:
    """Run the Skyvern MCP server."""
    load_dotenv()
    console.print(Panel("[bold cyan]Starting Skyvern MCP Server[/bold cyan]", border_style="cyan"))
    console.print("🔗 [bold]MCP server will be available for AI applications.[/bold]")

    try:
        # Start the MCP server
        mcp.run()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]MCP server stopped by user.[/bold yellow]")


@run_app.command(name="kill")
def kill_services() -> None:
    """Kill any running Skyvern services."""
    console.print(Panel("[bold red]Killing Skyvern Services[/bold red]", border_style="red"))

    # Kill processes on common Skyvern ports
    ports_to_check = [8000, 8080]
    killed_any = False

    for port in ports_to_check:
        pids = get_pids_on_port(port)
        if pids:
            console.print(f"🔪 [bold]Killing processes on port {port}...[/bold]")
            kill_pids(pids)
            killed_any = True

    if not killed_any:
        console.print("[yellow]No Skyvern services found running.[/yellow]")
    else:
        console.print("✅ [green]Skyvern services killed.[/green]")


@run_app.command(name="status")
def check_status() -> None:
    """Check the status of Skyvern services."""
    console.print(Panel("[bold blue]Skyvern Services Status[/bold blue]", border_style="blue"))

    ports_to_check = [(8000, "API Server"), (8080, "UI")]
    any_running = False

    for port, service_name in ports_to_check:
        pids = get_pids_on_port(port)
        if pids:
            console.print(f"🟢 [green]{service_name} is running on port {port} (PID: {', '.join(map(str, pids))})[/green]")
            any_running = True
        else:
            console.print(f"🔴 [red]{service_name} is not running on port {port}[/red]")

    if not any_running:
        console.print("\n[yellow]No Skyvern services are currently running.[/yellow]")
        console.print("[italic]Use 'skyvern run all' to start all services.[/italic]")
    else:
        console.print("\n[green]Some Skyvern services are running.[/green]")
        console.print("[italic]Use 'skyvern run kill' to stop all services.[/italic]")
