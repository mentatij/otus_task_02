import argparse

from habr_parser import fetch_raw_habr_feed, parse_raw_habr_page


if __name__ == '__main__':
    # comandline_parser = argparse.ArgumentParser(description='Some message')
    # comandline_parser.add_argument('--pages', )
    print('It is main habr_parser.py file!')
    pages = 15
    start_page = 1
    raw_pages = fetch_raw_habr_feed(pages, start_page)
    print(len(raw_pages))
    articles_info = []
    for raw_page in raw_pages:
        articles_info += parse_raw_habr_page(raw_page)
    for article in articles_info:
        print(article)

    articles_info_grouped_by_weeks = group_articles_by_week(articles_info)
