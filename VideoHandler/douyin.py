import re

from SmartDjango import Packing

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class DouyinShort(Handler):
    NAME = '抖音短链接'

    @staticmethod
    def detect(url):
        return url.find('v.douyin.com') > -1

    @classmethod
    @Packing.pack
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            title_regex = '<p class="desc">(.*?)</p>'
            title = re.search(title_regex, html, flags=re.S).group(1)

            video_url_regex = 'playAddr: "(.*?)",'
            video_url = re.search(video_url_regex, html, flags=re.S).group(1)

            cover_regex = 'cover: "(.*?)"'
            cover = re.search(cover_regex, html, flags=re.S).group(1)
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


class DouyinLong(Handler):
    NAME = '抖音长链接'
    SUPPORT_VERSION = 2

    @staticmethod
    def detect(url):
        return url.find('iesdouyin.com') > -1

    @classmethod
    @Packing.pack
    def handler(cls, url):
        return DouyinShort.handler(url)
