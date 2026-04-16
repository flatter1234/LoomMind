.PHONY: run clean

LOOM := $(CURDIR)/loom

run:
	UV_PROJECT_ENVIRONMENT=$(LOOM) uv run python src/main.py

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache build dist
	find src -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find src -type f \( -name '*.py[co]' -o -name '*.pyo' \) -delete 2>/dev/null || true
	find . -maxdepth 1 -type d -name '*.egg-info' -exec rm -rf {} + 2>/dev/null || true
