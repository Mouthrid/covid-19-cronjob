from video.channel import Channel


class Video:
    def __init__(self, id: str, title: str, imgUrl: str,
                 videoUrl: str, viewCount: str, viewState: str,
                 channel: Channel = None, duration: str = '0',
                 videoTime: str = None) -> None:
        self.id = id
        self.title = title
        self.imgUrl = imgUrl
        self.videoUrl = videoUrl
        self.viewCount = viewCount
        self.viewState = viewState
        self.channel = channel
        self.duration = duration
        self.videoTime = videoTime

    def update_to_saved(self, title: str, videoTime: str, imgUrl: str, viewCount: int,
                        duration: str, viewState: str) -> None:
        self.title = title
        self.videoTime = videoTime
        self.imgUrl = imgUrl
        self.viewCount = viewCount
        self.duration = duration
        self.viewState = viewState

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self) -> str:
        return f'Video({self.id}, {self.title}, {self.imgUrl}, ' + \
               f'{self.videoUrl}, {self.viewCount}, {self.viewState}, ' + \
               f'{self.channel}, {self.duration}, {self.videoTime})'
