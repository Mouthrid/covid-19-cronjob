# -*- coding: utf-8 -*-
import os
import logging
import json

from video.crawler import Crawler
from video.video import Video
from video.channel import Channel
from video.uploader import Uploader
from video.utils import get_video_duration


def main():
    urls = ('https://www.youtube.com/channel/UCyh91eTE9jA3ykg8W3_v3DQ',  # 衛服部
            'https://www.youtube.com/channel/UC8ROUUjHzEQm-ndb69CX8Ww',  # 台視新聞
            'https://www.youtube.com/channel/UCR3asjvr_WAaxwJYEDV_Bfw',  # 東森新聞
            'https://www.youtube.com/channel/UC5nwNW4KdC0SzrhF9BXEYOQ'   # TVBS
            )
    prefix = '<script nonce="JLYpkEzmSYBjienogfF9aA">var ytInitialData ='
    endwith = ';</script>'
    pattern = 'var ytInitialData'
    ip = f'{os.getenv("HOST_IP")}:8080'
    keywords = ('記者會', '說明')
    reject_words = ('氣象',)

    logging.basicConfig(format='[%(asctime)s][%(levelname)s] %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S')
    crawler = Crawler(prefix, endwith, pattern)
    uploader = Uploader(ip, os.getenv("APP_KEY"))

    for url in urls:
        for content in crawler.get_content(url):
            if isinstance(content, tuple):
                logging.info(f'POST {content}')
                channel, video = content
                video = Video(*video).to_dict()
                video['channel'] = Channel(*channel).to_dict()
                relative = any([key in video['title'] for key in keywords])
                reject = any([key in video['title'] for key in reject_words])
                if not relative or reject:
                    logging.warning(f"Irrelevant content {video['title']}")
                    continue
                state = uploader.put_video(video)
                assert state == None
            elif isinstance(content, KeyError):
                logging.error(f'KeyError: {content}')
            
    while True:
        live_videos = uploader.get_live_video()
        videos_info = [get_video_duration(video['id']) for video in live_videos]
        if videos_info.count(False) == len(live_videos):
            break
        for i, info in enumerate(videos_info):
            if isinstance(info, dict):
                live_video = live_videos[i]
                video = Video(**live_video)
                video.update_to_saved(**info)
                uploader.put_video(video.to_dict())
            elif isinstance(info, str):
                uploader.delete_video(info)


if __name__ == '__main__':
    main()
