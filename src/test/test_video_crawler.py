import json
from unittest import TestCase, main

from video.crawler import Crawler
from video.video import Video
from video.channel import Channel

class TestCrawler(TestCase):
    def test_parse_json(self):
        with open('test/video_data.json', 'r') as f:
            video_json = json.loads(f.read())
        crawler = Crawler(None, None, None)
        
        cnt = 0
        for content in crawler._parse_json(video_json):
            cnt += 1
            self.assertIsInstance(content, tuple)

    def test_parse_invalid_json(self):
        crawler = Crawler(None, None, None)
        
        for content in crawler._parse_json({}):
            self.assertIsInstance(content, KeyError)
    
    
if __name__ == '__main__':
    main()