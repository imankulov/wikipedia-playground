#!/usr/bin/env python
import json

import redis

from wikiutils import current_timestamp, pubsub_channel, redis_url

r = redis.Redis.from_url(redis_url)


EXPIRATION_TIMEOUT_SEC = 3600


def process():
    ps = r.pubsub()
    ps.subscribe(pubsub_channel)
    for raw_message in ps.listen():
        if raw_message["type"] != "message":
            continue
        message = json.loads(raw_message["data"])
        process_message(message)


def process_message(message):
    domain = message["meta"]["domain"]
    ts = current_timestamp()
    keys = [f"ev:{ts}", f"ev:{domain}:{ts}"]
    pipe = r.pipeline()
    for key in keys:
        pipe.incr(key)
        pipe.expire(key, 3600)
    pipe.sadd("known_domains", domain)
    pipe.execute()


if __name__ == "__main__":
    process()
