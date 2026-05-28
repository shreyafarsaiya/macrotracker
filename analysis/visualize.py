import yfinance as yf
import plotly.graph_objects as go

# fetching data
def get_spy_data():
    data = yf.download("SPY", period="1mo", interval="1h")
    return data

df = get_spy_data()

print(df.shape)
print(df.head())
print(df["Close"].isna().sum())

# returns
df["Returns"] = df[("Close", "SPY")].pct_change()

# rolling volatility
df["Volatility"] = (
    df["Returns"]
    .rolling(window=10)
    .std()
)

# create a chart
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df.index,
        y=df[("Close", "SPY")],
        mode="lines",
        name="SPY Price"
    )
)

# macro events
events = [
    {"event": "CPI", "time": "2026-05-13 08:30", "color": "red"},
    {"event": "NFP", "time": "2026-05-02 08:30", "color": "yellow"},
    {"event": "FED", "time": "2026-05-07 14:00", "color": "green"},
]

# add vertical lines
for event in events:

    fig.add_vline(
        x=event["time"],
        line_width=2,
        line_dash="dash",
        line_color=event["color"]
    )

    fig.add_annotation(
        x=event["time"],
        y=max(df[("Close", "SPY")]),
        text=event["event"],
        showarrow=True,
        arrowhead=1
    )

# -------------------------
# reaction analytics
# -------------------------

print("===== EVENT REACTION ANALYSIS =====")

event_results = []

for event in events:

    # find nearest timestamp
    nearest_idx = df.index.get_indexer(
        [event["time"]],
        method="nearest"
    )[0]

    # price at event
    event_price = df[("Close", "SPY")].iloc[nearest_idx]

    # 3 candles later
    future_idx = nearest_idx + 3

    # avoid out-of-range error
    if future_idx < len(df):

        # future price
        future_price = df[("Close", "SPY")].iloc[future_idx]

        # movement
        move = future_price - event_price

        # percentage movement
        reaction_pct = (
            move / event_price
        ) * 100

        # store result
        event_results.append({
            "event": event["event"],
            "reaction": reaction_pct
        })

        # chart annotation
        fig.add_annotation(
            x=event["time"],
            y=event_price,
            text=f"{event['event']}<br>{reaction_pct:.2f}%",
            showarrow=True,
            arrowhead=2
        )

        # print event info
        print(f"\nEvent: {event['event']}")
        print(f"Price At Event: {event_price:.2f}")
        print(f"3H Later Price: {future_price:.2f}")
        print(f"Point Move: {move:.2f}")
        print(f"Reaction %: {reaction_pct:.2f}%")

# -------------------------
# STRONGEST EVENT ANALYSIS
# -------------------------

strongest_event = max(
    event_results,
    key=lambda x: abs(x["reaction"])
)

print("\n===== STRONGEST MARKET EVENT =====")

print(
    f"{strongest_event['event']} "
    f"had the strongest reaction: "
    f"{strongest_event['reaction']:.2f}%"
)

# layout
fig.update_layout(
    title="SPY 1-hour chart of 1-month periods.",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)

fig.show()

# -------------------------
# VOLATILITY CHART
# -------------------------

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
    title="SPY Rolling Volatility",
    xaxis_title="Time",
    yaxis_title="Volatility",
    template="plotly_dark"
)

vol_fig.show()