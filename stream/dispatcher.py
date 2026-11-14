"""
stream/dispatcher.py  — Part D2
Publishes ride/food dispatch requests to a RabbitMQ topic exchange.

Usage:
    python stream/dispatcher.py

Environment variable (in .env):
    RABBITMQ_URL=amqp://guest:guest@localhost:5672/
    (or a CloudAMQP URL — keep it out of Git)

Every 2 seconds it picks a random city (Bangalore or Chennai),
zone, and type (ride or food), builds the routing key city.zone.type,
and publishes a JSON message to the 'rapido-dispatch' topic exchange.

For Part D3: one message in every 10 is a "bad" message that deliberately
omits the 'zone' field, so drivers can test NACK handling.
"""

import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

import pika
from dotenv import load_dotenv

load_dotenv()

EXCHANGE    = "rapido-dispatch"
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

CITIES = {
    "bangalore": ["koramangala", "indiranagar", "whitefield", "jayanagar"],
    "chennai":   ["tnagar", "adyar", "velachery", "anna_nagar"],
}
TYPES = ["ride", "food"]


def publish_forever():
    params = pika.URLParameters(RABBITMQ_URL)
    conn   = pika.BlockingConnection(params)
    ch     = conn.channel()
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    count = 0
    print(f"[dispatcher] Connected. Publishing to exchange '{EXCHANGE}' ...")

    while True:
        count += 1
        city  = random.choice(list(CITIES.keys()))
        zone  = random.choice(CITIES[city])
        otype = random.choice(TYPES)

        # Every 10th message is intentionally bad (no 'zone') — Part D3
        bad_message = (count % 10 == 0)

        if bad_message:
            # Only two words in routing key → matches nothing with * or # patterns
            # that expect three words, so drivers can NACK it
            routing_key = f"{city}.{otype}"  # e.g. "bangalore.food"
            msg = {
                "id":   str(uuid.uuid4()),
                "city": city,
                # 'zone' is intentionally missing
                "type": otype,
                "ts":   datetime.now(timezone.utc).isoformat(),
                "_bad": True,
            }
            print(f"[dispatcher] BAD MSG #{count}  key={routing_key}  {msg}")
        else:
            routing_key = f"{city}.{zone}.{otype}"
            msg = {
                "id":   str(uuid.uuid4()),
                "city": city,
                "zone": zone,
                "type": otype,
                "ts":   datetime.now(timezone.utc).isoformat(),
            }
            print(f"[dispatcher] #{count}  key={routing_key}  id={msg['id'][:8]}")

        body = json.dumps(msg).encode()
        ch.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
        time.sleep(2)


if __name__ == "__main__":
    publish_forever()
