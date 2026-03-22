# URL Shortener

A microservice application for shortening URLs.

## Stack

- **Python 3.14**, **uv**
- **Backend** — [Litestar](https://litestar.dev) + SQLAlchemy (PostgreSQL)
- **Generator** — [FastStream](https://faststream.airt.ai) (NATS) + Redis
- **Message broker** — NATS (JetStream)
- **Docker Compose** — orchestration

## Architecture

```
┌──────────┐  POST /shorten   ┌──────────┐  NATS request   ┌───────────┐
│  Client  │ ───────────────► │ Backend  │ ──────────────► │ Generator │
│          │ ◄─────────────── │ (Litestar│ ◄────────────── │(FastStream│
└──────────┘   JSON response  │ + PG)    │   slug response │ + Redis)  │
                              └──────────┘                 └───────────┘
                                   │                            │
                                   ▼                            ▼
                              PostgreSQL                      Redis
                             (URL storage)                 (slug pool)
```

**Backend** — HTTP API, stores `slug → original_url` pairs in PostgreSQL.

**Generator** — listens on NATS subject `slug.get`, returns unique 6-character slugs from a Redis pool.

## How it works

1. Client sends `POST /shorten` with `original_url` (and an optional `slug`).
2. If no slug is provided, backend requests one from the generator via NATS (`slug.get`).
3. Generator pops a random slug from a Redis SET (`SPOP`). If the pool drops below the threshold, a background task refills it in batches.
4. Backend saves `slug + original_url` to PostgreSQL and returns the result.
5. `GET /{slug}` — redirects (302) to the original URL.

### Slug generation

A slug is 6 characters from `[a-zA-Z0-9]` (~56.8 billion combinations), generated with `secrets.choice`. Slugs are pre-generated in batches and stored in a Redis SET, which guarantees uniqueness and O(1) retrieval.

## Quick start

```bash
cp .env.template .env
cp services/backend/.env.template services/backend/.env
cp services/generator/.env.template services/generator/.env

make dev
```

## API

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/shorten` | Create a short link |
| `GET` | `/{slug}` | Redirect to the original URL |

### POST /shorten

```json
{ "original_url": "https://example.com", "slug": "abc123" }
```

`slug` is optional (6–18 characters). If omitted, it is generated automatically.

## Deployment

The service is deployed on a VPS behind [Traefik](https://traefik.io/) reverse proxy with automatic HTTPS (Let's Encrypt).

**CI/CD:** GitHub Actions — push to `main` triggers lint/typecheck/tests, then deploys via SSH (`docker compose up -d --build`).

**Required GitHub Secrets:** `HOST`, `USERNAME`, `PRIVATE_KEY`.

## Project structure

```
├── docker-compose.yaml            # base service definitions
├── docker-compose.dev.yaml        # dev overrides (ports, volumes, hot-reload)
├── docker-compose.prod.yaml       # prod overrides (restart, Traefik labels)
├── Makefile                       # dev, prod, test, check, format, migrate
├── .env.template                  # root env template (Postgres, ports)
│
├── services/backend/
│   ├── src/
│   │   ├── main.py                # Litestar app factory, lifespan
│   │   ├── api/
│   │   │   ├── controllers/       # HTTP handlers (index, url)
│   │   │   └── schemas/           # request/response models (msgspec)
│   │   ├── core/
│   │   │   ├── config.py          # pydantic-settings configuration
│   │   │   ├── exceptions/        # AppError hierarchy + handler
│   │   │   ├── models/            # SQLAlchemy ORM models
│   │   │   ├── services/          # business logic (url, broker)
│   │   │   └── providers.py       # DI providers
│   │   └── infra/                 # broker and database initialization
│   └── tests/
│
└── services/generator/
    ├── src/
    │   ├── main.py                # FastStream app, lifespan
    │   ├── handlers/              # NATS message handlers
    │   ├── schemas/               # response models (msgspec)
    │   ├── core/
    │   │   ├── config.py          # pydantic-settings configuration
    │   │   ├── exceptions.py      # AppError, PoolExhaustedError
    │   │   ├── services/          # slug generation + pool management
    │   │   └── providers.py       # DI providers
    │   └── infra/                 # Redis initialization
    └── tests/
```
