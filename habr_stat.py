import argparse
import collections
from datetime import timedelta
import re

import pymorphy2

from habr_parser import fetch_raw_habr_feed, parse_raw_habr_page


def get_words_from_title(title_string):
    lower_letters_regex = re.compile('[^a-zа-я]')
    title_string = title_string.lower().strip()
    words = lower_letters_regex.sub(' ', title_string).split()
    return words


def group_articles_info_by_weeks(articles):
    weeks_info = dict()
    for article in articles:
        week_start = article['date'] - timedelta(days=article['date'].weekday())
        article_words = get_words_from_title(article['title'])
        if week_start not in weeks_info:
            weeks_info[week_start] = []
        weeks_info[week_start].extend(article_words)
    return weeks_info


def normalize_words(words_list):
    morph = pymorphy2.MorphAnalyzer()
    words_normal = []
    for word in words_list:
        word_parsing = morph.parse(word)[0]
        if 'NOUN' in word_parsing.tag or 'LATN' in word_parsing.tag:
            words_normal.append(word_parsing.normal_form)
    return words_normal


if __name__ == '__main__':

    # Parsing arguments of command line
    help_message = '''Habr Stats is tool for analyzing the frequency of using words in the main feed of habr.com'''
    parser = argparse.ArgumentParser(description=help_message, formatter_class=argparse.MetavarTypeHelpFormatter)
    parser.add_argument('--pages', type=int,
                        help='Number of pages to parse (10 by default)', default=10)
    parser.add_argument('--start', type=int,
                        help='Start page number (1 by default)', default=1)
    parser.add_argument('--min', type=int,
                        help='The minimum length of a word that gets into statistics (5 by default)', default=5)
    parser.add_argument('--top', type=int,
                        help='The quantity of  most popular words that gets into statistics (5 by default)', default=5)
    parser.add_argument('--url', type=str,
                        help='Url of feed to parse (http://habr.com/all/ by default)', default='http://habr.com/all/')
    command_line_arguments = parser.parse_args()

    pages = command_line_arguments.pages
    start_page = command_line_arguments.start
    min_word_len = command_line_arguments.min
    top = command_line_arguments.top
    url = command_line_arguments.url

    # Main program flow
    raw_pages = fetch_raw_habr_feed(pages, start_page, url)
    articles_info = []
    for raw_page in raw_pages:
        articles_info += parse_raw_habr_page(raw_page)
    articles_info_by_weeks = group_articles_info_by_weeks(articles_info)

    # Output
    print('Pages parsed:', len(raw_pages))
    print('Weeks parsed (may be not fully):', len(articles_info_by_weeks))
    print('-' * 100)
    print('Start of week | End of week | Top{} most popular words'.format(top))
    for week in articles_info_by_weeks:
        print('-' * 100)
        words_normal_form = [w for w in normalize_words(articles_info_by_weeks[week]) if len(w) >= min_word_len]
        words_collection = collections.Counter(words_normal_form).most_common(top)
        print('{0: ^14}|{1: ^13}| '.format(str(week), str(week + timedelta(days=6))), end='')
        for word in words_collection:
            print(word[0], end=' ')
        print('')
    print('-' * 100)
