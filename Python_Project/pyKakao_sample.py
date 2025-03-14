import yfinance as yf
import time
from PyKakao import Message


# 티커(symbol) 설정
ticker = "NVDA"  # 삼성전자 (한국 주식은 .KQ 또는 .KS 사용)
stock = yf.Ticker(ticker)


# 초기 주식 가격 가져오기
initial_price = stock.history(period="1d")["Close"].iloc[-1]

# 현재 주식 가격 가져오기
current_price = stock.history(period="1d")["Close"].iloc[-1]
#print(f"현재 가격: ${current_price} USD")
print(ticker + ": " + str(current_price) + " USD")



######################################################################################
# 메시지 API 인스턴스 생성
MSG = Message(service_key = "d27a569424104e56816b6ed9f872abe2")

# 카카오 인증코드 발급 URL 생성
auth_url = MSG.get_url_for_generating_code()
print(auth_url)

# 카카오 인증코드 발급 URL 접속 후 리다이렉트된 URL
#https://accounts.kakao.com/login?continue=https%3A%2F%2Fkauth.kakao.com%2Foauth%2Fauthorize%3Fresponse_type%3Dcode%26redirect_uri%3Dhttps%253A%252F%252Flocalhost%253A5000%26client_id%3Dd27a569424104e56816b6ed9f872abe2%26scope%3Dtalk_message%26through_account%3Dtrue
url = "https://localhost:5000/?code=zNku847D_Xjf3GAc14WXwVJb6BgPiTq-bSI2YyfBDTgsJhBKcVMkAQAAAAQKPXNOAAABlUyfxoui-KZYUq23DA"

#https://localhost:5000/?code=N3OigidpdKJo3-42B6UQ1gepMY_gIakyp49EGgo6x0k4qnhDNsK2XAAAAAQKKcleAAABlQeBl2-xu3fh8M0xkQ
#https://localhost:5000/?code=pZD8rNjaL3W34DBYsCTEY49691qDPgr5fd8kPMSb4MvUELbGFNGdFAAAAAQKKiVTAAABlO_-v-_E017PSiBv1Q

# 위 URL로 액세스 토큰 추출
access_token = MSG.get_access_token_by_redirected_url(url)

# 액세스 토큰 설정
MSG.set_access_token(access_token)

# 가격 변동률 설정
threshold = 0.03  # 3%

target_price = 133  # 목표 가격 설정

while True:
    price = stock.history(period="1d")["Close"].iloc[-1]
    print(f"현재 가격: {price} USD")

    if price > target_price:
        print("🎉 목표 가격 도달! 알람 발송 🎉")
        
        # 1. 나에게 보내기 API - 텍스트 메시지 보내기 예시
        message_type = "text" # 메시지 유형 - 텍스트
        text = f"{ticker}: {price} USD" # 전송할 텍스트 메시지 내용
        link = {
          "web_url": "https://developers.kakao.com",
          "mobile_web_url": "https://developers.kakao.com",
        }
        button_title = "바로 확인" # 버튼 타이틀

        MSG.send_message_to_me(
            message_type=message_type, 
            text=text,
            link=link,
            button_title=button_title,
        )
        break  # 반복문 종료

    price_change = (price - initial_price) / initial_price
    if abs(price_change) >= threshold:
        print("📈 가격 변동 알림 발송 📉")
        
        # 메시지 내용 설정
        message_type = "text"
        text = f"{ticker}: {current_price} USD\n변동률: {price_change * 100:.2f}%"
        link = {
            "web_url": "https://finance.yahoo.com/quote/NVDA",
            "mobile_web_url": "https://finance.yahoo.com/quote/NVDA",
        }
        button_title = "주식 확인"

        MSG.send_message_to_me(
            message_type=message_type,
            text=text,
            link=link,
            button_title=button_title,
        )
        break  # 반복문 종료    

    time.sleep(600)  # 10초마다 확인

# # 1. 나에게 보내기 API - 텍스트 메시지 보내기 예시
# message_type = "text" # 메시지 유형 - 텍스트
# text = "텍스트 영역입니다. 최대 200자 표시 가능합니다." # 전송할 텍스트 메시지 내용
# link = {
#   "web_url": "https://developers.kakao.com",
#   "mobile_web_url": "https://developers.kakao.com",
# }
# button_title = "바로 확인" # 버튼 타이틀

# MSG.send_message_to_me(
#     message_type=message_type, 
#     text=text,
#     link=link,
#     button_title=button_title,
# )

# 2. 친구에게 보내기 API - 텍스트 메시지 보내기 예시 (친구의 UUID 필요)
# message_type = "text" # 메시지 유형 - 텍스트
# receiver_uuids = [] # 메시지 수신자 UUID 목록
# text = "텍스트 영역입니다. 최대 200자 표시 가능합니다." # 전송할 텍스트 메시지 내용
# link = {
#   "web_url": "https://developers.kakao.com",
#   "mobile_web_url": "https://developers.kakao.com",
# }
# button_title = "바로 확인" # 버튼 타이틀

# MSG.send_message_to_friend(
#     message_type=message_type, 
#     receiver_uuids=receiver_uuids,
#     text=text,
#     link=link,
#     button_title=button_title,
# )
