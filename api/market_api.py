import yfinance as yf

def get_spy_data():
    spy = yf.download("SPY", period="1mo", interval="1h")
    return spy

data = get_spy_data()

print(data.head())