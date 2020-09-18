import requests
from bs4 import BeautifulSoup

#상품 페이지 url 받아서 목록 csv 파일로 만들기

response = requests.get('http://drmartens.co.kr/items/mens-footwear')
soup = BeautifulSoup(response.text ,'html.parser')
# print(soup)

li_list = soup.select('body >  div.wrap > main.AppMain toNone > div.vue-body > div.ProductListContainer > div.ProductListContainer__body > div.layout__wrapper')

print(len(li_list))
# product_list = []

# for li in li_list:
#     a_tag = li.select_one('div > div.contents-column.left > h2 > a')
#     product_list.append(a_tag)

# print(product_list)

# response = requests.get('https://movie.naver.com/movie/running/current.nhn')
# soup = BeautifulSoup(response.text ,'html.parser')

# movies_list = soup.select('#content > div.article > div:nth-of-type > div.lst_wrap > ul > li')

# print(movies_list)