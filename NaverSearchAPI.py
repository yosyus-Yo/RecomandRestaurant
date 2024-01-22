import requests
import os
from dotenv import load_dotenv
import pandas as pd
import urlscrap

load_dotenv()

# 클라이언트 아이디와 시크릿
client_id = os.getenv("NAVER_SEARCH_CLIENT_ID")
client_secret = os.getenv("NAVER_SEARCH_CLIENT_SECRET")

# API 요청 URL
urlserach = "https://openapi.naver.com/v1/search/local.json"
urlblog = "https://openapi.naver.com/v1/search/blog.json"

# HTTP 헤더
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# 쿼리 파라미터
def Search_Restaurant(input):
    Search_params = {
        "query": input,
        "display": 10,
        "start": 1,
        "sort": "comment"
    }
    Search_response = requests.get(urlserach, headers=headers, params=Search_params)
    data = Search_response.json()
    restaurant = pd.DataFrame(columns=['title', 'address'])
    for item in data['items']:
        restaurant.loc[len(restaurant)] = [item['title'], item['address']]
    # urlscrap.get_restaurant_url_selenium(restaurant['title'])
    for da in restaurant['title']:
        print(da)
    return restaurant

def Restaurant_Blog(restaurant_name):
    Blog_params = {
        "query": restaurant_name,
        "display": 10,
        "start": 1,
        "sort": "sim"
    }
    BLOG_response = requests.get(urlblog, headers=headers, params=Blog_params)
    data = BLOG_response.json()
    restaurant_blog = pd.DataFrame(columns=['title', 'link'])
    for item in data['items']:
        restaurant_blog.loc[len(restaurant_blog)] = [item['title'], item['link']]
    return restaurant_blog
input = input("어디로 가시나요?")
Search_Restaurant(input)    