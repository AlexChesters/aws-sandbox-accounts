.PHONY: clean venv test package

clean:
	( \
		rm -rf build .venv \
	)

install: clean
	uv sync

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			uv run ruff check db_client \
	)

package: install
	( \
		sh package.sh \
	)

run:
	( \
		export TABLE_NAME=test-aws-sandbox-accounts-account-pool && \
		export AWS_PROFILE=sandbox-administrator && \
		uv run python run.py \
	)
