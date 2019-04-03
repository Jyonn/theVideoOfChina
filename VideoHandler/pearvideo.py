import re

from SmartDjango import Packing
from bs4 import BeautifulSoup

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class PearVideo(Handler):
    NAME = '梨视频'

    @staticmethod
    def detect(url):
        return url.find('pearvideo.com') > -1

    @classmethod
    @Packing.pack
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            video_url_regex = 'srcUrl="(.*?)",'
            video_url = re.search(video_url_regex, html, flags=re.S).group(1)

            soup = BeautifulSoup(html, 'html.parser')

            title = soup.find('h1').get_text()
            cover = soup.find(id='poster').find('img').get('src')
        except Exception as err:
            deprint(str(err))
            return Error.ERROR_HANDLER('具体原因：' + cls.NAME + '，' + str(err))

        result = HandlerOutput(
            video_info=HandlerOutput.VideoInfo(
                title=title,
                cover=cover,
            ),
            one_url=video_url,
        )

        return HandlerAdapter([result])
