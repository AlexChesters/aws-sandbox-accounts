.PHONY: clean venv test package

clean:
	rm -rf build

install:
	( \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry install \
	)

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry run pylint account_manager_db_client \
	)

prod_requirements:
	poetry export -f requirements.txt --output requirements.prod.txt --only main

run:
	( \
		export TABLE_NAME=test-aws-sandbox-accounts-account-pool && \
		export AWS_PROFILE=sandbox-administrator && \
		poetry run python run.py \
	)
