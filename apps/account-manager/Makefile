.PHONY: install_poetry install nuke-config

install_poetry:
	( \
		echo 'Installing poetry...' && \
		curl -sSL https://install.python-poetry.org | POETRY_HOME=${HOME}/.poetry python3 - \
	)

install:
	( \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			poetry install \
	)

nuke-config:
	poetry run python nuke.py --account-id $ACCOUNT_ID
