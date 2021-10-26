import asyncio
import pikudhaoref


async def run(loop):
    async with pikudhaoref.AsyncClient(update_interval=2, loop=loop) as p:
        await p.initialize()
        # AsyncClient will do this automatically, but to make sure the city data is usable you should use it.

        print(await p.get_history())
        print(await p.current_sirens())


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
