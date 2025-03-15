import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# 분석할 종목 선택 (예: 애플)
ticker = "AAPL"

# 데이터 다운로드 (6개월)
df = yf.download(ticker, period="6mo")

# MACD 계산
df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()  # 12일 EMA
df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()  # 26일 EMA
df["MACD"] = df["EMA_12"] - df["EMA_26"]  # MACD 라인
df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()  # Signal 라인

# 매수·매도 신호 찾기
df["Buy_Signal"] = (df["MACD"] > df["Signal"]) & (df["MACD"].shift(1) <= df["Signal"].shift(1))
df["Sell_Signal"] = (df["MACD"] < df["Signal"]) & (df["MACD"].shift(1) >= df["Signal"].shift(1))

# 매수·매도 타이밍 출력
buy_dates = df[df["Buy_Signal"]].index
sell_dates = df[df["Sell_Signal"]].index

print(f"📈 매수 신호 발생일: {buy_dates}")
print(f"📉 매도 신호 발생일: {sell_dates}")

# 그래프 시각화
# plt.figure(figsize=(12,6))
# plt.plot(df.index, df["MACD"], label="MACD", color="blue")
# plt.plot(df.index, df["Signal"], label="Signal", color="red", linestyle="dashed")
# plt.scatter(buy_dates, df.loc[buy_dates, "MACD"], marker="^", color="green", label="Buy Signal", alpha=1, s=100)
# plt.scatter(sell_dates, df.loc[sell_dates, "MACD"], marker="v", color="red", label="Sell Signal", alpha=1, s=100)
# plt.legend()
# plt.title(f"{ticker} MACD 매매 신호")
# plt.show()

# 그래프 시각화
plt.figure(figsize=(12,6))
plt.plot(df.index, df["MACD"], label="MACD", color="blue")
plt.plot(df.index, df["Signal"], label="Signal", color="red", linestyle="dashed")
plt.scatter(buy_dates, df.loc[buy_dates, "MACD"], marker="^", color="green", label="Buy Signal", alpha=1, s=100)
plt.scatter(sell_dates, df.loc[sell_dates, "MACD"], marker="v", color="red", label="Sell Signal", alpha=1, s=100)

# # 매수 신호와 매도 신호 발생일을 그래프에 출력
for date in buy_dates:
    plt.annotate('Buy', (date, df.loc[date, "MACD"]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
for date in sell_dates:
    plt.annotate('Sell', (date, df.loc[date, "MACD"]), textcoords="offset points", xytext=(0,-15), ha='center', color='red')

plt.legend()
plt.title(f"{ticker} MACD Buy/Sell Signals")
plt.show()

# # 그래프 시각화
# plt.figure(figsize=(12,6))
# plt.plot(df.index, df["MACD"], label="MACD", color="blue")
# plt.plot(df.index, df["Signal"], label="Signal", color="red", linestyle="dashed")
# plt.scatter(buy_dates, df.loc[buy_dates, "MACD"], marker="^", color="green", label="Buy Signal", alpha=1, s=100)
# plt.scatter(sell_dates, df.loc[sell_dates, "MACD"], marker="v", color="red", label="Sell Signal", alpha=1, s=100)

# # 매수 신호와 매도 신호 발생일을 그래프에 출력
# for date in buy_dates:
#     plt.annotate(f'Buy\n{df.loc[date, "Close"]:.2f}', (date, df.loc[date, "MACD"]), textcoords="offset points", xytext=(0,10), ha='center', color='green')
# for date in sell_dates:
#     plt.annotate(f'Sell\n{df.loc[date, "Close"]:.2f}', (date, df.loc[date, "MACD"]), textcoords="offset points", xytext=(0,-15), ha='center', color='red')



# plt.legend()
# plt.title(f"{ticker} MACD 매매 신호")
# plt.show()