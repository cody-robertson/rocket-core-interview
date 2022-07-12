makemigrations:
	docker compose run api python manage.py makemigrations

migrate:
	docker compose run api python manage.py migrate

init_db:
	docker compose run api python manage.py init_db products.json

start:
	docker compose up --build -d

stop:
	docker compose down

restart:
	docker compose restart