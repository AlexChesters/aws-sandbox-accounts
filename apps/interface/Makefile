.PHONY: venv
venv:
	poetry install

.PHONY: devserver
devserver:
	poetry run python manage.py runserver

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: gunicorn
gunicorn:
	poetry run gunicorn aws_sandbox_accounts_interface.wsgi
