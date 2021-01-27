import yfinance as yf
frame = yf.download("SPY", period = "5d", interval = "1m")
print(frame)

