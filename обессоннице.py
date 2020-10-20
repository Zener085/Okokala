# Not important
import requests
from bs4 import BeautifulSoup as BS

html_code = requests.get('http://xn--90aialyadc0aa3d.xn--p1ai/articles/7-vidov/').text

soup = BS(html_code, 'lxml')

wrapper = soup.find('div', {'class': 'wrapper'})
article = wrapper.find('div', {'class': 'article-wrapper'})
container = article.find('div', {'class': 'article-container'})

print(container.text)
