## Overview

The Model Context Protocol (MCP) is an **open-source standard** for connecting language-model driven tools (like Claude Code) to external tools, data sources, APIs, etc. ([Claude Docs][1])
By registering “MCP servers” you allow Claude Code to work with external services and query resources via the protocol. ([Claude Docs][1])
Use cases include:

* Querying databases (“Find customers who haven’t purchased in 90 days”) ([Claude Docs][1])
* Accessing issue-trackers or monitoring tools (“Show me errors in the last 24 h”) ([Claude Docs][1])
* Automating workflows (draft emails, create PRs, etc) ([Claude Docs][1])

---

## Key Steps & Commands

### 1. Add an MCP server

You register a server depending on the transport type (HTTP / SSE / stdio). Examples:

```bash
# HTTP transport (recommended)
claude mcp add --transport http <name> <url>

# Example:
claude mcp add --transport http notion https://mcp.notion.com/mcp

claude mcp add --transport http contacts http://localhost:8000/mcp
```

([Claude Docs][1])

```bash
# SSE transport (deprecated, use only if required)
claude mcp add --transport sse <name> <url>

# example:
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

([Claude Docs][1])

```bash
# stdio transport (local process)
claude mcp add --transport stdio <name> -- <command> [args]
```

([Claude Docs][1])

### 2. Manage servers

```bash
# list all servers
claude mcp list

# get details for one
claude mcp get <name>

# remove a server
claude mcp remove <name>
```

([Claude Docs][1])

### 3. Use resources from servers

Once a server is connected, you can reference its resources inside prompts:

* Use `@server:protocol://resource/path` syntax to reference a resource. ([Claude Docs][1])
* Use the `/mcp__servername__promptname` slash-command to invoke a tool prompt made available by the server. ([Claude Docs][1])

Example:

```
> Can you analyze @github:issue://123 and suggest a fix?
> /mcp__github__pr_review 456
```

([Claude Docs][1])

---

## Configuration Scopes & Best Practices

### Scopes

You can register MCP servers at three scopes:

* **Local (default)**: configurations stored in your project, only for you. ([Claude Docs][1])
* **Project**: stored in `.mcp.json` at project root, shared with the team (via version control) ([Claude Docs][1])
* **User**: available across all projects for your user account. ([Claude Docs][1])

### Precedence

If servers with the **same name** exist at multiple scopes: local > project > user. ([Claude Docs][1])

### Environment variable expansion

In `.mcp.json` you can embed environment variables like `${VAR}` or `${VAR:-default}` for flexibility. ([Claude Docs][1])

---

## Practical Examples

* **Monitor errors via Sentry**

  ```bash
  claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
  ```

  Then in Claude Code:

  > “What are the most common errors in the last 24 hours?” ([Claude Docs][1])

* **Query your PostgreSQL database**

  ```bash
  claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "postgresql://readonly:...@host:5432/dbname"
  ```

  Then in Claude Code:

  > “Find customers who haven’t purchased in 90 days” ([Claude Docs][1])

---

## Advanced / Enterprise Configuration

* You can enforce enterprise-managed MCP configurations via `managed-mcp.json` (e.g., disable user adding servers, whitelist particular servers) ([Claude Docs][1])
* You can restrict which servers users can add via `allowedMcpServers` and `deniedMcpServers` lists. ([Claude Docs][1])

---

## Important Notes & Tips

* Use HTTP transport when possible; SSE is deprecated. ([Claude Docs][1])
* Be **very careful** about security: MCP servers can fetch content that may lead to prompt injection risks. Always trust the servers you add. ([Claude Docs][1])
* When tool output is very large, Claude Code shows a warning when output exceeds 10 ,000 tokens. You can raise the limit via `MAX_MCP_OUTPUT_TOKENS`. ([Claude Docs][1])
* When a server requires OAuth, run `/mcp` inside Claude Code to authenticate. ([Claude Docs][1])

---

## Sample Workflow

Here’s a condensed workflow for you (given your context as researcher/developer):

1. Pick a service you want Claude Code to access (e.g., a database with experimental results).
2. Add the MCP server:

   ```bash
   claude mcp add --transport stdio results-db -- npx -y my-mcp-server --dsn "postgresql://read:…"
   ```
3. In Claude Code terminal, ensure the server is available:

   ```bash
   claude mcp list
   ```
4. In your prompt to Claude Code, you might write:

   > “Using the resource `@results-db:query://monthly_metrics`, show me which experiment variants improved execution time over baseline.”
5. Claude Code will fetch the data via the server, interpret it, and you can then ask follow-ups like “Plot a violin of execution time improvements by variant.”
6. If the server supports prompts, you can run slash commands:

   ```
   /mcp__results-db__run_query "SELECT variant, time_improvement FROM experiments WHERE date > '2025-01-01'"
   ```

