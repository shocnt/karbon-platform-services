import asyncio
import os
import signal
from nats.aio.client import Client as NATS
import sys
import logging
from datetime import datetime, timezone, timedelta
import time
import json
import random

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

natsURL = "nats://nats:4222"
topic = os.environ['TOPIC']

JST = timezone(timedelta(hours=+9), 'JST')

def run(loop):
    nc = NATS()

    @asyncio.coroutine
    def closed_cb():
        logging.info("Connection to NATS is closed.")
        yield from asyncio.sleep(0.1, loop=loop)
        loop.stop()

    options = {
        "servers": [natsURL],
        "io_loop": loop,
        "closed_cb": closed_cb
    }

    yield from nc.connect(**options)
    logging.info("Connected to NATS at {}...".format(nc.connected_url.netloc))

    def signal_handler():
        if nc.is_closed:
            return
        logging.info("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)

    while(True):
        dt = datetime.now(JST)
        timestamp = dt.strftime("%Y-%m-%d %H:%M:%S:%f")
        status = str(random.randint(0,1))
        msg = json.dumps({"timestamp": timestamp, "status": status}) 

        logging.info("Publishing to NATS topic: {}".format(topic))
        logging.info("Publishing msg: {}".format(msg.encode()))

        yield from nc.publish(topic, msg.encode())
        yield from nc.flush()
        time.sleep(10)

    yield from nc.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(loop))
    finally:
        loop.close()
