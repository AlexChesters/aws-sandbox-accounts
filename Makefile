.PHONY: clean test package install_poetry

clean:
	cd apps/account-manager-db-client && $(MAKE) clean

test:
	cd apps/account-manager-db-client && $(MAKE) test

package:
	cd apps/account-manager-db-client && $(MAKE) package

install_poetry:
	( \
		echo 'Installing poetry...' && \
		curl -sSL https://install.python-poetry.org | POETRY_HOME=${HOME}/.poetry python3 - \
	)

build: clean install_poetry test package
