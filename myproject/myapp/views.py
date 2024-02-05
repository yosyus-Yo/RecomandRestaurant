from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import UserInfo
from . Langchain import Output
import reverse_geocode
import tes

def submit_info(request):
    if request.method == "POST":
        name = request.POST.get('name')
        print(name)
        UserInfo.objects.create(name=name)
        return HttpResponse("정보가 성공적으로 제출되었습니다!")
    else:
        return render(request, "myapp/submit_info_form.html")
    
def chat_and_map(request):
    return render(request, 'myapp/chat_and_map.html')

def send_message(request):
    message = request.json['message']
    checkmarker = request.json['checkmarker']
    response_message, restaurant_data, flag = Output(message, checkmarker)
    if(flag == 3):
        return JsonResponse({"response": response_message , "checkmarker": restaurant_data})
    if restaurant_data != []:
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
    currentLocation = request.json['message']
    lat = currentLocation['y']
    lng = currentLocation['x']
    response = reverse_geocode.reverse_geocode(lat, lng)
    return JsonResponse({'response': response})

def findPath(request):
    start = request.json['start']
    end = request.json['end']
    summary, response = tes.get_directions(start, end)
    return JsonResponse({'response': response, 'summary' : summary})

def convert_to_lat(mapx):
    # mapx 값을 위도로 변환하는 함수
    return float(mapx) / 10000000.0  # 예시 변환 로직

def convert_to_lng(mapy):
    # mapy 값을 경도로 변환하는 함수
    return float(mapy) / 10000000.0  # 예시 변환 로직