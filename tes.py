import requests
import json

client_id = "2xj7pkji00"
client_secret = "A7eNM0APAKyfGI44wUv8mISY9DNo0dqd9y0Q5RjU"
def get_directions(start, end):
    url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        "start": start,
        "goal": end
    }
    response = requests.get(url, headers=headers, params=params)
    directions_data = response.json()
    if response.status_code == 200:
        print("성공")
        if 'route' in directions_data:
            routes = directions_data['route']['traoptimal']
            for route in routes:
                # 각 경로의 세부 정보 (예: 경로 설명, 총 거리, 총 소요 시간 등)
                summary = route['summary']

                # 경로의 세부 구간 정보
                path_data = route['path']
                return summary, path_data
    else:
        return None