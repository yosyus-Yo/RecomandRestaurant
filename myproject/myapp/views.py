from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import UserInfo
from .Langchain import Output
from .reverse_geocode import reverse_geocode
from .tes import get_directions
import json

@csrf_exempt
def main_handler(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            action = data.get('action')
            print(action)
            if action == 'send_message':
                return send_message(request)
            elif action == 'currentMarking':
                return currentMarking(request)
            elif action == 'findPath':
                return findPath(request)
            else:
                return JsonResponse({'error': 'Invalid action'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == "GET":
        # GET 요청에 대해 chat_and_map.html 페이지를 렌더링합니다.
        return render(request, 'myapp/chat_and_map.html')

    # 비POST/GET 요청에 대한 처리
    return JsonResponse({'message': 'This endpoint only supports POST requests.'}, status=405)
    
def submit_info(request):
    if request.method == "POST":
        name = request.POST.get('name')
        print(name)
        UserInfo.objects.create(name=name)
        return HttpResponse("정보가 성공적으로 제출되었습니다!")
    else:
        return render(request, "myapp/submit_info_form.html")
    
def send_message(request):
    data = json.loads(request.body)
    message = data['message']
    response_message, restaurant_data, flag = Output(message)
    if(flag == 3):
        return JsonResponse({"response": response_message})
    if restaurant_data != None:
        markers = [
        {
            "title": data['title'],
            "address": data['address'],
            "lng": convert_to_lat(data['mapx']),  # mapx 값을 경도로 변환
            "lat": convert_to_lng(data['mapy'])   # mapy 값을 위도로 변환
        }
        for data in restaurant_data
        ]
        return JsonResponse({"response": response_message, "markers": markers})
    return JsonResponse({"response": response_message})

def currentMarking(request):
    data = json.loads(request.body)
    currentLocation = data['message']
    lat = currentLocation['y']
    lng = currentLocation['x']
    response = reverse_geocode(lat, lng)
    return JsonResponse({'response': response})

def findPath(request):
    data = json.loads(request.body)
    start = str(data['start']['Lng']) + ',' + str(data['start']['Lat'])
    end = str(data['end']['Lng']) + ',' + str(data['end']['Lat'])
    print(start, end)
    summary, response = get_directions(start, end)
    return JsonResponse({'response': response, 'summary' : summary})

def convert_to_lat(mapx):
    # mapx 값을 위도로 변환하는 함수
    return float(mapx) / 10000000.0  # 예시 변환 로직

def convert_to_lng(mapy):
    # mapy 값을 경도로 변환하는 함수
    return float(mapy) / 10000000.0  # 예시 변환 로직
