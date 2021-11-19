import requests
import json

from video.video import Video


class Uploader():
    def __init__(self, ip: str, app_key: str) -> None:
        self.ip = ip
        self.app_key = app_key

    def put_video(self, video: Video) -> None:
        payload = json.dumps(video)
        response = requests.put(f'http://{self.ip}/api/v0/video',
                                headers={'Content-Type': 'application/json',
                                         'appKey': self.app_key},
                                data=payload)
        if response.status_code != 200:
            return False

    def delete_video(self, id: str) -> None:
        response = requests.delete(f'http://{self.ip}/api/v0/video?id={id}',
                                   headers={'appKey': self.app_key})

    def get_live_video(self) -> list:
        response = requests.get(f'http://{self.ip}/api/v0/video?viewState=live&limit=100')
        if response.status_code == 200:
            return response.json()
        return False

    def get_saved_video(self) -> list:
        response = requests.get(f'http://{self.ip}/api/v0/video?viewState=saved&limit=100')
        if response.status_code == 200:
            return response.json()
        return False


if __name__ == '__main__':
    video_saved = {'id': 'KDRwIRKP5tY',
                   'title': '【ON AIR】TVBS新聞 55 頻道 24 小時直播 | TVBS Taiwan News Live│台湾TVBS NEWS～世界中のニュースを24時 間配信中│대만 TVBS뉴스 24시간 생방송',
                   'imgUrl': 'https://i.ytimg.com/vi/LN1JzIdfMqY/mqdefault.jpg',
                   'videoUrl': 'https://www.youtube.com/watch?v=KDRwIRKP5tY',
                   'viewCount': 92104,
                   'viewState': 'saved',
                   'duration': '03:09',
                   'channel': None}
    channel = {'id': 'UC5nwNW4KdC0SzrhF9BXEYOQ',
               'name': 'TVBS NEWS',
               'imgUrl': 'https://yt3.ggpht.com/ytc/AKedOLTCGiM-wQo5lHpHr62WkOa_y1mezJzNPjpyjy-CVA=s88-c-k-c0x00ffffff-no-rj'}
    video_saved['channel'] = channel

    video_watch = {'id': 'RNcvyYuhIq4',
                   'title': '【ON AIR】TVBS新聞 55 頻道 24 小時直播 | TVBS Taiwan News Live│台湾TVBS NEWS～世界中のニュースを24時 間配信中│대만 TVBS뉴스 24시간 생방송',
                   'imgUrl': 'https://i.ytimg.com/vi/LN1JzIdfMqY/mqdefault.jpg',
                   'videoUrl': 'https://www.youtube.com/watch?v=RNcvyYuhIq4',
                   'viewCount': 92104,
                   'viewState': 'watching',
                   'duration': '03:09',
                   'channel': None}
    video_watch['channel'] = channel

    video_wait = {'id': 'acdFEYu2Ovc',
                  'title': '【ON AIR】TVBS新聞 55 頻道 24 小時直播 | TVBS Taiwan News Live│台湾TVBS NEWS～世界中のニュースを24時 間配信中│대만 TVBS뉴스 24시간 생방송',
                  'imgUrl': 'https://i.ytimg.com/vi/LN1JzIdfMqY/mqdefault.jpg',
                  'videoUrl': 'https://www.youtube.com/watch?v=acdFEYu2Ovc',
                  'viewCount': 92104,
                  'viewState': 'waiting',
                  'duration': '03:09',
                  'channel': None}
    video_wait['channel'] = channel

    uploader = Uploader("localhost:8081")

    uploader.put_video(video_saved)
    uploader.put_video(video_wait)
    uploader.put_video(video_watch)

    print(uploader.get_live_video())
