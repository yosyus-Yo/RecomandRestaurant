from flask import Flask, render_template, jsonify, request
import urlscrap
import Place
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sendMessage', methods=['POST'])
def send_message():
    message = request.json['message']
    response_message, restaurant_data = Place.startMessage(message)
    if restaurant_data != []:
        markers = [
        {
            "title": data['title'],
            "address": data['address'],
            "lng": convert_to_lat(data['mapx']),  # mapx 값을 위도로 변환
            "lat": convert_to_lng(data['mapy'])   # mapy 값을 경도로 변환
        }
        for data in restaurant_data
        ]
        return jsonify({"response": response_message, "markers": markers})
    return jsonify({"response": response_message})

def convert_to_lat(mapx):
    # mapx 값을 위도로 변환하는 함수
    return float(mapx) / 10000000.0  # 예시 변환 로직

def convert_to_lng(mapy):
    # mapy 값을 경도로 변환하는 함수
    return float(mapy) / 10000000.0  # 예시 변환 로직
if __name__ == '__main__':
    app.run(debug=True)
