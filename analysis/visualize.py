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

# layout
fig.update_layout(
    title="SPY 1-hour chart of 1-month periods.",
    xaxis_title="Time",
    yaxis_title="Price",
    template="plotly_dark"
)


fig.show()