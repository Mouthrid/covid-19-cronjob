import json
import requests
import re
from typing import Iterator, Optional

from bs4 import BeautifulSoup

from video import channel, video


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

    def get_content(self, url: str) -> Optional[Iterator[tuple]]:
        """Get the needed information for URL

        Get data from URL, and parse the content to extract needed information.

        Args:
            url: URL for get information, it need including page parameter.
            e.q. https://www.twreporter.org/tag/5e32b7b606a3d10600e11047?page={page}
        
        Returns:
            Video object generator
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.text, "html.parser")
        data = soup.find('script', text=re.compile(pattern=self.pattern))
        str_data = str(data)[len(self.prefix):-len(self.endwith)]
        json_data = json.loads(str_data)
        return self._parse_json(json_data)

    def _parse_json(self, json_data: dict) -> Optional[Iterator[tuple]]:
        """Parse the input json

        This function need to be design for extracting specific content.
        For other website, this function need to redesign.

        Args:
            json_data: json format data
            id_exists: check id exists in database or not
        
        Return:
            Video tuple generator, if all keys exist returns tuple 
            else returns False
        """
        try:
            header = json_data['header']['c4TabbedHeaderRenderer']
            channelId = header['channelId']
            title = header['title']
            avatar = header['avatar']['thumbnails'][1]['url']

            channel = (channelId, title, avatar)

            contents = json_data['contents']['twoColumnBrowseResultsRenderer']\
                            ['tabs'][0]['tabRenderer']['content']\
                            ['sectionListRenderer']['contents'][0]\
                            ['itemSectionRenderer']['contents']
            for content in contents:
                items = content['channelFeaturedContentRenderer'].get('items')
                if items:
                    try:
                        for item in items:
                            item = item['videoRenderer']
                            video_id = item['videoId']
                            title = item['title']['runs'][0]['text']
                            img_url = item['thumbnail']['thumbnails'][1]['url']
                            video_url = f'https://www.youtube.com/watch?v={video_id}'
                            view_count_text = item['viewCountText']['runs']
                            view_count = int(view_count_text[0]['text'].replace(',', ''))
                            view_state = view_count_text[1]['text']
                            if view_state in (' 人正在收看', ' 人が視聴中'):
                                view_state = 'watching'
                            elif view_state in (' 位觀眾等待中', ' 人が待機しています'):
                                view_state = 'waiting'
                            video = (video_id, title, img_url, video_url, view_count, 
                                     view_state)
                            yield channel, video
                    except KeyError as e:
                        raise e
        except KeyError as e:
            yield e


if __name__ == '__main__':
    url = 'https://www.youtube.com/channel/UC5nwNW4KdC0SzrhF9BXEYOQ'

    prefix = '<script nonce="JLYpkEzmSYBjienogfF9aA">var ytInitialData ='
    endwith = ';</script>'
    pattern = 'var ytInitialData'

    crawler = Crawler(prefix, endwith, pattern)

    cnt = 0
    for content in crawler.get_content(url):
        cnt += 1
    print(cnt)
    crawl_channel, crawl_video = content

    print(channel.Channel(*crawl_channel))
    print(video.Video(*crawl_video))
