import os
from unittest import TestCase, main

from video.utils import get_video_duration

class TestProcessor(TestCase):
    def test_invalid_youtube_api_key(self):
        id = 'KDRwIRKP5tY'
        response = get_video_duration(id)
        self.assertEqual(response, False)
    
    def test_live_video(self):
        id = 'KDRwIRKP5tY'
        response = get_video_duration(id)
        self.assertEqual(response, False)
    
    def test_saved_video(self):
        id = 'LN1JzIdfMqY'
        response = get_video_duration(id)
        self.assertIsInstance(response, dict)


if __name__ == '__main__':
    main()