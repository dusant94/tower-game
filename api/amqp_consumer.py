import asyncio
import aio_pika
from api import helpers
import json

async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    async with connection:
        queue_name = "connected"

        # Creating channel
        channel = await connection.channel()    # type: aio_pika.Channel

        # Declaring queue
        queue = await channel.declare_queue(
            queue_name,
            auto_delete=True
        )   # type: aio_pika.Queue

        async with queue.iterator() as queue_iter:
            # Cancel consuming after __aexit__
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    hocus, pocus = helpers.add_tower_points(int(message.body))
                    await publish_update(hocus, pocus)
                    if queue.name in message.body.decode():
                        break


async def publish_update(hocus, pocus):
    h = {
        "tower_healt": hocus.healt,
        "name": hocus.name
    }
    p = {
        "tower_healt": pocus.healt,
        "name": pocus.name
    }
    msg = {
        "hocus": h,
        "pocus": p 
    }
    msg = json.dumps(msg)
  
    loop = asyncio.get_running_loop()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )

    async with connection:
        routing_key = "tower_update"

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body="{}".format(msg).encode()),
            routing_key=routing_key,
        )


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()