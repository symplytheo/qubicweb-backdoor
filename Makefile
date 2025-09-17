# Default help command
help:
	@echo "Available commands:"
	@echo "  make run        - Run Django development server"
	@echo "  make freeze     - Freeze current dependencies to requirements.txt"
	@echo "  make install    - Install dependencies from requirements.txt"
	@echo "  make migrate    - Run makemigrations and migrate"
	@echo "  make superuser  - Create Django superuser"
	@echo "  make shell      - Open Django shell"
	@echo "  make collect    - Collect static files"
	@echo "  make test       - Run tests"

# Available commands

run:
	python manage.py runserver 3010

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

superuser:
	python manage.py createsuperuser

shell:
	python manage.py shell

collect:
	python manage.py collectstatic --noinput

test:
	python manage.py test
