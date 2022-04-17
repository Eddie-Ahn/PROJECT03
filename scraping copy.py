from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests


client = MongoClient('15.164.250.227', 27017, username="test", password="test")
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)

for i in range(10):  # 더보기 10번 버튼 찾아서 10번 클릭하기
    try:
        btn_more = driver.find_element_by_css_selector(
            "#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(5)
    # 더보기 버튼을 10번이나 할때 반약 더 누를게 안나올때는, element 가 없다고 오류가 뜰 것이고, 그 경우 멈추도록 try except 구문으로 break 해준다.
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one(
        "div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one(
        "div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one(
        "div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    print(title, address, category, show, episode)

    # 아래는 네이버 Geocoding 이용. Geocoding 은 주소를 인식하여 좌표로 돌려줌.
    headers = {
        "X-NCP-APIGW-API-KEY-ID": "49tdbelq95",  # Client ID 값 넣기
        "X-NCP-APIGW-API-KEY": "6q8ZkwZHgkQ286ou4rQvgZJLW4V61UVi9QgoI9Cr"  # Secret 키 넣기
    }
    r = requests.get(
        f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()

    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            # 그냥 [0]['x'] 면 문자열로 가져오니 소수 숫자로 인식해줄 float 형태로 변환 해줌.
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            print(title, address, category, show, episode, x, y)

            doc = {  #몽고 DB 에 저장하기
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y}
            db.matjips.insert_one(doc)
else:
    print(title, "좌표를 찾지 못했습니다")
