import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


def _read_lines(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Log file not found: {path}")
    return p.read_text(errors="replace").splitlines()


def tail_logs(path: str, lines: int = 100) -> dict[str, Any]:
    try:
        all_lines = _read_lines(path)
        result = all_lines[-lines:]
        return {"lines": result, "total_returned": len(result), "error": None}
    except Exception as e:
        return {"lines": [], "total_returned": 0, "error": str(e)}


def search_logs(path: str, pattern: str, max_results: int = 200) -> dict[str, Any]:
    try:
        all_lines = _read_lines(path)
        regex = re.compile(pattern, re.IGNORECASE)
        matched = [l for l in all_lines if regex.search(l)][:max_results]
        return {"matches": matched, "match_count": len(matched), "error": None}
    except re.error as e:
        return {"matches": [], "match_count": 0, "error": f"Invalid regex: {e}"}
    except Exception as e:
        return {"matches": [], "match_count": 0, "error": str(e)}


def filter_by_level(path: str, level: str) -> dict[str, Any]:
    """Filter structured JSON logs or plain text logs by level (ERROR, WARN, INFO, DEBUG)."""
    level_upper = level.upper()
    try:
        all_lines = _read_lines(path)
        matched = []
        for line in all_lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
            # Try JSON first
            try:
                obj = json.loads(line_stripped)
                log_level = (
                    obj.get("level") or obj.get("severity") or obj.get("lvl") or ""
                ).upper()
                if level_upper in log_level:
                    matched.append(line)
                    continue
            except (json.JSONDecodeError, AttributeError):
                pass
            # Plain text fallback
            if level_upper in line.upper():
                matched.append(line)
        return {"lines": matched, "match_count": len(matched), "level": level_upper, "error": None}
    except Exception as e:
        return {"lines": [], "match_count": 0, "level": level_upper, "error": str(e)}


def summarize_errors(path: str, max_errors: int = 20) -> dict[str, Any]:
    """Count and group errors by message pattern from a log file."""
    try:
        all_lines = _read_lines(path)
        error_lines = []
        for line in all_lines:
            if "error" in line.lower() or "exception" in line.lower() or "fatal" in line.lower():
                error_lines.append(line.strip())

        # Try to extract core message (strip timestamps/IDs)
        def normalize(line: str) -> str:
            # Remove timestamps like 2026-04-17T12:00:00
            line = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[\.\d+Z]*", "", line)
            # Remove hex IDs
            line = re.sub(r"\b[0-9a-f]{8,}\b", "<id>", line)
            return line.strip()

        counts = Counter(normalize(l) for l in error_lines)
        top = [{"message": msg, "count": cnt} for msg, cnt in counts.most_common(max_errors)]

        return {
            "total_error_lines": len(error_lines),
            "unique_patterns": len(counts),
            "top_errors": top,
            "error": None,
        }
    except Exception as e:
        return {"total_error_lines": 0, "unique_patterns": 0, "top_errors": [], "error": str(e)}
