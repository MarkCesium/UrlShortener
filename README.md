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
