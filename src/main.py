import asyncio
import logging

from src.module.upbit_websocket import upbit_ws_client
from src.module.util import set_loglevel
from src.module.cal_indicator import CalIndicator
from src.module.trading_strategy import stochastic_slow_k_trade_decision, sma_trade_decision


queue = asyncio.Queue()


async def producer():
    async for data in upbit_ws_client():
        await queue.put(data)
        logging.info(f"📥 큐에 추가됨: {data}")

async def consumer(indicator_calculator):
    while True:
        data = await queue.get()
        if data["cd"] == "KRW-BTC":
            slow_k = indicator_calculator.cal_stochastic_slow('K', data["cd"], data["tp"], 20, 7)
            sma = indicator_calculator.cal_sma(data["cd"], data["tp"], 5)
            slow_k_decision = stochastic_slow_k_trade_decision(slow_k)
            sma_decision = sma_trade_decision(sma, data["tp"], data["op"])
            if slow_k_decision and sma_decision:
                if slow_k_decision == "BUY" and sma_decision == "BUY":
                    final_decision = "BUY"
                if slow_k_decision == "SELL" and sma_decision == "SELL":
                    final_decision = "SELL"
            logging.info(final_decision)
            logging.info(f"✅ 처리된 데이터: {data}")

        queue.task_done()


async def main():
    indicator_calculator = CalIndicator()
    producer_task = asyncio.create_task(producer())
    consumer_task = asyncio.create_task(consumer(indicator_calculator))

    await asyncio.gather(producer_task, consumer_task)


set_loglevel('I')
asyncio.run(main())

