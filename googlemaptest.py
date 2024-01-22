import googlemaps
from googlemaps.places import places_nearby
import requests
from dotenv import load_dotenv
import os

load_dotenv()

gmap_keys = os.getenv("GOOGLE_API_KEY")
UserPick = input("어디로 가시나요?")
gmaps = googlemaps.Client(key=gmap_keys)
tmp = gmaps.geocode(UserPick, language="ko")
print(tmp)
# userPickPlaceID = tmp[0]['place_id']

# url = "https://maps.googleapis.com/maps/api/place/details/json?place_id="+userPickPlaceID+"&fields=name%2Crating%2Cformatted_address%2Creviews&language=ko&key="+gmap_keys

# payload={}
# headers = {}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.json())