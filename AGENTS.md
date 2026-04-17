# AGENTS.md

This file provides guidance to AI coding agents (Claude Code, Cursor, GitHub Copilot, etc.)
working in this repository.

## Project
MCP server for log analysis — tail, search by regex, filter by level, summarise errors across file and Docker log sources. Built with FastMCP.

## Code Style
- Python 3.11+
- Follow existing patterns in the codebase before adding new ones
- Use type hints on all public functions
- Keep file tools and Docker tools in separate modules (`file_logs.py`, `docker_logs.py`)

## Testing
- Run tests before committing: `pytest`
- Docker tests require Docker daemon running — skip gracefully if not available
- All new tools require tests in `tests/`

## Commits
- Use conventional commits: `feat:`, `fix:`, `chore:`, `docs:`
- No WIP commits to main

## What NOT to do
- Do not add dependencies without updating `pyproject.toml`
- Do not read files outside the allowed log directories
- Do not expose raw tracebacks in MCP tool output
