def stochastic_slow_k_trade_decision(slow_k):
    if slow_k < 20:
        return "BUY"
    elif slow_k > 80:
        return "SELL"


def sma_trade_decision(sma, today_price, open_price):
    if today_price > open_price:
        if sma > open_price:
            return "BUY"
    elif today_price < open_price:
        if sma < open_price:
            return "SELL"

