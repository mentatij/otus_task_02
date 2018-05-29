from habr_parser import fetch_raw_habr_feed, parse_raw_habr_page


if __name__ == '__main__':
    print('It is main habr_parser.py file!')
    raw_pages = fetch_raw_habr_feed()
    print(len(raw_pages))
    articles_info = []
    for raw_page in raw_pages:
        articles_info += parse_raw_habr_page(raw_page)
    for article in articles_info:
        print(article)
