import re
from collections import Counter
from typing import Any

import docker
from docker.errors import NotFound, DockerException


def _get_client():
    try:
        return docker.from_env()
    except DockerException as e:
        raise RuntimeError(f"Docker not available: {e}") from e


def docker_tail(container: str, lines: int = 100) -> dict[str, Any]:
    try:
        client = _get_client()
        raw = client.containers.get(container).logs(tail=lines, stream=False)
        log_lines = raw.decode(errors="replace").splitlines()
        return {"lines": log_lines, "total_returned": len(log_lines), "container": container, "error": None}
    except NotFound:
        return {"lines": [], "total_returned": 0, "container": container, "error": f"Container not found: {container}"}
    except Exception as e:
        return {"lines": [], "total_returned": 0, "container": container, "error": str(e)}


def docker_search(container: str, pattern: str, tail: int = 1000) -> dict[str, Any]:
    try:
        client = _get_client()
        raw = client.containers.get(container).logs(tail=tail, stream=False)
        all_lines = raw.decode(errors="replace").splitlines()
        regex = re.compile(pattern, re.IGNORECASE)
        matched = [l for l in all_lines if regex.search(l)]
        return {"matches": matched, "match_count": len(matched), "container": container, "error": None}
    except NotFound:
        return {"matches": [], "match_count": 0, "container": container, "error": f"Container not found: {container}"}
    except re.error as e:
        return {"matches": [], "match_count": 0, "container": container, "error": f"Invalid regex: {e}"}
    except Exception as e:
        return {"matches": [], "match_count": 0, "container": container, "error": str(e)}


def docker_summarize_errors(container: str, tail: int = 2000) -> dict[str, Any]:
    try:
        client = _get_client()
        raw = client.containers.get(container).logs(tail=tail, stream=False)
        all_lines = raw.decode(errors="replace").splitlines()
        error_lines = [
            l.strip() for l in all_lines
            if "error" in l.lower() or "exception" in l.lower() or "fatal" in l.lower()
        ]

        def normalize(line: str) -> str:
            line = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[\.\d+Z]*", "", line)
            line = re.sub(r"\b[0-9a-f]{8,}\b", "<id>", line)
            return line.strip()

        counts = Counter(normalize(l) for l in error_lines)
        top = [{"message": msg, "count": cnt} for msg, cnt in counts.most_common(20)]

        return {
            "container": container,
            "total_error_lines": len(error_lines),
            "unique_patterns": len(counts),
            "top_errors": top,
            "error": None,
        }
    except NotFound:
        return {"container": container, "total_error_lines": 0, "unique_patterns": 0, "top_errors": [], "error": f"Container not found: {container}"}
    except Exception as e:
        return {"container": container, "total_error_lines": 0, "unique_patterns": 0, "top_errors": [], "error": str(e)}
