import logging

import src.resources.config as cfg
from src.module.util import send_request


def get_items(market_codes, except_item):
    try:
        # 조회결과 리턴용
        rtn_list = list()

        # 마켓 데이터
        markets = market_codes.split(',')

        # 제외 데이터
        except_items = except_item.split(',')

        url = "/v1/market/all"
        querystring = {"isDetails": "false"}
        response = send_request("GET", cfg.UPBIT_URL + url, querystring, "")
        data = response.json()

        # 조회 마켓만 추출
        for data_for in data:
            for market_for in markets:
                if data_for["market"].split('-')[0] == market_for:
                    rtn_list.append(data_for)

        # 제외 종목 제거
        for rtnlist_for in rtn_list[:]:
            for exceptItemFor in except_items:
                for marketFor in markets:
                    if rtnlist_for["market"] == marketFor + '-' + exceptItemFor:
                        rtn_list.remove(rtnlist_for)

        return rtn_list

    except Exception as e:
        logging.error("Exception Raised In Getting Items!")
        logging.error(e)
        raise


def get_daily_candle_chart(market, to_date, data_count, currency):
    try:
        url = "/v1/candles/days"
        querystring = {
            "market": market,
            "to": to_date,
            "count": data_count,
            "converting_price_unit": currency
        }
        response = send_request("GET", cfg.UPBIT_URL + url, querystring, "")
        data = response.json()

        return data

    except Exception as e:
        logging.error("Exception Raised In Getting Candle Chart!")
        logging.error(e)
        raise


if __name__ == "__main__":
    import datetime

    now = datetime.datetime.now()
    print(now.strftime("%Y-%m-%d %H:%M:%S"))
    price = get_daily_candle_chart("KRW-BTC", now.strftime("%Y-%m-%d %H:%M:%S"), 100, "KRW")
    print(price)

