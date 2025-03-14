import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

#티커
#AAPL, MSFT, GOOGL, AMZN, FB, TSLA, NVDA, PYPL, ADBE, INTC, CSCO, NFLX, CMCSA, PEP, COST, TMUS, AVGO, TXN, QCOM, AMAT

# 티커(symbol) 설정
ticker = "INTC"
stock = yf.Ticker(ticker)

# 2년치 주식 데이터 가져오기
data = stock.history(period="2y")

# 20일, 50일, 120일 이동 평균 계산
data['20_MA'] = data['Close'].rolling(window=20).mean()
data['50_MA'] = data['Close'].rolling(window=50).mean()
data['120_MA'] = data['Close'].rolling(window=120).mean()

# 그래프 그리기
# plt.figure(figsize=(14, 7))
# plt.plot(data.index, data['Close'], label='Close Price')
# plt.plot(data.index, data['20_MA'], label='20 Day MA')
# plt.plot(data.index, data['50_MA'], label='50 Day MA')
# plt.plot(data.index, data['120_MA'], label='120 Day MA')

# plt.title(ticker + ' Moving Averages')
# plt.xlabel('Date')
# plt.ylabel('Price (USD)')
# plt.legend()
# plt.grid(True)
# plt.show()


# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# 주가와 이동 평균선 그래프
ax1.plot(data.index, data['Close'], label='Close Price')
ax1.plot(data.index, data['20_MA'], label='20 Day MA')
ax1.plot(data.index, data['50_MA'], label='50 Day MA')
ax1.plot(data.index, data['120_MA'], label='120 Day MA')
ax1.set_title(ticker + ' Moving Averages')
ax1.set_ylabel('Price (USD)')
ax1.legend()
ax1.grid(True)

# 거래량 그래프
ax2.bar(data.index, data['Volume'], color='gray')
ax2.set_ylabel('Volume')
ax2.set_xlabel('Date')
ax2.grid(True)

plt.show()