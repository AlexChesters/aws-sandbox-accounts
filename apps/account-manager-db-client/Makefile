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
	poetry export -f requirements.txt --output requirements.txt --only main

package: clean install test
	( \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			export VENV_PATH=$(poetry env info -p) && \
			poetry install --only main && \
			mkdir build && \
			cp -R ${VENV_PATH}/lib/python3.*/site-packages/* build/ && \
			cp -R account_manager_db_client/ build/ \
	)
