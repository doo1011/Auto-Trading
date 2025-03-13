import yfinance as yf


# 날짜 오름차순
def get_all_price(market_code):
    ticker = yf.Ticker(market_code)
    prices = ticker.history(interval="1d", period="max")

    return prices


if __name__ == "__main__":
    get_all_price("BTC-KRW")
