# RateGuard 🛡️

A lightweight, modular **rate limiting library** for [FastAPI](https://fastapi.tiangolo.com/) applications. RateGuard provides a clean decorator-based API to protect your endpoints from abuse, with pluggable algorithms and storage backends.

---

## Features

- ✅ Simple `@limit` decorator — drop onto any route handler
- ✅ **Fixed Window** algorithm out of the box
- ✅ Smart key resolution — auto-detects authenticated users or falls back to client IP
- ✅ Custom key resolver support for advanced use cases
- ✅ Pluggable storage backend (in-memory by default, extensible)
- ✅ Returns `429 Too Many Requests` with `retry_after` metadata
- ✅ Zero external dependencies beyond FastAPI

---

## Project Structure

```
rateguard/                        ← project root
├── rateguard/                    ← installable Python package
│   ├── __init__.py               # Public API surface
│   ├── py.typed                  # PEP 561 type marker
│   ├── algorithms/
│   │   └── fixed_window.py       # Fixed Window rate limiting algorithm
│   ├── core/
│   │   ├── limiter.py            # RateLimiter — orchestrates algorithm checks
│   │   ├── policy.py             # RateLimitPolicy — limit & window config
│   │   └── resolver.py           # KeyResolver — identifies the client
│   ├── decorators/
│   │   └── decorator.py          # @limit decorator — the main public API
│   └── storage/
│       └── storage.py            # MemoryStorage — in-memory key/value store
├── examples/
│   └── basic_usage.py            # Example FastAPI app
├── pyproject.toml                # Package metadata & build config
├── setup.py                      # Editable install shim
├── requirements.txt
└── README.md
```

---

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/AdeelMalik22/rateguard.git
cd rateguard
pip install -e .
```

The `-e` flag installs it in **editable mode** — any changes you make to the source are reflected immediately without reinstalling.

### From PyPI *(once published)*

```bash
pip install rateguard
```

---

## Quick Start

```python
from fastapi import FastAPI, Request
from rateguard import limit

app = FastAPI()


@limit(requests=5, window=60)
def my_handler(request: Request):
    return {"message": "Hello!"}


@app.get("/hello")
def hello_route(request: Request):
    return my_handler(request)
```

### Run the server

```bash
uvicorn examples.basic_usage:app --reload
```

---

## Usage

### `@limit(requests, window, key=None)`

| Parameter  | Type       | Description                                                   |
|------------|------------|---------------------------------------------------------------|
| `requests` | `int`      | Maximum number of requests allowed within the window          |
| `window`   | `int`      | Time window in **seconds**                                    |
| `key`      | `callable` | *(Optional)* Custom function to resolve the client identifier |

#### Basic — 3 requests per 10 seconds

```python
from rateguard import limit

@limit(requests=3, window=10)
def my_endpoint(request: Request):
    return {"status": "ok"}
```

#### Custom Key Resolver

```python
from rateguard import limit

def resolve_by_api_key(*args, **kwargs):
    request = kwargs.get("request")
    return request.headers.get("X-API-Key", "anonymous")

@limit(requests=100, window=60, key=resolve_by_api_key)
def protected_endpoint(request: Request):
    return {"data": "..."}
```

---

## How It Works

```
Request
  │
  ▼
@limit decorator
  │
  ├─► KeyResolver.resolve()       → Identifies client (user ID or IP)
  │
  ├─► RateLimiter.check()         → Delegates to the algorithm
  │
  ├─► FixedWindowLimiter.allow()
  │     ├─ Fetch record from MemoryStorage
  │     ├─ Reset window if expired
  │     ├─ Block if limit reached → raise HTTPException(429)
  │     └─ Increment counter & allow
  │
  └─► Route handler executes normally
```

### Key Resolution Priority

1. **Custom resolver** — if a `key` function is passed to `@limit`
2. **Authenticated user** — reads `request.scope["user"].id` (set by auth middleware)
3. **Client IP** — falls back to `request.client.host`

---

## Algorithms

### Fixed Window

Counts requests within a fixed time window. Once the window expires, the counter resets.

- **Pros**: Simple, predictable, low memory usage
- **Cons**: Burst traffic possible at window boundaries

| Field           | Description                          |
|-----------------|--------------------------------------|
| `allowed`       | `bool` — whether the request passes  |
| `remaining`     | `int` — requests left in window      |
| `retry_after`   | `float` — seconds until window resets (only on `429`) |

---

## Storage Backends

### `MemoryStorage` (default)

In-memory dictionary store. Fast and dependency-free, but **not shared** across multiple processes or workers.

```python
from rateguard import MemoryStorage

storage = MemoryStorage()
storage.set("key", {"count": 1, "start": 1234567890.0})
storage.get("key")     # → {"count": 1, "start": ...}
storage.delete("key")
```

> **Note:** For production deployments with multiple workers, replace `MemoryStorage` with a Redis-backed implementation to share state across processes.

---

## Response Behavior

| Scenario           | HTTP Status | Response Body                                           |
|--------------------|-------------|----------------------------------------------------------|
| Request allowed    | `2xx`       | Normal route response                                    |
| Limit exceeded     | `429`       | `{"error": "Too many requests", "retry_after": <float>}` |

---

## Publishing to PyPI

```bash
# Install build tools
pip install build twine

# Build the distribution
python -m build

# Upload to PyPI
twine upload dist/*
```

---

## Requirements

| Package            | Version   |
|--------------------|-----------|
| fastapi            | ≥ 0.100.0 |
| starlette          | ≥ 0.27.0  |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/sliding-window`
3. Commit your changes: `git commit -m "feat: add sliding window algorithm"`
4. Push to the branch: `git push origin feature/sliding-window`
5. Open a Pull Request

---

## License

This project is open-source and available under the MIT License.
