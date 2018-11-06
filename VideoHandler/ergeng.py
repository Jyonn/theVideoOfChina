import json
import re

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput


class ErGeng(Handler):
    SUPPORT_VERSION = 1
    NAME = '二更视频'

    RESOURCE_API = 'https://member.ergengtv.com/api/video/vod/?id=%s'

    @staticmethod
    def detect(url):
        return url.find('ergengtv.com') > -1

    @classmethod
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            media_id_regex = '"media_id": (.*?),'
            media_id = re.search(media_id_regex, html, flags=re.S).group(1)

            title_regex = '"title": "(.*?)",'
            title = re.search(title_regex, html, flags=re.S).group(1)
            cover_regex = '"cover": "(.*?)",'
            cover = re.search(cover_regex, html, flags=re.S).group(1)

            data = abstract_grab(cls.RESOURCE_API % media_id)
            data = json.loads(data)['msg']['segs']

            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=title,
                    cover=cover,
                ),
                only_default=False,
            )

            for key in data:
                result.more_options.append(HandlerOutput.Option(
                    quality=key,
                    url=data[key][0]['url'],
                ))

            result.default_url = result.more_options[0].url
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER)

        return Ret(result.to_dict())
