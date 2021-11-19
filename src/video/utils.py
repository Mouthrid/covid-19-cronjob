import os
import re
import requests


def get_video_duration(id):
    youtube_url = 'https://www.googleapis.com/youtube/v3/videos?' + \
                    f'part=statistics,contentDetails,snippet&id={id}&key={os.getenv("youtube_api_key")}'
    response = requests.get(youtube_url)
    try:
        if response.status_code == 200:
            json_data = response.json()
            item = json_data['items'][0]
            title = item['snippet']['title']
            video_time = item['snippet']['publishedAt']
            img_url = f'https://i.ytimg.com/vi/{id}/mqdefault.jpg'
            view_count = item['statistics']['viewCount']
            duration_str = item['contentDetails']['duration']
            if duration_str == 'P0D':
                return False
            time_list = ['00', '00', '00']
            hour = re.findall(r'(\d+)H',duration_str)
            time_list[0] = hour[0] if hour else '00'
            minute = re.findall(r'(\d+)M',duration_str)
            time_list[1] = minute[0] if minute else '00'
            second = re.findall(r'(\d+)S',duration_str)
            time_list[2] = second[0] if second else '00'
            duration = [f'{int(t):02d}' for t in time_list]
            duration = ':'.join(duration)
            return {'title': title, 'videoTime': video_time, 'imgUrl': img_url,
                    'viewCount': view_count, 'duration': duration, 'viewState': 'saved'}
        return False
    except IndexError as e:
        return id
    

if __name__ == '__main__':
    import json
    from video.uploader import Uploader
    from video.video import Video

    # GET the data are not 'saved' from database
    db_video = ('KDRwIRKP5tY', 
     '【ON AIR】TVBS新聞 55 頻道 24 小時直播 | TVBS Taiwan News Live│台湾TVBS NEWS～世界中のニュースを24時 間配信中│대만 TVBS뉴스 24시간 생방송',
     'https://i.ytimg.com/vi/KDRwIRKP5tY/hqdefault_live.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLDxOh24AVRHhc5HXQEaFFhX7DELyA',
     'https://www.youtube.com/watch?v=KDRwIRKP5tY',
     '30697',
     'watching')

    video = Video(*db_video)

    channel = {'id': 'UC5nwNW4KdC0SzrhF9BXEYOQ',
    'name': 'TVBS NEWS',
    'imgUrl': 'https://yt3.ggpht.com/ytc/AKedOLTCGiM-wQo5lHpHr62WkOa_y1mezJzNPjpyjy-CVA=s88-c-k-c0x00ffffff-no-rj'}

    uploader = Uploader("localhost:8080", os.getenv('APP_KEY'))

    id = 'KDRwIRKP5tY'
    print(get_video_duration(id))

    id = 'LN1JzIdfMqY'
    print(get_video_duration(id))

    print(video)
    video.update_to_saved(**get_video_duration(id))
    print(video)
    video = video.to_dict()
    video['channel'] = channel
    response = uploader.put_video(video)