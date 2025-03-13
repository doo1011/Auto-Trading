import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.module.backtesting import Backtesting

# market_code = "BTC-KRW"
market_code = "KRW-BTC"

backtesting = Backtesting(market_code, "5-minute")

backtesting.prices.dropna(inplace=True)

backtesting.add_stochastic(20, 7, 3)
backtesting.add_sma(5)

fig = make_subplots(
    rows=4, cols=1, shared_xaxes=True,
    row_heights=[0.45, 0.2, 0.3, 0.05], vertical_spacing=0.05,
    subplot_titles=("Candlestick Chart", "Volume", "Stochastic Slow %K & %D", "")
)

fig.add_trace(go.Candlestick(x=backtesting.prices.index,
                             open=backtesting.prices["Open"],
                             high=backtesting.prices["High"],
                             low=backtesting.prices["Low"],
                             close=backtesting.prices["Close"],
                             name=f"{market_code} Candle Chart"),
              row=1,
              col=1)

backtesting.find_trading_point(fig)

fig.add_trace(go.Scatter(x=backtesting.prices.index,
                         y=backtesting.prices["SMA_5"],
                         mode="lines",
                         name="SMA 5",
                         line=dict(color="blue", width=1.5)),
              row=1,
              col=1)

fig.add_trace(go.Bar(x=backtesting.prices.index,
                     y=backtesting.prices["Volume"],
                     name="Volume",
                     marker=dict(color="gray"),
                     opacity=0.5),
              row=2,
              col=1)

fig.add_trace(go.Scatter(x=backtesting.prices.index,
                         y=backtesting.prices["Slow %K"],
                         mode="lines",
                         name="Slow %K",
                         line=dict(color="blue", width=1.5)),
              row=3,
              col=1)

fig.add_trace(go.Scatter(x=backtesting.prices.index,
                         y=backtesting.prices["Slow %D"],
                         mode="lines",
                         name="Slow %D",
                         line=dict(color="red", width=1.5, dash="dot")),
              row=3,
              col=1)

fig.add_trace(
    go.Scatter(
        x=[backtesting.prices.index[0], backtesting.prices.index[-1]],
        y=[20, 20],
        mode="lines",
        line=dict(color="lightblue", width=1, dash="dash"),
        name="20 Line"
    ),
    row=3, col=1
)
fig.add_trace(
    go.Scatter(
        x=[backtesting.prices.index[0], backtesting.prices.index[-1]],
        y=[80, 80],
        mode="lines",
        line=dict(color="lightcoral", width=1, dash="dash"),
        name="80 Line"
    ),
    row=3, col=1
)

fig.add_trace(
    go.Scatter(
        x=backtesting.prices.index, y=backtesting.prices['Close'], mode="lines", line=dict(color="gray", width=1),
        showlegend=False
    ),
    row=4, col=1
)

for i in range(3):
    fig.layout.annotations[i].font.color = "white"

fig.update_layout(
    xaxis=dict(
        showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    yaxis=dict(
        showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        title="Price", tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    xaxis2=dict(
        showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    yaxis2=dict(
        showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        title="Volume", tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    xaxis3=dict(
        title="Date", showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    yaxis3=dict(
        showgrid=True, gridcolor="gray", zeroline=False, showline=True, linecolor="white",
        title="Stochastic", tickfont=dict(color="white"), title_font=dict(color="white")
    ),
    legend=dict(font=dict(color="white")),  # 🔹 범례 글자색 변경
    plot_bgcolor="black",  # 서브플롯 배경색
    paper_bgcolor="rgb(20, 20, 20)",  # 전체 배경색
    title=dict(text=f"{market_code} Candlestick Chart with Volume & Stochastic", font=dict(size=18, color="white")),
    height=900  # 🔹 전체 차트 높이 증가
)

fig.update_layout(
    xaxis_rangeslider=dict(visible=False)
)

fig.show()


