import asyncio
import pikudhaoref

loop = asyncio.get_event_loop()
client = pikudhaoref.AsyncClient(update_interval=2, loop=loop)


@client.event()
async def on_siren(sirens):
    print(sirens)


async def run():
    await client.initialize()
    # AsyncClient will do this automatically,
    # but to make sure the city data is usable immediately you should use it.

    print(await client.get_history())
    print(await client.current_sirens())


loop.run_until_complete(run())
loop.run_forever()
