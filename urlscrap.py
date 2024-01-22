from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib import parse
import pandas as pd
import Scraping
import time

def get_restaurant_url_selenium(keyword):
    # 웹드라이버 경로 설정 (예시: Chrome)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # 네이버 플레이스 검색 URL
    data = pd.DataFrame(columns=['Restaurant_ID'])
    for KW in keyword:
        search_url = f"https://map.naver.com/v5/search/{KW}"
        # URL 열기
        driver.get(search_url)

        # 페이지 로드를 기다림
        wait = WebDriverWait(driver, 5)
        time.sleep(1)
        if parse.unquote(driver.current_url.split('?')[0].split('/')[-1]) == KW:
            iframe = wait.until(EC.presence_of_element_located((By.ID, 'searchIframe')))
            driver.switch_to.frame(iframe)
            try :
                first_restaurant = driver.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.CHC5F > a')
            except NoSuchElementException:
                first_restaurant = driver.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:nth-child(1) > div.qbGlu > div.ouxiq > a:nth-child(1)')
            first_restaurant.click()
        Furl = driver.current_url.split('?')[0].split('/')[-1]
        print(Furl)
        data.loc[len(data)] = [Furl]
        # 드라이버 종료
    driver.quit()
    #Scraping.get_restaurant_reviwes(Furl)
    return data