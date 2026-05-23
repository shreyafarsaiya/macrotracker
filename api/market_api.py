import yfinance as yf

def get_spy_data():
    spy = yf.download("SPY", period="5d", interval="5m")
    return spy

data = get_spy_data()

print(data.head())