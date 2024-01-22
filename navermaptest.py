import requests
import os
from dotenv import load_dotenv
load_dotenv()

# 클라이언트 ID와 클라이언트 시크릿
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# API 요청 URL
url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

# 쿼리 파라미터
params = {
    "query": "분당구 불정로 6",
    "coordinate": "127.1054328,37.3595963"
}

# HTTP 헤더
headers = {
    "X-NCP-APIGW-API-KEY-ID": client_id,
    "X-NCP-APIGW-API-KEY": client_secret
}

# API 요청을 보내고 응답 받기
response = requests.get(url, headers=headers, params=params)

# 응답 출력
print(response.text)
