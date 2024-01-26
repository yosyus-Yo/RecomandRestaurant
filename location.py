import requests

def get_location_from_google_api():
    url = "https://www.googleapis.com/geolocation/v1/geolocate?key=AIzaSyAMeDcOmec29TuZTF27Mzmpfl8OiIrgUCA"
    data = {
        "considerIp": "true",  # IP 주소를 고려하여 위치 추정
        # 여기에 추가적인 파라미터를 넣을 수 있습니다 (예: Wi-Fi 액세스 포인트 정보 등)
    }
    response = requests.post(url, json=data)
    return response.json()

location = get_location_from_google_api()
print(location)
