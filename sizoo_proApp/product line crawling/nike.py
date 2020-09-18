import requests
from bs4 import BeautifulSoup

#상품 페이지 url 받아서 목록 csv 파일로 만들기

response = requests.get('https://www.nike.com/kr/ko_kr/w/men/fw')
soup = BeautifulSoup(response.text ,'html.parser')

nike = soup.select('body > section > section > section > article > div > div > ul > li')

print(nike)

#  > div > div.a-product-info.pt3-sm > div.product-display > div.product-info > p.product-display-name > span')