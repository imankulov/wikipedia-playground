#!/usr/bin/env python
import asyncio as aio
import json

import aioredis
from aiohttp_sse_client import client as sse_client

from wikiutils import pubsub_channel, redis_url

wikimedia_stream = "https://stream.wikimedia.org/v2/stream/recentchange"


async def publish():
    redis = await aioredis.create_redis_pool(redis_url)
    while True:
        async with sse_client.EventSource(wikimedia_stream) as event_source:
            try:
                async for event in event_source:
                    json.loads(event.data)
                    await redis.publish(pubsub_channel, event.data)
            except (ConnectionError, aio.TimeoutError):
                pass


if __name__ == "__main__":
    aio.run(publish(), debug=True)
