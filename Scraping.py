from selenium.webdriver.common.by import By
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import requests
import urlscrap

def get_restaurant_reviwes(url):
    # url
    url = 'https://m.place.naver.com/restaurant/'+url+'/review/visitor?entry=ple'

    # Webdriver headless mode setting
    options = Options()
    options.add_argument('headless')

    # BS4 setting for secondary access
    session = requests.Session()
    headers = {
        "User-Agent": "user value"}

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    session.mount('http://', HTTPAdapter(max_retries=retries))
    # Start crawling/scraping!
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        res = driver.get(url)
        driver.implicitly_wait(30)

        # Pagedown
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

        time.sleep(5)
        html = driver.page_source
        bs = BeautifulSoup(html, 'lxml')
        try:
            rating = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.no_margin.mdJ86 > div > div > div.Xj_yJ > span.m7jAR.ohonc > em').text
            RatingCount = driver.find_element(By.CSS_SELECTOR, "#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.no_margin.mdJ86 > div > div > div.Xj_yJ > span:nth-child(2)").text
            print('식당 평균 별점 :', rating, RatingCount)
        except:
            pass
        BlogCounter = driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div:nth-child(2) > div.place_section.k5tcc > h2 > span.place_section_count').text
        print('영수증 리뷰 개수 :', BlogCounter)
        reviews = bs.select('li.YeINN')
        data = pd.DataFrame(columns=['nickname', 'content', 'date', 'revisit'])
        for r in reviews:
            nickname = r.select_one('div.VYGLG')
            content = r.select_one('div.ZZ4OK.IwhtZ')
            date = r.select('div._7kR3e>span.tzZTd>time')[0]
            revisit = r.select('div._7kR3e>span.tzZTd')[1]

            # exception handling
            nickname = nickname.text if nickname else ''
            content = content.text if content else ''
            date = date.text if date else ''
            revisit = revisit.text if revisit else ''
            data.loc[len(data)] = [nickname, content, date, revisit]
        print(data)
        return data

    except Exception as e:
        print(e)
