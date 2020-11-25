shell:
	poetry run python favorites-api/manage.py shell_plus

install:
	poetry install

pyformat:
	poetry run black .

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	DJANGO_SETTINGS_MODULE=favorites_api.settings poetry run pytest -x -s favorites-api
