import json
import pytest
from log_mcp.tools.file_logs import tail_logs, search_logs, filter_by_level, summarize_errors


@pytest.fixture
def plain_log(tmp_path):
    f = tmp_path / "app.log"
    f.write_text("\n".join([
        "2026-04-17 INFO server started",
        "2026-04-17 ERROR database connection failed",
        "2026-04-17 WARN slow query detected",
        "2026-04-17 ERROR timeout on request",
        "2026-04-17 INFO request completed",
    ]))
    return str(f)


@pytest.fixture
def json_log(tmp_path):
    f = tmp_path / "structured.log"
    lines = [
        json.dumps({"level": "info", "msg": "started"}),
        json.dumps({"level": "error", "msg": "db failed"}),
        json.dumps({"level": "warn", "msg": "slow query"}),
        json.dumps({"level": "error", "msg": "timeout"}),
    ]
    f.write_text("\n".join(lines))
    return str(f)


def test_tail_returns_last_n_lines(plain_log):
    result = tail_logs(plain_log, lines=3)
    assert result["error"] is None
    assert result["total_returned"] == 3
    assert "INFO request completed" in result["lines"][-1]


def test_tail_missing_file():
    result = tail_logs("/nonexistent/path.log", lines=10)
    assert result["error"] is not None
    assert "not found" in result["error"].lower()


def test_search_finds_matches(plain_log):
    result = search_logs(plain_log, pattern="ERROR")
    assert result["error"] is None
    assert result["match_count"] == 2


def test_search_invalid_regex(plain_log):
    result = search_logs(plain_log, pattern="[invalid")
    assert result["error"] is not None
    assert "regex" in result["error"].lower()


def test_filter_by_level_plain(plain_log):
    result = filter_by_level(plain_log, "ERROR")
    assert result["error"] is None
    assert result["match_count"] == 2


def test_filter_by_level_json(json_log):
    result = filter_by_level(json_log, "error")
    assert result["error"] is None
    assert result["match_count"] == 2


def test_summarize_errors(plain_log):
    result = summarize_errors(plain_log)
    assert result["error"] is None
    assert result["total_error_lines"] == 2
    assert result["unique_patterns"] >= 1
