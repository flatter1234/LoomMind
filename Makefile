.PHONY: run clean format lint

run:
	uv run python src/main.py

format:
	uv run --group dev ruff format src

lint:
	uv run --group dev ruff format --check src
	uv run --group dev ruff check src

clean:
	rm -rf .ruff_cache
	find . -type d -name '__pycache__' -exec rm -rf {} +
