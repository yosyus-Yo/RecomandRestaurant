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
    print(directions_data)
    if response.status_code == 200:
        if 'route' in directions_data:
            routes = directions_data['route']['traoptimal'][0]
                # 각 경로의 세부 정보 (예: 경로 설명, 총 거리, 총 소요 시간 등)
            summary = routes['summary']
                # 경로의 세부 구간 정보
            path_data = routes['path']
            return parse_important_info(summary), path_data
        else :
            return None, None
    else:
        return None, None
def parse_important_info(response_data):
    try:
        # 거리와 예상 소요 시간
        distance = response_data['distance']
        duration = response_data['duration']

        # 예상 택시 요금
        taxi_fare = response_data['taxiFare']

        return parse_and_format_info({
            "distance": distance,  # 미터 단위
            "duration": duration,  # 밀리초 단위
            "taxi_fare": taxi_fare  # 원 단위
        })
    except KeyError as e:
        return f"필요한 정보를 파싱하는 데 실패했습니다: {e}"

def parse_and_format_info(response_data):
    try:
        # 거리 (미터 단위)
        distance_m = response_data['distance']
        if distance_m >= 1000:
            distance = f"거리 : {distance_m / 1000:.2f}km\n"  # 킬로미터 단위로 변환
        else:
            distance = f"거리 : {distance_m}m\n"  # 미터 단위 유지

        # 소요 시간 (밀리초 단위)
        duration_ms = response_data['duration']
        duration_s = duration_ms // 1000  # 초 단위로 변환
        minutes, seconds = divmod(duration_s, 60)
        if minutes > 0:
            duration = f"소요 시간 : {minutes}분 {seconds}초\n"
        else:
            duration = f"소요 시간 : {seconds}초\n"
        taxi_fare_ = response_data['taxi_fare']
        taxi_fare = f"택시 가격 : {taxi_fare_}원"
        summary = distance + duration + taxi_fare
        print(summary)
        return summary
    except KeyError as e:
        return f"필요한 정보를 파싱하는 데 실패했습니다: {e}"
