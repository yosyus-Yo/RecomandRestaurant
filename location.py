import os
import requests
from dotenv import load_dotenv

load_dotenv(verbose=True)

google_api_key = os.getenv('GOOGLE_API_KEY')

url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={google_api_key}'
data = {
    'considerIp': True,
}

result = requests.post(url, data)

lat = result.json()['location']['lat']
lng = result.json()['location']['lng']

print(lat, lng)