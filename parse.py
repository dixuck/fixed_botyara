import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime, timedelta

URL = 'https://kaktus.media/?lable=8'
wishnum = 20 # количество выводимых новостей

def get_description(url):

    response = requests.get(url)
    soup = BS(response.content, 'html.parser')
    return soup.find('p').text
    

def get_soup(url):
    response = requests.get(url)
    soup = BS(response.content, 'html.parser')
    news =  soup.find_all('div', {'class':'ArticleItem--data'})
    return news

def get_news(news, list_=[]):
    for new in news:
        if len(list_) < wishnum:
            title = new.find('a', {'class':'ArticleItem--name'}).text.strip()
            link = new.find('a', {'class':'ArticleItem--name'}).get('href')
            img = new.find('img', {'class': 'ArticleItem--image-img'}).get('src')
            list_.append((title, link, img))
    if len(list_) == wishnum:
        return list_
    else: 
        time = datetime.now()
        day = timedelta(days=1)
        today = time.date()
        news = get_soup(f'{URL}&date={today-day}')
        get_news(news, list_)
    return list_
                
def parsing():
    news = get_soup(URL)
    elements = get_news(news)
    return list(enumerate(elements,1))


news = parsing()
