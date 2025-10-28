#!/usr/bin/env python3
"""
FastMCP client for the ContactsServer.

This client demonstrates how to connect to and interact with the MCP server
using the FastMCP Client API.

Environment (optional):
- MCP_HOST (default: 0.0.0.0)
- MCP_PORT (default: 8000)

Usage:
    python fastmcp_client.py
    MCP_HOST=localhost MCP_PORT=8000 python fastmcp_client.py
"""

import asyncio
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastmcp import Client
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install as rich_traceback

# Setup
load_dotenv()
rich_traceback(show_locals=False)
console = Console()

MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "8000"))
MCP_BASE = f"http://{MCP_HOST}:{MCP_PORT}/mcp"

# Render helpers
def header(title: str) -> None:
    console.print(Panel.fit(f"[bold]{title}[/bold]", border_style="cyan"))

def ok(msg: str) -> None:
    console.print(f"[bold green]✓[/bold green] {msg}")

def info(msg: str) -> None:
    console.print(f"[bold blue]›[/bold blue] {msg}")

def warn(msg: str) -> None:
    console.print(f"[bold yellow]![/bold yellow] {msg}")

def fail(msg: str) -> None:
    console.print(f"[bold red]✗[/bold red] {msg}")


async def main():
    header("FastMCP Client — ContactsServer Test")
    
    # Create client for HTTP server
    client = Client(MCP_BASE)
    
    async with client:
        info("Connected to MCP server")
        
        # Ping the server
        try:
            await client.ping()
            ok("Server ping successful")
        except Exception as e:
            warn(f"Ping failed: {e}")
        
        # List available operations
        info("Listing available operations")
        
        # List tools
        try:
            tools = await client.list_tools()
            if tools:
                table = Table(title="Available Tools")
                table.add_column("Name", style="bold")
                table.add_column("Description")
                for tool in tools:
                    table.add_row(
                        tool.name,
                        getattr(tool, "description", "No description")
                    )
                console.print(table)
                ok(f"Found {len(tools)} tool(s)")
            else:
                warn("No tools available")
        except Exception as e:
            fail(f"Error listing tools: {e}")
        
        # List resources
        try:
            resources = await client.list_resources()
            if resources:
                table = Table(title="Available Resources")
                table.add_column("URI", style="bold")
                table.add_column("Name")
                table.add_column("MIME Type")
                for resource in resources:
                    table.add_row(
                        str(resource.uri),
                        getattr(resource, "name", ""),
                        getattr(resource, "mimeType", getattr(resource, "mime_type", ""))
                    )
                console.print(table)
                ok(f"Found {len(resources)} resource(s)")
            else:
                warn("No resources available")
        except Exception as e:
            fail(f"Error listing resources: {e}")
        
        # List prompts
        try:
            prompts = await client.list_prompts()
            if prompts:
                table = Table(title="Available Prompts")
                table.add_column("Name", style="bold")
                table.add_column("Description")
                for prompt in prompts:
                    table.add_row(
                        prompt.name,
                        getattr(prompt, "description", "No description")
                    )
                console.print(table)
                ok(f"Found {len(prompts)} prompt(s)")
            else:
                warn("No prompts available")
        except Exception as e:
            fail(f"Error listing prompts: {e}")
        
        # Read contacts resource
        info("Reading data://contacts resource")
        try:
            contacts_before = await client.read_resource("data://contacts")
            console.print(f"[dim]Contacts before: {contacts_before}[/dim]")
            ok("Successfully read contacts resource")
        except Exception as e:
            fail(f"Error reading resource: {e}")
        
        # Test the summarize prompt
        info("Testing 'summarize' prompt")
        try:
            prompt_result = await client.get_prompt(
                "summarize",
                arguments={"text": "This is a sample text that needs to be summarized for testing purposes."}
            )
            console.print(f"[dim]Prompt result: {prompt_result}[/dim]")
            ok("Successfully retrieved prompt")
        except Exception as e:
            fail(f"Error getting prompt: {e}")
        
        # Call the save_contact tool
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        unique_email = f"test+{timestamp}@example.com"

        info(f"Calling save_contact tool with email: {unique_email}")
        try:
            result = await client.call_tool(
                "save_contact",
                arguments={
                    "name": "Test User",
                    "email": unique_email
                }
            )
            console.print(f"[dim]Tool result: {result}[/dim]")
            ok("Successfully saved contact")
        except Exception as e:
            fail(f"Error calling tool: {e}")
        
        # Re-read contacts to verify the update
        info("Re-reading data://contacts to verify update")
        try:
            contacts_after = await client.read_resource("data://contacts")
            console.print(f"[dim]Contacts after: {contacts_after}[/dim]")
            ok("Successfully verified contact was saved")
        except Exception as e:
            fail(f"Error reading resource: {e}")
        
        ok("All operations completed successfully!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
    except Exception as e:
        fail(f"Fatal error: {e}")
        raise
