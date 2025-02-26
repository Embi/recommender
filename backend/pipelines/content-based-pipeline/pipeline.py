import json
import numpy as np

from typing import List, Any
from typing_extensions import override
from bytewax import operators as op
from bytewax.dataflow import Dataflow
from bytewax.outputs import DynamicSink, StatelessSinkPartition
from core.db.models.user import get_user_by_id
from core.db.models.listing import get_listing_by_id
from core.db.session import get_session

from pipelines.connectors.redis_pubsub import RedisPubSubSource

INPUT = RedisPubSubSource(["interest:detail"])


def deserialize(payload):
    try:
        data = json.loads(payload)
    except json.decoder.JSONDecodeError:
        return None
    return data


class DevNullPartition(StatelessSinkPartition[Any]):
    @override
    def write_batch(self, items: List[dict]) -> None:
        pass


class DevNullSink(DynamicSink[Any]):
    @override
    def build(
        self, _step_id: str, _worker_index: int, _worker_count: int
    ) -> DevNullPartition:
        return DevNullPartition()


def __update_preference(
    user_preference: np.ndarray, listing_features: np.ndarray
) -> np.ndarray:
    # This is a super naive placeholder
    user_preference = (user_preference + listing_features) / 2
    return user_preference


def process_user_activity(user_activity: dict):
    with get_session() as session:
        user = get_user_by_id(user_activity["user"], session)
        listing = get_listing_by_id(user_activity["listing"], session)
        user.preference = __update_preference(
            user.preference, listing.features
        )
        print(f"Updated preference for user {user.email}")
        session.add(user)
    return user_activity


def get_flow() -> Dataflow:
    flow = Dataflow("content-based-pipeline")
    inp = op.input("inp", flow, INPUT)
    deserialized = op.map("deserialize", inp, deserialize)
    processed = op.map("process_activity", deserialized, process_user_activity)
    op.inspect("processed:", processed)
    op.output("devnull", processed, DevNullSink())
    return flow
