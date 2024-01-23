from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os
from dotenv import load_dotenv
import requests

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
# 웹드라이버 경로 설정 (예시: Chrome)
options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("--log-level=3")

def Search_Restaurant(input):
    Search_params = {
        "query": input,
        "display": 10,
        "start": 1,
        "sort": "comment"
    }
    Search_response = requests.get(urlserach, headers=headers, params=Search_params)
    data = Search_response.json()
    # RestaurantData = ''
    # for item in data['items']:
    #     RestaurantData += item['title'] + '/' + item['address'] + '/ mapx : ' + item['mapx'] + '/ mapy : ' + item['mapy'] +'\n'
    # return RestaurantData
    # 추출할 필드를 지정합니다.
    fields = ['title', 'address', 'mapx', 'mapy']

    # 필요한 정보를 추출하여 새로운 리스트에 저장합니다.
    extracted_data = []
    for item in data['items']:
        extracted_item = {field: item[field] for field in fields}
        extracted_data.append(extracted_item)
    return extracted_data

def Restaurant_Blog(restaurant_name):
    Blog_params = {
        "query": restaurant_name,
        "display": 5,
        "start": 1,
        "sort": "sim"
    }
    BLOG_response = requests.get(urlblog, headers=headers, params=Blog_params)
    data = BLOG_response.json()
    restaurant_blog = ''
    for item in data['items']:
        restaurant_blog += item['title'] + '/' + item['link'] + '\n'
    return restaurant_blog

def get_restaurant_url_selenium(keyword):
    # 네이버 플레이스 검색 URL
    data = pd.DataFrame(columns=['Restaurant_ID'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    search_url = f"https://map.naver.com/v5/search/{keyword}"
    # URL 열기
    driver.get(search_url)

    # 페이지 로드를 기다림
    wait = WebDriverWait(driver, 5)
    time.sleep(2)
    if parse.unquote(driver.current_url.split('?')[0].split('/')[-1]) == keyword:
        iframe = wait.until(EC.presence_of_element_located((By.ID, 'searchIframe')))
        driver.switch_to.frame(iframe)
        try :
            first_restaurant = driver.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.CHC5F > a')
        except NoSuchElementException:
            first_restaurant = driver.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.qbGlu > div.ouxiq > a:nth-child(1)')
        first_restaurant.click()
    Furl = driver.current_url.split('?')[0].split('/')[-1]
    driver.quit()
    data = get_restaurant_reviwes(Furl, keyword) + '\n'
    data += Restaurant_Blog(keyword)
    return data

def get_restaurant_reviwes(Furl, keyword):
    Reviewdata = ''
    getReviweDriver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    search_url = 'https://m.place.naver.com/restaurant/'+Furl+'/review/visitor?entry=ple'
    try:
        getReviweDriver.get(search_url)
        getReviweDriver.implicitly_wait(10)
        # Pagedown
        getReviweDriver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        time.sleep(2)
        html = getReviweDriver.page_source
        bs = BeautifulSoup(html, 'lxml')
        BillCounter = getReviweDriver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.k5tcc > h2 > span.place_section_count').text
        review = bs.select('li.YeINN')
        Reviewdata += "\n음식점 : " + keyword + "의 리뷰, 리뷰개수 : " + BillCounter +'\n'
        for r in review:
            nickname = r.select_one('div.VYGLG')
            content = r.select_one('div.ZZ4OK.IwhtZ')
            date = r.select('div._7kR3e>span.tzZTd>time')[0]
            revisit = r.select('div._7kR3e>span.tzZTd')[1]

            # exception handling
            nickname = nickname.text if nickname else ''
            content = content.text if content else ''
            date = date.text if date else ''
            revisit = revisit.text if revisit else ''
            Reviewdata += nickname + '/' + content + '/' + date + '/' + revisit + '\n'
        Reviewdata += '음식점 정보 링크 : '+ search_url + '\n'
    except Exception as e:
        print(e)
    getReviweDriver.quit()
    return Reviewdata
Search_Restaurant('맛집')