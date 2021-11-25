import json
import requests
import re
from typing import Iterator, Optional, Callable

from bs4 import BeautifulSoup


class Crawler():
    def __init__(self, prefix: str, endwith: str, pattern: str) -> None:
        """A Tool for get website content

        Get the needed information from specific website.

        Public attributes:
        - prefix: the prefix string in the data to remove
        - endwith: the endwith string in the data to remove
        - pattern: the pattern for re library to search specific content
        - uploader: Uploader class for get or post data to database
        """
        self.prefix = prefix
        self.endwith = endwith
        self.pattern = pattern

    def get_content(self, url: str, id_exists: Callable = None) -> Optional[Iterator[tuple]]:
        """Get the needed information for URL

        Get data from URL, and parse the content to extract needed information.

        Args:
            url: URL for get information, it need including page parameter.
            e.q. https://www.twreporter.org/tag/5e32b7b606a3d10600e11047?page={page}
        
        Returns:
            News object generator
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        data = soup.find('script', text=re.compile(pattern=self.pattern))
        str_data = str(data)[len(self.prefix):-len(self.endwith)]
        json_data = json.loads(str_data)
        return self._parse_json(json_data, id_exists)
        
    def _parse_json(self, json_data: dict, id_exists: Callable) -> Optional[Iterator[tuple]]:
        """Parse the input json

        This function need to be design for extracting specific content.
        For other website, this function need to redesign.

        Args:
            json_data: json format data
            id_exists: check id exists in database or not
        
        Return:
            News tuple generator, if all keys exist returns tuple 
            else returns False
        """
        try:
            allIds = json_data['entities']['posts']['allIds']

            for id in allIds:
                if id_exists(id):
                    yield id
                else:
                    try:
                        news = json_data['entities']['posts']['byId'][id]
                        title = news['title']
                        news_time = news['published_date']
                        news_slug = news['slug']
                        news_url = f'https://www.twreporter.org/a/{news_slug}'
                        img_url = news['hero_image']['resized_targets']['tiny']['url']
                        description = news['og_description']

                        yield (id, title, news_time, news_url, img_url, description)
                    except KeyError as e:
                        raise e
        except KeyError as e:
            yield e
    

if __name__ == '__main__':
    url = 'https://www.twreporter.org/tag/5e32b7b606a3d10600e11047?page={page}'
    prefix = '<script charset="UTF-8">window.__REDUX_STATE__='
    endwith = ';</script>'
    pattern = 'window.__REDUX_STATE__='

    crawler = Crawler(prefix, endwith, pattern)

    cnt = 0
    for page in range(2):
        for content in crawler.get_content(url.format(page=page), lambda x: False):
            cnt += 1
            print(content)
    print(cnt)
