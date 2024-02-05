import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

client_id = os.getenv("NAVER_MAP_CLIENT_ID")
client_secret = os.getenv("NAVER_MAP_CLIENT_SECRET")

def reverse_geocode(lat, lng):
    url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": client_id,
        "X-NCP-APIGW-API-KEY": client_secret
    }
    params = {
        "coords": f"{lng},{lat}",
        "output": "json",
        "orders": "roadaddr"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return extract_road_address(json.loads(response.text))
    else:
        return None
def extract_road_address(response_data):
    try:
        # 'results' 배열의 첫 번째 요소에서 'land' 객체를 찾음
        land_info = response_data['results'][0]['land']
        region_info = response_data['results'][0]['region']

        # 도로명과 건물번호를 조합하여 주소 생성
        road_name = land_info['name']
        building_number = land_info['number1']
        road_address = f"{road_name} {building_number}"

        # 추가적으로 건물명이 있는 경우, 주소에 포함
        building_name = land_info['addition0']['value']
        if building_name:
            road_address += f", {building_name}"

        si_name = region_info['area1']['name']
        gu_name = region_info['area2']['name']
        dong_name = region_info['area3']['name']
        full_address = f"{si_name} {gu_name} {dong_name}, {road_address}"

        return full_address
    except KeyError:
        return "주소를 찾을 수 없습니다."
    except IndexError:
        return "주소를 찾을 수 없습니다."

