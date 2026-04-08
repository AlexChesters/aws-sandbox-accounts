install:
	uv sync

test:
	uv run ruff check lease_manager_web

run:
	uv run flask --app lease_manager_web.app run --host 0.0.0.0 --port 5000
