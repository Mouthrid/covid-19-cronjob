import sys
from video.main import main as video
from news.main import main as news

if __name__ == '__main__':
    if sys.argv[1] == 'video':
        video()
    elif sys.argv[1] == 'news':
        news()
    else:
        print('wrong argument')