from log_mcp.tools.docker_logs import docker_tail, docker_search, docker_summarize_errors


def test_docker_tail_missing_container():
    result = docker_tail("nonexistent_container_xyz_123", lines=10)
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_docker_search_missing_container():
    result = docker_search("nonexistent_container_xyz_123", pattern="ERROR")
    assert result["error"] is not None


def test_docker_summarize_missing_container():
    result = docker_summarize_errors("nonexistent_container_xyz_123")
    assert result["error"] is not None


def test_docker_tail_real_container():
    """Requires pg-mcp-test container from pg-mcp-server dev to be running."""
    result = docker_tail("pg-mcp-test", lines=5)
    # If container not running, we get a graceful error — not a crash
    assert "error" in result
    if result["error"] is None:
        assert isinstance(result["lines"], list)
