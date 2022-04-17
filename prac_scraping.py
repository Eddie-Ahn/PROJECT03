from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep


driver = webdriver.Chrome('./chromedriver')

url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=%EC%95%84%EC%9D%B4%EC%9C%A0"
driver.get(url)
sleep(10)
driver.execute_script("window.scrollTo(0, 1000)")  # 네이버 이미지 검색 시 보이는 화면 만큼만 그림 정보를 가져오니 1000픽셀만큼 더 내려 보기. window 는 내가 보는창 .scrollTo 는 스크롤을 해줘라는 메서드, (0, 1000) 에서 0은 x좌표 이동. 좌우로는 0만큼 이동 1000은 y 좌표 이동. 1000 px만큼 내려서 이동해라. 
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # 맨 밑까지 스크롤 내리기
sleep(10)

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')
images = soup.select(".tile_item._item ._image._listImage")
print(len(images))

for image in images:
    src = image["src"]
    print(src)

