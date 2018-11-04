import re

from bs4 import BeautifulSoup

from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler


class PearVideo(Handler):
    SUPPORT_VERSION = 1
    NAME = '梨视频'

    @staticmethod
    def detect(url):
        return url.find('pearvideo.com') > -1

    @classmethod
    def handler(cls, url):
        html = abstract_grab(url)
        video_url_regex = 'srcUrl="(.*?)",'
        video_url = re.search(video_url_regex, html, flags=re.S).group(1)

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find('h1').get_text()
        cover = soup.find(id='poster').find('img').get('src')

        result = dict(
            default_url=video_url,
            more_options=[
                dict(
                    quality='default',
                    url=video_url,
                )
            ],
            video_info=dict(
                title=title,
                cover=cover,
            )
        )

        return Ret(result)
