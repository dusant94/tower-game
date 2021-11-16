from aio_pika import channel
from aiohttp import web
import socketio
import aio_pika
import asyncio

mgr = socketio.AsyncAioPikaManager('amqp://guest:guest@127.0.0.1/')

sio = socketio.AsyncServer(cors_allowed_origins=['http://127.0.0.1:8001','http://127.0.0.1:666'],
                           client_manager=mgr)
app = web.Application()
sio.attach(app)


async def index(request):
    return web.Response(text="Pocus")
 

@sio.event
def connect(sid, environ):
    print("connect ", sid)

@sio.event
async def connected(sid, data):
    loop = asyncio.get_running_loop()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    routing_key = "connected"
    channel = await connection.channel()   
    await channel.default_exchange.publish(
        aio_pika.Message(
            body='{}'.format(data).encode()
        ),
        routing_key=routing_key
    )
    await connection.close()

@sio.event
async def defend(sid, data):
    print("message ", data)

@sio.event
async def attack(sid, data):
    loop = asyncio.get_running_loop()
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )
    routing_key = "attack " + data
    channel = await connection.channel()   
    await channel.default_exchange.publish(
        aio_pika.Message(
            body='{}'.format(data).encode()
        ),
        routing_key=routing_key
    )
    await connection.close()
    print("message ", data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


app.router.add_get('/', index)


 

if __name__ == '__main__':
    web.run_app(app, port=666)

    