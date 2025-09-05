.PHONY: clean venv test package

clean:
	( \
		rm -rf build && \
		pip uninstall -r requirements.txt -y \
	)

install: clean requirements
	( \
			pip install -r requirements.txt \
	)

test: install
	( \
			export AWS_ACCESS_KEY_ID='testing' && \
			export AWS_SECRET_ACCESS_KEY='testing' && \
			export AWS_SESSION_TOKEN='testing' && \
			export AWS_SECURITY_TOKEN='testing' && \
			export PATH="${HOME}/.poetry/bin:${PATH}" && \
			pylint db_client \
	)

requirements: all_requirements prod_requirements

all_requirements:
	poetry export -f requirements.txt --output requirements.txt --with dev

prod_requirements:
	poetry export -f requirements.txt --output requirements.prod.txt --only main

package: clean requirements
	( \
		pip install -r requirements.prod.txt -t deps && \
		mkdir build && \
		cp -R deps/* build/ && \
		cp -R db_client/ build/ && \
		aws cloudformation package --template-file stacks/sandbox-administrator-account/db-client.yml --s3-bucket $ARTIFACTS_BUCKET --s3-prefix artifacts/aws-sandbox-accounts/apps/db-client --output-template-file stacks/sandbox-administrator-account/db-client.yml \
	)

run:
	( \
		export TABLE_NAME=test-aws-sandbox-accounts-account-pool && \
		export AWS_PROFILE=sandbox-administrator && \
		poetry run python run.py \
	)
