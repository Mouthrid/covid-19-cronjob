import requests
import json

from news.news import News


class Uploader():
    def __init__(self, ip, app_key) -> None:
        self.ip = ip
        self.app_key = app_key
        self.error = 0

    def post_news(self, news: News) -> None:
        payload = json.dumps(news)
        response = requests.post(f'http://{self.ip}/api/v0/news',
                                 headers={'Content-Type': 'application/json',
                                          'appKey': self.app_key},
                                 data=payload)
        if response.status_code != 200:
            self.error += 1

    def id_exists(self, id: str) -> bool:
        response = requests.get(f'http://{self.ip}/api/v0/news?id={id}')
        if response.status_code == 200:
            return response.json()['state']
        return False


if __name__ == '__main__':
    news = {'id': '60eac28f59bfdf0600b1cc02',
    'title': '急診室醫師的COVID-19戰記：「因為弱小，所以強大」',
    'newsTime': '2021-07-16T16:00:00Z',
    'newsUrl': 'https://www.twreporter.org/a/bookreview-emergency-doctors-frontline-battles-against-covid-19',
    'imgUrl': 'https://www.twreporter.org/images/20210712163555-db46e65073913c5fd1c51a6dbcbdb642-mobile.jpg',
    'description': '急診科醫師「胖鳥」在《這裡沒有英雄》書中，笑中帶淚記錄COVID-19來襲時，站在台灣醫療前線的見聞：「台灣第一例歸國確診，如同一聲槍響⋯⋯醫院鳴笛決定：我們決戰戶外。這一鳴，最苦了的是護理師，那一刻，我終於知道他們為什麼叫天使。」'}

    uploader = Uploader("localhost:8081")

    print(uploader.id_exists("1L"))
    print(uploader.id_exists(None))

    uploader.post_news(news)
    uploader.post_news(news)