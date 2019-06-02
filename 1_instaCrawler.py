#instagram crawler
#인스타 크롤러
from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome('/Users/rexypark/Desktop/chromedriver')
#가상으로 웹페이지 열기
browser.get('https://www.instagram.com/explore/tags/'+'크루즈여행/')

soup = bs(browser.page_source, 'html.parser')
print(soup)
urlWay = soup.select('div a')
print(urlWay[0]['href'])
#크루즈 여행 검색어에 대한 포스팅 url저장
cruise_url = []

#크루즈여행 전체 포스팅의 url 크롤링
for i in range(len(urlWay)):
    if urlWay[i]['href'][0:3] == '/p/':
        cruise_url.append(urlWay[i]['href'])
        print(urlWay[i]['href'])

#해시테그 크롤링
hashTags = []
for url in range(len(cruise_url)-30):
    browser = webdriver.Chrome('/Users/rexypark/Desktop/chromedriver')
    urls = 'https://www.instagram.com' + cruise_url[url]
    inputUrl = urls
    browser.get(inputUrl)
    
    soup = bs(browser.page_source, 'html.parser')
    hashTag = soup.select('span a')
    print(len(hashTag))
    c = 0
    for i in range(len(hashTag)):
        c = c+1
        if hashTag[i].text[0:1] == "#":
            hashTags.append(hashTag[i].text)
    browser.close()

#text파일로 해시태그 전체 저장
f = open("/Users/rexypark/Desktop/insta_all_hashtag.txt", 'w', encoding = 'utf8')
for i in hashTags:
    data = i + '\n'
    f.write(data)
f.close()
