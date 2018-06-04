import argparse
from datetime import date, timedelta
import re

from habr_parser import fetch_raw_habr_feed, parse_raw_habr_page


def get_words_from_title(title_string):
    lower_letters_regex = re.compile('[^a-zа-я]')
    title_string = title_string.lower().strip()
    words = lower_letters_regex.sub(' ', title_string).split()
    return words


def group_articles_info_by_week(articles):
    weeks_info = dict()
    for article in articles:
        week_start = article['date'] - timedelta(days=article['date'].weekday())
        article_words = get_words_from_title(article['title'])
        if week_start not in weeks_info:
            weeks_info[week_start] = []
        weeks_info[week_start].extend(article_words)
    return weeks_info


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Some message', formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('--pages', type=int,
                        help='Number of pages to parse', default=10)
    parser.add_argument('--start', type=int,
                        help='Start page number', default=1)
    parser.add_argument('--min', type=int,
                        help='The minimum length of a word that gets into statistics', default=5)
    command_line_arguments = parser.parse_args()

    pages = command_line_arguments.pages
    start_page = command_line_arguments.start
    min_word_length = command_line_arguments.min

    raw_pages = fetch_raw_habr_feed(pages, start_page)
    print('Total pages parsed:', len(raw_pages))
    articles_info = []
    for raw_page in raw_pages:
        articles_info += parse_raw_habr_page(raw_page)
    articles_info_by_weeks = group_articles_info_by_week(articles_info)
    print('Total weeks parsed (may not fully):', len(articles_info_by_weeks))
    for week in articles_info_by_weeks:
        print(week, week + timedelta(days=6), articles_info_by_weeks[week])

