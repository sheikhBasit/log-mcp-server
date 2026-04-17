from fastmcp import FastMCP
from log_mcp.tools.file_logs import (
    filter_by_level,
    search_logs,
    summarize_errors,
    tail_logs,
)
from log_mcp.tools.docker_logs import (
    docker_search,
    docker_summarize_errors,
    docker_tail,
)

mcp = FastMCP("log-mcp-server")


@mcp.tool()
def tail(path: str, lines: int = 100) -> dict:
    """Tail last N lines from a log file."""
    return tail_logs(path, lines)


@mcp.tool()
def search(path: str, pattern: str, max_results: int = 200) -> dict:
    """Search a log file with a regex pattern. Returns matching lines."""
    return search_logs(path, pattern, max_results)


@mcp.tool()
def filter_level(path: str, level: str) -> dict:
    """Filter log file by level: ERROR, WARN, INFO, DEBUG. Supports JSON and plain text logs."""
    return filter_by_level(path, level)


@mcp.tool()
def summarize(path: str, max_errors: int = 20) -> dict:
    """Summarize and group errors by pattern from a log file."""
    return summarize_errors(path, max_errors)


@mcp.tool()
def docker_logs(container: str, lines: int = 100) -> dict:
    """Tail last N lines from a Docker container's logs."""
    return docker_tail(container, lines)


@mcp.tool()
def docker_grep(container: str, pattern: str, tail: int = 1000) -> dict:
    """Search Docker container logs with a regex pattern."""
    return docker_search(container, pattern, tail)


@mcp.tool()
def docker_errors(container: str, tail: int = 2000) -> dict:
    """Summarize and group errors from a Docker container's logs."""
    return docker_summarize_errors(container, tail)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
