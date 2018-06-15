from datetime import date, timedelta

from bs4 import BeautifulSoup
import requests


def fetch_raw_habr_feed(pages=10, start_page=1):
    start_page_num = start_page if start_page < 100 else 100
    end_page_num = start_page + pages if (start_page + pages) < 100 else 100
    raw_pages = []
    for page_num in range(start_page_num, end_page_num + 1):
        raw_pages.append(_fetch_raw_habr_page(page_num))
    return raw_pages


def _fetch_raw_habr_page(page_num, url='http://habr.com/all/'):
    if page_num:
        url += 'page{}/'.format(page_num)
    return requests.get(url).text


def parse_raw_habr_page(raw_page):
    articles_info = []
    soup = BeautifulSoup(raw_page, "html.parser")
    for article_block in soup.find_all('article', {'class': 'post_preview'}):
        article_date = article_block.find('span', {'class': 'post__time'})
        article_title = article_block.find('a', {'class': 'post__title_link'})
        articles_info.append({
            'date': normalize_habr_date_v2(article_date.contents[0]),
            'title': article_title.contents[0],
        })
    return articles_info


def normalize_habr_date(habr_format_datetime_string):
    """Possible format examples: 'сегодня в 14:59', 'вчера в 21:23', '27 мая в 15:57', '14 февраля 2007 в 00:30"""
    date_list = habr_format_datetime_string.split()[:-2]  # real strange thing happens with ' ' in split argument
    months_ru_to_en = {'января': 1, 'февраля': 2, 'марта': 3,
                       'апреля': 4, 'мая': 5, 'июня': 6,
                       'июля': 7, 'августа': 8, 'сентября': 9,
                       'октября': 10,  'ноября': 11, 'декабря': 12}
    one_word_date = {'сегодня': date.today(),
                     'вчера': date.today() - timedelta(days=1)}
    if len(date_list) == 3:
        return date(int(date_list[2]), months_ru_to_en[date_list[1]], int(date_list[0]))
    elif len(date_list) == 2:
        return date(date.today().year, months_ru_to_en[date_list[1]], int(date_list[0]))
    elif len(date_list) == 1:
        return one_word_date[date_list[0]]
    else:
        print('Wrong date value')
        return None


def normalize_habr_date_v2(habr_format_datetime_string):
    """Possible format examples: 'сегодня в hh:mm', 'вчера в hh:mm', 'dd month_ru в hh:mm', 'dd month_ru yyyy в hh:mm"""
    date_list = habr_format_datetime_string.split()[:-2]  # real strange thing happens with ' ' in split argument
    if len(date_list) == 0:
        print('Wrong date value')
        return None
    months_ru_to_en = {'января': 1, 'февраля': 2, 'марта': 3,
                       'апреля': 4, 'мая': 5, 'июня': 6,
                       'июля': 7, 'августа': 8, 'сентября': 9,
                       'октября': 10,  'ноября': 11, 'декабря': 12}
    one_word_date = {'сегодня': date.today().day,
                     'вчера': date.today().day - 1}
    year = int(date_list[2]) if len(date_list) == 3 else date.today().year
    month = months_ru_to_en[date_list[1]] if len(date_list) >= 2 else date.today().month
    day = one_word_date[date_list[0]] if date_list[0].isalpha() else int(date_list[0])
    return date(year, month, day)
