"""
stream/driver.py  — Part D2 / D3
Receives ride/food dispatch requests matching a binding pattern.

Usage:
    python stream/driver.py <NAME> <PATTERN>

Examples (using the D1 patterns from the assignment):
    python stream/driver.py Ravi  "bangalore.koramangala.*"
    python stream/driver.py Priya "bangalore.indiranagar.*"
    python stream/driver.py Arjun "bangalore.*.ride"
    python stream/driver.py Meena "bangalore.*.food"
    python stream/driver.py Karthik "chennai.tnagar.food"
    python stream/driver.py Control "bangalore.#"

RabbitMQ pattern rules:
    *  matches exactly ONE word (between dots)
    #  matches ZERO or more words

Environment variable (in .env):
    RABBITMQ_URL=amqp://guest:guest@localhost:5672/

Part D3: a message whose JSON body is missing the 'zone' field gets
basic_nack(requeue=False) — it is discarded to the dead-letter queue
(or dropped if no DLX is configured). Every other message gets basic_ack.
"""

import json
import os
import sys

import pika
from dotenv import load_dotenv

load_dotenv()

EXCHANGE     = "rapido-dispatch"
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")


def main(driver_name: str, pattern: str):
    params = pika.URLParameters(RABBITMQ_URL)
    conn   = pika.BlockingConnection(params)
    ch     = conn.channel()

    # Declare the exchange (idempotent — safe if dispatcher already declared it)
    ch.exchange_declare(exchange=EXCHANGE, exchange_type="topic", durable=True)

    # Private, exclusive queue — disappears when this driver disconnects
    result = ch.queue_declare(queue="", exclusive=True)
    queue  = result.method.queue

    # Bind this queue to the exchange using the driver's pattern
    ch.queue_bind(exchange=EXCHANGE, queue=queue, routing_key=pattern)
    print(f"[{driver_name}] Queue '{queue}' bound with pattern '{pattern}'")
    print(f"[{driver_name}] Waiting for messages. CTRL+C to stop.\n")

    def on_message(ch, method, properties, body):
        try:
            msg = json.loads(body)
        except json.JSONDecodeError:
            print(f"[{driver_name}] NACK (bad JSON) key={method.routing_key}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        # Part D3: reject messages that are missing the 'zone' field
        if "zone" not in msg:
            print(f"[{driver_name}] NACK (missing zone) "
                  f"key={method.routing_key}  id={msg.get('id','?')[:8]}")
            # requeue=False → message is discarded (or sent to DLX)
            # requeue=True  would loop forever for a "poison" message
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            return

        # Normal message: acknowledge it
        city  = msg.get("city", "?")
        zone  = msg.get("zone", "?")
        otype = msg.get("type", "?")
        mid   = msg.get("id", "?")[:8]
        ts    = msg.get("ts", "?")
        print(f"[{driver_name}] ACK  key={method.routing_key}  "
              f"city={city} zone={zone} type={otype} id={mid} ts={ts}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Turn on manual acknowledgements (auto_ack=False is the default)
    ch.basic_consume(queue=queue, on_message_callback=on_message, auto_ack=False)

    try:
        ch.start_consuming()
    except KeyboardInterrupt:
        print(f"\n[{driver_name}] Stopped.")
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python stream/driver.py <NAME> <PATTERN>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
