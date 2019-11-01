#!/usr/bin/env python
"""Module and script to parse pub-sub events and write them to Redis hashes."""
import json

import redis

from wikiutils import current_timestamp, pubsub_channel, redis_url

r = redis.Redis.from_url(redis_url)


def process():
    """Process messages from the pubsub stream."""
    ps = r.pubsub()
    ps.subscribe(pubsub_channel)
    for raw_message in ps.listen():
        if raw_message["type"] != "message":
            continue
        message = json.loads(raw_message["data"])
        process_message(message)


def process_message(message):
    """Process single decoded message."""
    domain = message["meta"]["domain"]
    ts = current_timestamp()
    keys = ["ev", f"ev:{domain}"]
    pipe = r.pipeline()
    for key in keys:
        pipe.hincrby(key, ts, 1)
    pipe.sadd("known_domains", domain)
    pipe.execute()


if __name__ == "__main__":
    process()
