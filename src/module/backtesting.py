import plotly.graph_objects as go
import pandas as pd

from src.module.yfinance_api import get_all_price
from src.module.trading_strategy import stochastic_slow_k_trade_decision, sma_trade_decision


class Backtesting:
    def __init__(self, market_code):
        self.prices = get_all_price(market_code)

    def add_stochastic(self, n, m, t):
        self.prices["Low_N"] = self.prices["Low"].rolling(window=n).min()
        self.prices["High_N"] = self.prices["High"].rolling(window=n).max()
        self.prices["Fast %K"] = ((self.prices["Close"] - self.prices["Low_N"]) / (self.prices["High_N"] - self.prices["Low_N"])) * 100

        self.prices["Slow %K"] = self.prices["Fast %K"].rolling(window=m).mean()

        self.prices["Slow %D"] = self.prices["Slow %K"].rolling(window=t).mean()

    def add_sma(self, n):
        self.prices[f"SMA_{n}"] = self.prices["Close"].rolling(window=n).mean()

    def find_trading_point(self, figure):
        buy_info = None
        for i in self.prices.iterrows():
            slow_k_decision = stochastic_slow_k_trade_decision(i[1]['Slow %K'])
            sma_decision = sma_trade_decision(i[1]["SMA_5"], i[1]["Close"], i[1]["Open"])
            if slow_k_decision and sma_decision:
                if slow_k_decision == "BUY" and sma_decision == "BUY":
                    buy_info = i
                if slow_k_decision == "SELL" and sma_decision == "SELL":
                    if buy_info:
                        point1 = (buy_info[0], self.prices.loc[buy_info[0], "Close"])
                        point2 = (i[0], self.prices.loc[i[0], "Close"])

                        profit = round((point2[1] - point1[1]) / point1[1] * 100, 2)
                        figure.add_trace(go.Scatter(
                            x=[point1[0], point2[0]],
                            y=[point1[1], point2[1]],
                            mode="lines+markers",
                            line=dict(color="yellow", width=2, dash="dash"),
                            marker=dict(size=8, color="purple"),
                            name=f"{point1[0].strftime("%Y-%m-%d")} ~ {point2[0].strftime("%Y-%m-%d")} {profit}"
                        ))
                        figure.add_annotation(
                            x=pd.Timestamp(point1[0]) + (pd.Timestamp(point2[0]) - pd.Timestamp(point1[0])) / 2,  # 📍 중간 지점 (X 좌표)
                            y=(point1[1] + point2[1]) / 2,  # 📍 중간 지점 (Y 좌표)
                            text=profit,  # 🔹 중간에 추가할 텍스트
                            showarrow=False,
                            font=dict(color="white", size=12),  # 🔹 텍스트 스타일
                            bgcolor="black",  # 🔹 텍스트 배경색
                        )

                        buy_info = None





if __name__ == "__main__":
    b = Backtesting("BTC-KRW")
    b.add_stochastic(14, 3, 3)
    print("Done")
