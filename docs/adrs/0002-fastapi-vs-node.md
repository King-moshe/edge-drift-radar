# ADR 0002 – FastAPI (Python) vs Node.js for Agent/Services

*Status*: Proposed (Day 2)
*Context*: Agent runs at the edge; we need quick prototyping and direct use of online-ML libs (River/Evidently).
*Decision*: Use **Python + FastAPI** for Agent and early services. Keep Node.js for gateways/UI if needed.
*Consequences*:
- (+) Tight integration with River/Evidently/Great Expectations.
- (+) Fast developer loop; Pydantic validation.
- (±) Performance: fine for MVP; hot paths can be optimized with C/WASM later.
- (±) Packaging on constrained devices → use `python:3.11-slim`, poetry/uv, and multi-stage builds.
*Alternatives*: Node.js (Express/Fastify) – stronger async throughput, weaker ML ecosystem for our needs.
