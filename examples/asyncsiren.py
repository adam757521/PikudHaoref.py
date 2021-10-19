import asyncio
import pikudhaoref


async def run(loop):
    async with pikudhaoref.ASyncClient(update_interval=2, loop=loop) as p:
        print(await p.history())
        print(await p.current_sirens())


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))