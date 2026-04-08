.PHONY: clean venv test package

clean:
	rm -rf build

install:
	uv sync

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			uv run ruff check auth_client \
	)

package: install
	( \
		sh package.sh \
	)
