import json
import redis.asyncio as redis

from typing import List, AsyncIterator
from core.utils.conf import CoreSettings

__REDIS_URL = CoreSettings().pubsub_url
__REDIS = redis.from_url(__REDIS_URL, decode_responses=True)


async def consume(channel_patterns: List[str]) -> AsyncIterator:
    async with __REDIS.pubsub() as pubsub:
        assert channel_patterns
        await pubsub.psubscribe(*channel_patterns)
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                payload = json.loads(message["data"])
                yield payload


async def publish(channel: str, payload: dict):
    await __REDIS.publish(channel, json.dumps(payload))
