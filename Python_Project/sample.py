import requests

# API 키 (본인의 인증키 사용)
api_key = '+DQWruZ+EAFomv4OpkrPQEiW56UgnhvYExQNFgioOAh+ur6Py2Sl1CYj/Za8t/vPj7YEw3AKdLDBkTu7lKGltA=='


# 요청할 URL
url = 'http://apis.data.go.kr/1360000/NwpModelInfoService/getLdapsUnisAll'


# 요청 파라미터 설정 (예제 값)
params = {
    "ServiceKey": api_key,  # API 인증키
    "numOfRows": 10,        # 가져올 데이터 개수
    "pageNo": 1,            # 페이지 번호
    "dataType": "JSON",     # 데이터 형식 (JSON or XML)
    "baseTime": "202502080300",     # 기준 시간 (예: 0600 = 06:00 AM)
    "leadHour": "1",  # 기준 날짜 (YYYYMMDD)
    "dataTypeCd": "Temp"
}

# API 요청 보내기
response = requests.get(url, params=params)

# 응답 데이터 확인
if response.status_code == 200:
    data = response.json()  # JSON 응답을 파이썬 딕셔너리로 변환
    print(data)
    #print(response.content)
else:
    print(f"API 요청 실패: {response.status_code}")
