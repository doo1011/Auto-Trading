import asyncio
import websockets
import logging
import json
import time
import datetime
import ssl
import certifi

import src.resources.config as cfg
from src.module.util import set_loglevel
from src.module.upbit_rest_api import get_items

ssl_context = ssl.create_default_context(cafile=certifi.where())


def get_subscribe_items():
    try:
        subscribe_items = list()

        # KRW 마켓 전 종목 추출
        items = get_items("KRW", '')

        # 종목코드 배열로 변환
        for item in items:
            subscribe_items.append(item["market"])

        return subscribe_items

    except Exception as e:
        logging.error("Exception Raised In Getting Subscribe Items!")
        logging.error(e)
        raise


async def upbit_ws_client():
    try:
        # 중복 실행 방지용
        seconds = 0

        # 구독 데이터 조회
        subscribe_items = get_subscribe_items()

        logging.info("구독 종목 개수 : " + str(len(subscribe_items)))
        logging.info("구독 종목 : " + str(subscribe_items))

        # 구독 데이터 조립
        subscribe_fmt = [
            {"ticket": "test-websocket"},
            {
                "type": "ticker",
                "codes": subscribe_items,
                "isOnlyRealtime": True
            },
            {"format": "SIMPLE"}
        ]

        subscribe_data = json.dumps(subscribe_fmt)

        async with websockets.connect(cfg.UPBIT_WS, ssl=ssl_context) as ws:

            await ws.send(subscribe_data)

            async for message in ws:
                period = datetime.datetime.now()

                data = json.loads(message)

                # 5초마다 종목 정보 재 조회 후 추가된 종목이 있으면 웹소켓 다시 시작
                if (period.second % 5) == 0 and seconds != period.second:
                    # 중복 실행 방지
                    seconds = period.second

                    # 종목 재조회
                    re_subscribe_items = get_subscribe_items()
                    logging.info("\n\n")
                    logging.info("*************************************************")
                    logging.info("기존 종목[" + str(len(subscribe_items)) + "] : " + str(subscribe_items))
                    logging.info("종목 재조회[' + str(len(re_subscribe_items)) + '] : " + str(re_subscribe_items))
                    logging.info("*************************************************")
                    logging.info("\n\n")

                    # 현재 종목과 다르면 웹소켓 다시 시작
                    if subscribe_items != re_subscribe_items:
                        logging.info("종목 달리짐! 웹소켓 다시 시작")
                        await ws.close()
                        time.sleep(1)
                        await upbit_ws_client()

                yield data

    except Exception as e:
        logging.error("Exception Raised In Websocket Client!")
        logging.error(e)
        logging.error("Connect Again!")

        # 웹소켓 다시 시작
        await upbit_ws_client()


if __name__ == "__main__":
    set_loglevel('I')
    asyncio.run(upbit_ws_client())
