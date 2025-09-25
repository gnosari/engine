Let's start a new Project. 

Context:
- Greenfield Python WebSocket server project (real-time, scalable, secure).
- Initial domain + use cases: {domain_and_use_cases}.
- Exact message formats & contracts (client↔server, success/error, versions, examples): {ws_message_formats}.
  ⚠️ Include full JSON schemas/examples inline (types, optional fields, enums, error envelopes).

Requirements (EXTREMELY CONCISE + SOLID):
- Only actionable steps and essential details.
- SOLID boundaries: Transport (WS/HTTP) ↔ Application Services (use-cases) ↔ Domain ↔ Infrastructure (DB/cache/broker).
- Clean architecture, dependency inversion (ports/adapters), small interfaces, testability.

Library Selection (propose options + pick one set; justify briefly):
- Runtime/Concurrency: asyncio (+ uvloop) | Trio (via anyio) — choose and justify.
- WS Framework/ASGI: websockets | Starlette | Django Channels | aiohttp WS — choose and justify.
- ASGI Server: uvicorn | hypercorn | gunicorn+uvicorn workers — choose and justify.
- Serialization/Validation: Pydantic v2 (BaseModel/TypeAdapter); msgspec (optional for perf) — choose and justify.
- Data Layer: SQLAlchemy 2.x (async) + Alembic; or Prisma; or Tortoise — choose and justify.
- Caching/Coordination: redis-py/aioredis; locks, rate limits, pub/sub.
- Message Broker (horizontal fan-out): aiokafka | aio-pika (RabbitMQ) | NATS — choose and justify.
- Background Jobs: Arq | Celery (redis/rabbit) | Dramatiq — choose and justify.
- Observability: structlog (JSON) + OpenTelemetry (traces/metrics) + Prometheus client + Sentry/Errors.
- Testing: pytest, pytest-asyncio, httpx/WS clients, jsonschema/pydantic for contract tests, locust/k6 for load.
- Security: pyca/cryptography, python-jose/pyjwt for JWT, passlib/argon2 for hashing, secure config via pydantic-settings.

Architecture & Contracts:
- Define WS routes/paths, subprotocols (if any), handshake/auth (JWT/OAuth2), correlation/request IDs, versioning strategy (v1, deprecation policy).
- Connection Manager: track connections, groups/rooms, broadcast/unicast, backpressure handling, ping/pong heartbeats, reconnection guidance.
- Message lifecycle: validate → authorize → route → execute use-case → persist → publish/broadcast → ack/error.
- Error model: stable error codes, messages, details; retryable vs non-retryable; throttling/rate-limit feedback.
- State mapping: inbound payload → DTO → domain; domain event → outbound payload.

Implementation Steps (bullet-only, no fluff):
1) Project scaffold: repo structure (src/…; apps/{transport,app,domain,infra}), toolchain (ruff, black, mypy, pre-commit).
2) Choose and pin library stack (above); record versions; enable uvloop if asyncio.
3) Define Pydantic models: messages (C2S/S2C), errors, configs; jsonschema export for contracts.
4) Build ConnectionManager and routing (event name → handler); DI for services.
5) Implement auth (JWT), per-connection context, permissions.
6) Implement core use-cases (application services) with ports (repos/brokers); adapters in infra.
7) Persistence: async DB setup, migrations, repositories; Redis cache + pub/sub for fan-out.
8) Resilience: timeouts, cancellation, retry/backoff (idempotency keys), circuit-breakers where relevant.
9) Rate limits & quotas; message size limits; chunking strategy if needed.
10) Observability: structured logs, request IDs, metrics (connects, msgs/sec, p95 lat), traces.
11) Security hardening: origin policy, CSRF posture (document), input/output validation, secrets handling.
12) Performance: batching, caching policy, N+1 avoidance, lazy loads; horizontal scale via broker/pub-sub.
13) Docs: minimal ADRs (choices/tradeoffs), runbook (ops), message catalog (schemas, examples).

Edge/Failure Matrix (must include):
- Auth failure, schema mismatch/version skew, duplicate msgs, dropped connections, slow consumers/backpressure, broker/DB outages, partial writes, retries/timeouts.

Testing Plan (concise but complete):
- Unit: domain/services/validators.
- Contract: jsonschema/pydantic validation for all message types; golden samples.
- Integration: WS connect/auth/subscribe/send/receive/error; DB/cache/broker.
- E2E: critical flows; chaos tests for disconnects.
- Load: concurrency, broadcast fan-out, soak tests.

Deliverable:
- An **extremely concise**, step-by-step plan in `planning/{filename}.md` with:
  1) Overview & scope
  2) Chosen stack (with brief justification)
  3) WS routes & message formats (exact)
  4) Architecture (SOLID boundaries, ports/adapters)
  5) Implementation steps
  6) Edge/failure matrix
  7) Testing plan
  8) Observability, performance, security
  9) Risks/assumptions