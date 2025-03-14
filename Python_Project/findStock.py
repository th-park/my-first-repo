import yfinance as yf
import pandas as pd

# 티커 목록 설정
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "PYPL", "ADBE", 
           "INTC", "CSCO", "NFLX", "CMCSA", "PEP", "COST", "TMUS", "AVGO", 
           "TXN", "QCOM", "AMAT",
           "ASML", "TSM", "ARM", "SMCI", "MU", "QCOM", "NXPI", "AMD", "LRCX",
           "NKE", "UPST", "SOFI", 
           "ABNB", "ORCL", "CRWD", "PLTR", "SNOW", "ZM", "DOCU", "FSLY", "NET",
           "ZETA", "UBER", "CRDO", "FLNC", "VST", "CLS"
           ]

# 현재 주가가 20일, 50일, 120일 이동 평균선을 뚫고 상승하는 주식을 찾기
for ticker in tickers:
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="2y")

        # 데이터가 충분한지 확인
        if len(data) < 120:
            print(f"{ticker}: 데이터가 충분하지 않습니다.")
            continue

        # 20일, 50일, 120일 이동 평균 계산
        data['20_MA'] = data['Close'].rolling(window=20).mean()
        data['50_MA'] = data['Close'].rolling(window=50).mean()
        data['120_MA'] = data['Close'].rolling(window=120).mean()

        # 현재 주가 가져오기
        current_price = data['Close'].iloc[-1]

        # 이동 평균 값이 NaN이 아닌지 확인
        if pd.isna(data['20_MA'].iloc[-1]) or pd.isna(data['50_MA'].iloc[-1]) or pd.isna(data['120_MA'].iloc[-1]):
            print(f"{ticker}: 이동 평균 값을 계산할 수 없습니다.")
            continue

        # 거래량 증가 확인 (현재 거래량이 20일 평균 거래량보다 큰지 확인)
        current_volume = data['Volume'].iloc[-1]
        avg_volume_20 = data['Volume'].rolling(window=20).mean().iloc[-1]


        # 현재 주가가 모든 이동 평균선 위에 있고 거래량이 증가했는지 확인
        if (current_price > data['20_MA'].iloc[-1] and 
            current_price > data['50_MA'].iloc[-1] and 
            current_price > data['120_MA'].iloc[-1] and 
            current_volume > avg_volume_20):
            print(f"{ticker}: 현재 주가 {current_price} USD가 20일, 50일, 120일 이동 평균선 위에 있으며 거래량이 증가했습니다.")
    except Exception as e:
        print(f"{ticker}: 데이터를 가져오는 중 오류 발생 - {e}")