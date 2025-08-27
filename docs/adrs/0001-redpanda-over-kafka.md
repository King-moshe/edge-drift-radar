
# ADR 0001 – Choose Redpanda over Kafka for Edge streaming

*Status*: Proposed (Day 1), to be validated in Day 4
*Context*: We need Kafka-compatible streaming with small footprint for edge/dev.
*Decision*: Use **Redpanda** (Kafka API compatible), single binary, lower ops overhead.
*Consequences*:
- (+) Faster local/dev setup, good DX, fewer moving parts.
- (+) Kafka API compatibility lets us reuse clients/consumers.
- (±) Some enterprise Kafka ecosystem tools may need adjustments.
*References*:
- https://redpanda.com/
