import asyncio

from fastapi import FastAPI
from proxybroker import Broker

app = FastAPI()
proxies = asyncio.Queue()
broker = Broker(proxies)


@app.post('/')
async def handler_find_new_proxies():
    task = asyncio.create_task(broker.find(types=['HTTPS'],
                                           limit=1000))
    await task


@app.get('/')
async def handler_get_proxy():
    proxy = proxies.get_nowait()
    proxy_data = {'host': proxy.host,
                  'port': proxy.port,
                  'types': proxy.types}
    return proxy_data


@app.get('/check')
async def handler_check_proxy_queue():
    return proxies.qsize()
