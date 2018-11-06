import re

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput


class Douyin(Handler):
    NAME = '抖音'

    @staticmethod
    def detect(url):
        return url.find('v.douyin.com') > -1

    @classmethod
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
            return Ret(Error.ERROR_HANDLER)

        result = HandlerOutput(
            video_info=HandlerOutput.VideoInfo(
                title=title,
                cover=cover,
            ),
            one_url=video_url,
        )
        return Ret(result.to_dict())
