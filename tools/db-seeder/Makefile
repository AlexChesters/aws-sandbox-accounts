install:
	poetry install

test_db:
	poetry run python -m db_seeder.main --table-name test-aws-sandbox-accounts-account-pool

live_db:
	poetry run python -m db_seeder.main --table-name live-aws-sandbox-accounts-account-pool
