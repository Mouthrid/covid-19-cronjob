

class Channel():
    def __init__(self, id: str, name: str, img_url: str) -> None:
        self.id = id
        self.name = name
        self.imgUrl = img_url
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    def __str__(self) -> str:
        return f'Channel({self.id}, {self.name}, {self.imgUrl})'
