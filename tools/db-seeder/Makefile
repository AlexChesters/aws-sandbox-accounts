install:
	uv sync

test_db:
	uv run python -m db_seeder.main --env test

live_db:
	uv run python -m db_seeder.main --env live
