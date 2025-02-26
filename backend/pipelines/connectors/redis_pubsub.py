import redis
import time
from typing import List
from bytewax.inputs import FixedPartitionedSource, StatefulSourcePartition
from core.utils.conf import CoreSettings


class RedisPubSubPartition(StatefulSourcePartition):
    def __init__(self, redis_url: str, channel_patterns: List[str]):
        r = redis.from_url(redis_url)
        self.pubsub = r.pubsub(ignore_subscribe_messages=True)
        self.pubsub.psubscribe(channel_patterns)

    def next_batch(self, *args):
        message = self.pubsub.get_message()
        if message is None:
            # When there are no messages,
            # throttle down and poll only twice
            # per seconds
            time.sleep(0.5)
            return []
        data = message["data"]
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        return [data]

    def snapshot(self):
        return None

    def close(self):
        self.pubsub.close()


class RedisPubSubSource(FixedPartitionedSource):
    def __init__(self, channel_patterns: List[str]):
        self.redis_url = CoreSettings().pubsub_url
        self.channel_patterns = channel_patterns

    def list_parts(self):
        return ["single-part"]

    def build_part(self, now, for_key, resume_state):
        return RedisPubSubPartition(
            self.redis_url,
            self.channel_patterns,
        )
