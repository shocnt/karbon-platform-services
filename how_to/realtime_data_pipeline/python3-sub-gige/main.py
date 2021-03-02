import asyncio
import os
import signal
from nats.aio.client import Client as NATS
import datastream_pb2
import sys
import logging
import json
import base64

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)	

natsURL = "nats://nats:4222"
topic = os.environ['TOPIC']

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

    @asyncio.coroutine
    def subscribe_handler(msg):
        try:
            datastreamMsg = datastream_pb2.DataStreamMessage()
            datastreamMsg.ParseFromString(msg.data)
            json_raw = json.loads(datastreamMsg.payload[0].decode())
            image_frame_id = json_raw["image_frame_id"]
            image_height = json_raw["image_height"]
            image_width = json_raw["image_width"]
            image_ndim = json_raw["image_ndim"]
            logging.info("Frame# {}, Height {}, Width {}, Ndim {} Received!".format(
                image_frame_id,
                image_height,
                image_width,
                image_ndim))
            image_data = json_raw["image_data"]
            # Use cvImage_encoded for further processing.
            cvImage_encoded = base64.b64decode(image_data.encode())
        except Exception as exception:
            logging.info("Exception: {}".format(exception))

    yield from nc.subscribe(topic, cb=subscribe_handler)
    logging.info("Subscribed to topic: {}".format(topic))

    def signal_handler():
        if nc.is_closed:
            return
        logging.info("Disconnecting...")
        loop.create_task(nc.close())

    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), signal_handler)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    try:
        loop.run_forever()
    finally:
        loop.close()
