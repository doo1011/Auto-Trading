import datetime
import time
from statistics import mean
import logging

from src.module.upbit_rest_api import get_items, get_daily_candle_chart


class CalIndicator:
    def __init__(self):
        self.prices = dict()
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        items = get_items("KRW", '')
        for i in items:
            prices = get_daily_candle_chart(i["market"], today, 200, "KRW")
            time.sleep(0.1)
            self.prices[i["market"]] = prices
            break

    def cal_stochastic_slow(self, stochastic_type, market_code, today_price:float, n, m, t=0):
        try:
            logging.info(f"{market_code} Cal Stochastic Slow %D")
            prices = [i["trade_price"] for i in self.prices[market_code]]
            prices.insert(0, today_price)
            fast_k_list = list()
            slow_k_list = list()

            for i in range(m + t):
                high = max(prices[i : i + n])
                low = min(prices[i : i + n])
                fast_k = (prices[i] - low) / (high - low) * 100
                fast_k_list.append(fast_k)

            if stochastic_type == 'K':
                return mean(fast_k_list[0:m])

            for i in range(t):
                slow_k = mean(fast_k_list[i : i + m])
                slow_k_list.append(slow_k)

            slow_d = mean(slow_k_list)

            return slow_d
        except Exception as e:
            logging.error("Exception Raised In Calculating Stochastic Slow %D!")
            logging.error(e)
            raise

    def cal_sma(self, market_code, today_price:float, n):
        try:
            logging.info(f"{market_code} Cal SMA")
            prices = [i["trade_price"] for i in self.prices[market_code]]
            prices.insert(0, today_price)
            return mean(prices[0 : n])
        except Exception as e:
            logging.error("Exception Raised In Calculating SMA!")
            logging.error(e)
            raise


if __name__ == "__main__":
    c = CalIndicator()
    slow = c.cal_stochastic_slow_d("KRW-BTC", 14, 3, 3, 120501000.0)
    sma = c.cal_sma("KRW-BTC", 5, 120501000.0)
    print("done")
