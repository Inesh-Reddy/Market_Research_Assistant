#!/usr/bin/env bash
set -e
cd apps/backend && uv run ruff check app tests || true
