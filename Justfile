default:
    just --list

lint:
    uv run ruff check --fix
    uv run ruff format
    uv run ty check

dev:
    docker compose up -d

dev-down:
    docker compose down
