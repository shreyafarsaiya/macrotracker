import yfinance as yf
import plotly.graph_objects as go

#fetching data
def get_spy_data():
    data = yf.download("SPY", period="1mo", interval="1h")
    return data

df = get_spy_data()

print(df.shape)
print(df.head())
print(df["Close"].isna().sum())

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
# layout
fig.update_layout(
    title="SPY 1-hour chart of 1-month periods.",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)


fig.show()