import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://www.hindustantimes.com'
agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}



def get_response_text(url):
    response = requests.get(url,headers=agent)

    text = response.text
    
    return text

def get_top_news_links(html_response):
        soup = BeautifulSoup(html_response, 'html.parser')
        top_news_html = soup.find('div',{'id':'topnews'})
        top_news_links = []
        for div in top_news_html.find_all('div'):
            if div.get('data-weburl', None) is not None:
                top_news_links.append(div['data-weburl'])
        return top_news_links
    
def get_data_from_each_link(top_news_links):
    news_list = []
    for top_news_link in top_news_links:
        news_data = extract_data_link(top_news_link)
        if news_data is None:
            continue
        news_list.append(news_data)
    return news_list
        
    
    
def extract_data_link(link):
    try:
        response = requests.get(link,headers=agent)
        link_text_html = response.text
        soup = BeautifulSoup(link_text_html, 'html.parser')
        page_text = soup.find('div',{'class':'fullStory'})
        image = page_text.find('picture')
        image_link = image.find('img')['src']
        title = page_text.find('h1', {'class':'hdg1'})
        short_desc = page_text.find('h2', {'class': 'sortDec'})
        story_detail = page_text.find('div', {'class': 'detail'})
        story = ''
        for paragraph in story_detail.find_all('p'):
            story += paragraph.text + '\n'
        
        for paragraph in story_detail.find_all('li'):
            story += paragraph.text + '\n'
        
        story_dict = {'title' : title.text, 'short_desc' : short_desc.text, 'story_detail' : story, 'image_link' : image_link }
    except Exception as e:
        return None
    return story_dict
    
    
def scrapper(url=url):
    html_response = get_response_text(url)
    top_news_links = get_top_news_links(html_response)
    news_data = get_data_from_each_link(top_news_links)
    return news_data





