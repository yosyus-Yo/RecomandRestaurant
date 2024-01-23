from flask import Flask, render_template, jsonify, request
import urlscrap
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getMarkers', methods=['POST'])
def get_markers():
    data = request.json
    user_input = data['user_input']
    print(user_input)
    restaurant_data = urlscraping(user_input)
    print(restaurant_data)
    markers = [
        {
            "title": data['title'],
            "address": data['address'],
            "lng": convert_to_lat(data['mapx']),  # mapx 값을 위도로 변환
            "lat": convert_to_lng(data['mapy'])   # mapy 값을 경도로 변환
        }
        for data in restaurant_data
    ]
    print(markers)
    return jsonify(markers)
    # return jsonify(restaurant_data)

def urlscraping(user_input):
    return urlscrap.Search_Restaurant(user_input)
    # return [
    #     {"title": "음식점 1", "address": "서울특별시 강남구", "lat": 37.501, "lng": 127.0},
    #     {"title": "음식점 2", "address": "서울특별시 서초구", "lat": 37.502, "lng": 127.1},
    #     {"title": "음식점 3", "address": "서울특별시 송파구", "lat": 37.503, "lng": 127.2},
    #     {"title": "음식점 4", "address": "서울특별시 마포구", "lat": 37.504, "lng": 127.3}
    # ]

def convert_to_lat(mapx):
    # mapx 값을 위도로 변환하는 함수
    return float(mapx) / 10000000.0  # 예시 변환 로직

def convert_to_lng(mapy):
    # mapy 값을 경도로 변환하는 함수
    return float(mapy) / 10000000.0  # 예시 변환 로직
if __name__ == '__main__':
    app.run(debug=True)
