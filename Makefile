.PHONY: makemigrations
makemigrations:
	uv run alembic revision --autogenerate

.PHONY: migrate
migrate:
	uv run alembic upgrade head

.PHONY: dev
dev:
	uv run uvicorn --app-dir src main:app --reload

.PHONY: consumer
consumer:
	uv run --directory src consumer.py
