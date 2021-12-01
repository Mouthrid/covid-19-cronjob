import os
import logging

from news.crawler import Crawler
from news.news import News
from news.uploader import Uploader


def main():
    url = 'https://www.twreporter.org/tag/5e32b7b606a3d10600e11047?page={page}'
    prefix = '<script charset="UTF-8">window.__REDUX_STATE__='
    endwith = ';</script>'
    pattern = 'window.__REDUX_STATE__='
    ip = f'{os.getenv("HOST_IP")}:8080'

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
    logging.getLogger().setLevel(logging.INFO)

    crawler = Crawler(prefix, endwith, pattern)
    uploader = Uploader(ip, os.getenv("APP_KEY"))

    for page in range(1, 2):
        for content in crawler.get_content(url.format(page=page), uploader.id_exists):
            if isinstance(content, tuple):
                logging.info(f'POST: {content}')
                uploader.post_news(News(*content).to_dict())
            elif isinstance(content, str):
                logging.warning(f'ID: {content} is existing in database')
            elif isinstance(content, KeyError):
                logging.error(f'KeyError: {content}')


if __name__ == '__main__':
    main()
