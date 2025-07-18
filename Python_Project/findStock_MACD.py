import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys

# 티커(symbol) 설정
if len(sys.argv) > 1:
    ticker = sys.argv[1]
else:
    ticker = input("분석할 종목의 티커(symbol)를 입력하세요 (예: AAPL, TSLA, MSFT): ").upper()

try:
    # 데이터 다운로드 (6개월)
    df = yf.download(ticker, period="6mo")

    if df.empty:
        print("❌ 유효하지 않은 티커이거나 데이터가 없습니다. 다시 실행해 주세요.")
    else:
        # MACD 계산
        df["EMA_12"] = df["Close"].ewm(span=12, adjust=False).mean()  # 12일 EMA
        df["EMA_26"] = df["Close"].ewm(span=26, adjust=False).mean()  # 26일 EMA
        df["MACD"] = df["EMA_12"] - df["EMA_26"]  # MACD 라인
        df["Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()  # Signal 라인

        # 현재(마지막) MACD 및 Signal 값 출력
        latest_macd = df["MACD"].iloc[-1]
        latest_signal = df["Signal"].iloc[-1]
        latest_date = df.index[-1].strftime("%Y-%m-%d")

        print(f"\n📅 최신 데이터 ({latest_date}) - {ticker}")
        print(f"📊 MACD 값: {latest_macd:.2f}")
        print(f"📈 Signal 값: {latest_signal:.2f}")

        # 매수·매도 신호 찾기
        df["Buy_Signal"] = (df["MACD"] > df["Signal"]) & (df["MACD"].shift(1) <= df["Signal"].shift(1))
        df["Sell_Signal"] = (df["MACD"] < df["Signal"]) & (df["MACD"].shift(1) >= df["Signal"].shift(1))

        # 매수·매도 타이밍 저장
        buy_dates = df[df["Buy_Signal"]].index
        sell_dates = df[df["Sell_Signal"]].index

        #print(f"📈 매수 신호 발생일: {list(buy_dates)}")
        #print(f"📉 매도 신호 발생일: {list(sell_dates)}")

        # 그래프 시각화
        plt.figure(figsize=(12,6))
        plt.plot(df.index, df["MACD"], label="MACD", color="blue")
        plt.plot(df.index, df["Signal"], label="Signal", color="red", linestyle="dashed")
        plt.scatter(buy_dates, df.loc[buy_dates, "MACD"], marker="^", color="green", label="Buy Signal", alpha=1, s=100)
        plt.scatter(sell_dates, df.loc[sell_dates, "MACD"], marker="v", color="red", label="Sell Signal", alpha=1, s=100)

        # 매수·매도 신호를 그래프에 날짜와 함께 표시
        for date in buy_dates:
            close_price = float(df.loc[date, "Close"])
            plt.annotate(f'Buy\n{date.strftime("%Y-%m-%d")}\n{close_price:.2f}', 
                         (mdates.date2num(date), df.loc[date, "MACD"]), 
                         textcoords="offset points", xytext=(0,10), ha='center', color='green', fontsize=9, fontweight='bold')

        for date in sell_dates:
            close_price = float(df.loc[date, "Close"])
            plt.annotate(f'Sell\n{date.strftime("%Y-%m-%d")}\n{close_price:.2f}', 
                         (mdates.date2num(date), df.loc[date, "MACD"]), 
                         textcoords="offset points", xytext=(0,-20), ha='center', color='red', fontsize=9, fontweight='bold')

        # X축 날짜 포맷 설정
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
        plt.xticks(rotation=45)

        plt.legend()
        plt.title(f"{ticker} MACD Buy/Sell Signals")
        plt.grid()
        plt.show()

except Exception as e:
    print(f"❌ 오류 발생: {e}")
