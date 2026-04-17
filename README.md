# log-mcp-server

A log analysis MCP server — tail, search, filter, and summarize logs from local files and Docker containers.

## Tools

| Tool | Description |
|---|---|
| `tail` | Tail last N lines from a log file |
| `search` | Regex search in a log file |
| `filter_level` | Filter by level (ERROR/WARN/INFO/DEBUG) — JSON and plain text |
| `summarize` | Group and count errors by pattern |
| `docker_logs` | Tail last N lines from a Docker container |
| `docker_grep` | Regex search in Docker container logs |
| `docker_errors` | Summarize errors from a Docker container |

## Quick Start

```bash
git clone https://github.com/sheikhBasit/log-mcp-server
cd log-mcp-server
python -m venv .venv && .venv/bin/pip install -e .
log-mcp
```

## Claude Desktop Config

```json
{
  "mcpServers": {
    "logs": {
      "command": "/path/to/.venv/bin/log-mcp"
    }
  }
}
```

## Usage Examples

```
tail the last 50 lines of /var/log/nginx/error.log
search for "timeout" in /app/logs/api.log
filter ERROR lines from /app/logs/app.log
summarize errors in the "backend" docker container
tail 100 lines from docker container "nexavoxa-api"
```

## Running Tests

```bash
pip install -e ".[dev]"
pytest
```

## License

MIT
