import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# page title
st.title("Macro Event Tracker")

# fetch data
ticker = st.sidebar.selectbox(
    "Select Asset",
    ["SPY", "QQQ", "DIA"]
)

df = yf.download(
    ticker,
    period="1mo",
    interval="1h"
)

df["MA10"] = (
    df[("Close", ticker)]
    .rolling(window=10)
    .mean()
)



df["MA30"] = (
    df[("Close", ticker)]
    .rolling(window=30)
    .mean()
)

# MA Crossover Signal
df["Signal"] = 0

df.loc[
    df["MA10"] > df["MA30"],
    "Signal"
] = 1

df.loc[
    df["MA10"] < df["MA30"],
    "Signal"
] = -1

# detect position
df["Position"] = df["Signal"].diff()

# Buy signals
buy_signals = df[df["Position"] == 2]

# Sell signals
sell_signals = df[df["Position"] == -2]

buy_count = len(buy_signals)

sell_count = len(sell_signals)

total_trades = buy_count + sell_count


# returns
df["Returns"] = df[("Close", ticker)].pct_change()

# rolling volatility
df["Volatility"] = (
    df["Returns"]
    .rolling(window=10)
    .std()
)

# create chart
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df[("Close", ticker)],
        mode="lines",
        name=f"{ticker} Price"
    )
)


fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA10"],
        mode="lines",
        name="10H Moving Average"
    )
)

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["MA30"],
        mode="lines",
        name="30H Moving Average"
    )
)

# buy markers
fig.add_trace(
    go.Scatter(
        x=buy_signals.index,
        y=buy_signals[("Close", ticker)],
        mode="markers",
        name="BUY",
        marker=dict(
            size=12,
            color="green",
            symbol="triangle-up"
        )
    )
)

#sell markers
fig.add_trace(
    go.Scatter(
        x=sell_signals.index,
        y=sell_signals[("Close", ticker)],
        mode="markers",
        name="SELL",
        marker=dict(
            size=12,
            color="red",
            symbol="triangle-down"
        )
    )
)

# chart layout
fig.update_layout(
    title=f"{ticker} Market Chart",
    template="plotly_dark"
)

# show chart in dashboard
st.plotly_chart(fig)

events_data = [
    {"Event": "CPI", "Reaction %": 0.58},
    {"Event": "NFP", "Reaction %": -0.51},
    {"Event": "FED", "Reaction %": 0.88}
]

st.subheader("Market Insights")

col1, col2, col3, col4 = st.columns(4)

strongest_event = max(
    events_data,
    key=lambda x: abs(x["Reaction %"])
)

strongest_reaction = strongest_event["Reaction %"]

strongest_event = strongest_event["Event"]

current_price = df[("Close", ticker)].iloc[-1]

# Performance Statistics

start_price = df[("Close", ticker)].iloc[0]

highest_price = df[("Close", ticker)].max()

lowest_price = df[("Close", ticker)].min()

average_price = df[("Close", ticker)].mean()

monthly_return = (
    (current_price - start_price)
    / start_price
) * 100


current_ma = df["MA10"].iloc[-1]

current_ma30 = df["MA30"].iloc[-1]

if current_ma > current_ma30:
    crossover_signal = "Bullish 🚀"
else:
    crossover_signal = "Bearish 📉"

if current_ma > current_ma30:
    recommendation = "BUY 🟢"
    reason = "MA10 is above MA30"
else:
    recommendation = "SELL 🔴"
    reason = "MA10 is below MA30"


distance_pct = (
    (current_price - current_ma)
    / current_ma
) * 100



if current_price > current_ma:
    trend = "Bullish"
else:
    trend = "Bearish"

if strongest_reaction > 0:
    market_direction = "Bullish"
else:
    market_direction = "Bearish"

with col1:
    st.metric(
        "Strongest Event",
        strongest_event
    )

with col2:
    st.metric(
        "Strongest Reaction (%)",
        f"{strongest_reaction:.2f}"
    )

with col3:
    st.metric(
        "Market Direction",
        market_direction
    )

with col4:
    st.metric(
        "Trend vs MA10",
        trend
    )
col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(
        "Current Price",
        f"{current_price:.2f}"
    )

with col6:
    st.metric(
        "MA10",
        f"{current_ma:.2f}"
    )

with col7:
    st.metric(
        "Distance %",
        f"{distance_pct:.2f}%"
    )

with col8:
    st.metric(
        "MA Crossover",
        crossover_signal
    )


st.subheader("Performance Statistics")

col9, col10, col11, col12 = st.columns(4)

with col9:
    st.metric(
        "Highest Price",
        f"{highest_price:.2f}"
    )

with col10:
    st.metric(
        "Lowest Price",
        f"{lowest_price:.2f}"
    )

with col11:
    st.metric(
        "Average Price",
        f"{average_price:.2f}"
    )

with col12:
    st.metric(
        "Monthly Return %",
        f"{monthly_return:.2f}%"
    )

st.subheader("Signal Summary")

col13, col14, col15 = st.columns(3)

with col13:
    st.metric(
        "Buy Signals",
        buy_count
    )

with col14:
    st.metric(
        "Sell Signals",
        sell_count
    )

with col15:
    st.metric(
        "Current Signal",
        crossover_signal
    )
st.subheader("Strategy Performance")

col16, col17, col18 = st.columns(3)

with col16:
    st.metric(
        "Total Trades",
        total_trades
    )

with col17:
    st.metric(
        "Buy Signals",
        buy_count
    )

with col18:
    st.metric(
        "Sell Signals",
        sell_count
    )
st.subheader("Trading Recommendation")

col19, col20 = st.columns(2)

with col19:
    st.metric(
        "Recommendation",
        recommendation
    )

with col20:
    st.write("**Reason**")
    st.write(reason)


#download button
st.subheader("Download Data")

csv = df.to_csv().encode("utf-8")

st.download_button(
    label="📥 Download Market Data",
    data=csv,
    file_name=f"{ticker}_market_data.csv",
    mime="text/csv"
)


# Event Summary Table
event_df = pd.DataFrame(events_data)

st.subheader("Event Summary")

st.dataframe(event_df)

st.subheader("Volatility Chart")

vol_fig = go.Figure()

vol_fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df["Volatility"],
        mode="lines",
        name="Volatility"
    )
)

vol_fig.update_layout(
    title=f"{ticker} Rolling Volatility",
    template="plotly_dark"
)

st.plotly_chart(vol_fig)