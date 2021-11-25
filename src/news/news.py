

class News():
    def __init__(self, id: str, title: str, news_time: str,
                 news_url: str, img_url: str, description: str) -> None:
        self.id = id
        self.title = title
        self.newsTime = news_time
        self.newsUrl = news_url
        self.imgUrl = img_url
        self.description = description
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    def __str__(self) -> str:
        return f'News({self.id}, {self.title}, {self.newsTime}, ' + \
            f'{self.newsUrl}, {self.imgUrl}, {self.description})'
