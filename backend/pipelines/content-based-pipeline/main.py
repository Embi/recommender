import asyncio
from core.utils.asynchronous.pubsub import consume

__LOOP = asyncio.get_event_loop()


async def process_events():
    async for payload in consume(["interest:detail"]):
        print(payload)


if __name__ == "__main__":
    __LOOP.create_task(process_events())
    __LOOP.run_forever()
