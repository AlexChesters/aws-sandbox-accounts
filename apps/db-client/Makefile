.PHONY: clean venv test package

clean:
	( \
		rm -rf build .venv \
	)

install: clean
	( \
			poetry install && \
			poetry env use python3.11 \
	)

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry run ruff check db_client \
	)

package: install
	( \
		sh package.sh \
	)

run:
	( \
		export TABLE_NAME=test-aws-sandbox-accounts-account-pool && \
		export AWS_PROFILE=sandbox-administrator && \
		poetry run python run.py \
	)
