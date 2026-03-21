.PHONY: dev prod down logs migration migrate format check

dev:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml up --build

prod:
	docker compose -f docker-compose.yaml -f docker-compose.prod.yaml up --build

down:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml -f docker-compose.prod.yaml down

logs:
	docker compose -f docker-compose.yaml -f docker-compose.dev.yaml logs -f

migration:
	docker exec backend uv run alembic revision --autogenerate -m "$(m)"

migrate:
	docker exec backend uv run alembic upgrade head

format:
	cd services/backend && uv run ruff check --fix .
	cd services/backend && uv run ruff format .
	cd services/generator && uv run ruff check --fix .
	cd services/generator && uv run ruff format .

check:
	cd services/backend && uv run ruff check src
	cd services/backend && uv run mypy src
	cd services/generator && uv run ruff check src
	cd services/generator && uv run mypy src
