from bs4 import BeautifulSoup
import requests


def fetch_raw_habr_feed(pages=5, start_page=1):
    raw_pages = []
    for page_num in range(start_page, start_page+pages):
        raw_pages.append(_fetch_raw_habr_page(page_num))
    return raw_pages


def _fetch_raw_habr_page(page_num):
    url = 'http://habr.com/all/'
    if page_num:
        url += 'page{}/'.format(page_num)
    print(url)
    return requests.get(url).text


def parse_raw_habr_page(raw_page):
    articles_info = []
    soup = BeautifulSoup(raw_page, "html.parser")
    for article_block in soup.find_all('article', {'class': 'post_preview'}):
        article_date = article_block.find('span', {'class': 'post__time'})
        article_title = article_block.find('a', {'class': 'post__title_link'})
        articles_info.append({
            'date': article_date.contents[0],
            'title': article_title.contents[0],
        })
    return articles_info


