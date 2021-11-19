import json
from unittest import TestCase, mock, main

from news.crawler import Crawler
from news.news import News

class TestCrawler(TestCase):
    @mock.patch('news.uploader.Uploader.id_exists')
    def test_parse_json(self, mock_id_exists):
        with open('test/news_data.json', 'r') as f:
            news_json = json.loads(f.read())
        mock_id_exists.return_value = False
        crawler = Crawler(None, None, None)
        
        cnt = 0
        for content in crawler._parse_json(news_json, mock_id_exists):
            cnt += 1
            self.assertIsInstance(content, tuple)
        self.assertEqual(cnt, 10)

    @mock.patch('news.uploader.Uploader.id_exists')
    def test_parse_invalid_json(self, mock_id_exists):
        mock_id_exists.return_value = False
        crawler = Crawler(None, None, None)
        
        for content in crawler._parse_json({}, mock_id_exists):
            self.assertIsInstance(content, KeyError)
    
    @mock.patch('news.uploader.Uploader.id_exists')
    def test_id_exists_database(self, mock_id_exists):
        with open('test/news_data.json', 'r') as f:
            news_json = json.loads(f.read())

        mock_id_exists.return_value = True
        crawler = Crawler(None, None, None)

        for content in crawler._parse_json(news_json, mock_id_exists):
            self.assertIsInstance(content, str)

    @mock.patch('news.uploader.Uploader.id_exists')
    def test_id_not_exists_database(self, mock_id_exists):
        with open('test/news_data.json', 'r') as f:
            news_json = json.loads(f.read())

        mock_id_exists.return_value = False
        crawler = Crawler(None, None, None)

        cnt = 0
        for content in crawler._parse_json(news_json, mock_id_exists):
            cnt += 1
            self.assertIsInstance(content, tuple)
        self.assertEqual(cnt, 10)

    
if __name__ == '__main__':
    main()