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

col1, col2, col3 = st.columns(3)

strongest_event = max(
    events_data,
    key=lambda x: abs(x["Reaction %"])
)

strongest_reaction = strongest_event["Reaction %"]

strongest_event = strongest_event["Event"]

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
# Event Summary Table
event_df = pd.DataFrame(events_data)

st.subheader("Event Summary")

st.dataframe(event_df)