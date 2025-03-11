import asyncio

from src.module.upbit_websocket import upbit_ws_client
from src.module.util import set_loglevel

set_loglevel('I')
asyncio.run(upbit_ws_client())

