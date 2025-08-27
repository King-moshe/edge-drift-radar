import os, json, sys, time
from confluent_kafka import Consumer, KafkaException, KafkaError

BOOTSTRAP_SERVERS = os.getenv("BOOTSTRAP_SERVERS", "redpanda:9092")
TOPIC = os.getenv("TOPIC", "edr.telemetry")
GROUP_ID = os.getenv("GROUP_ID", "edr-consumer")

conf = {
    "bootstrap.servers": BOOTSTRAP_SERVERS,
    "group.id": GROUP_ID,
    "auto.offset.reset": "earliest",
    "enable.auto.commit": True,
}

def main():
    c = Consumer(conf)
    c.subscribe([TOPIC])
    print(f"👂 Listening on topic={TOPIC} brokers={BOOTSTRAP_SERVERS} group={GROUP_ID}")
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise KafkaException(msg.error())
            print(f"📥 {msg.topic()}[{msg.partition()}]@{msg.offset()} key={msg.key()} value={msg.value()}")
            # TODO: Day 5 – write to TimescaleDB
    except KeyboardInterrupt:
        pass
    finally:
        print("↩️  Closing consumer...")
        c.close()

if __name__ == "__main__":
    main()
