import json
import re

from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler


class ErGeng(Handler):
    SUPPORT_VERSION = 1
    NAME = '二更视频'

    RESOURCE_API = 'https://member.ergengtv.com/api/video/vod/?id=%s'

    @staticmethod
    def detect(url):
        return url.find('ergengtv.com') > -1

    @classmethod
    def handler(cls, url):
        html = abstract_grab(url)
        media_id_regex = '"media_id": (.*?),'
        media_id = re.search(media_id_regex, html, flags=re.S).group(1)

        title_regex = '"title": "(.*?)",'
        title = re.search(title_regex, html, flags=re.S).group(1)
        cover_regex = '"cover": "(.*?)",'
        cover = re.search(cover_regex, html, flags=re.S).group(1)

        data = abstract_grab(cls.RESOURCE_API % media_id)
        data = json.loads(data)['msg']['segs']

        result = dict(
            more_options=[],
            video_info=dict(
                title=title,
                cover=cover,
            )
        )

        for key in data:
            result['more_options'].append(dict(
                quality=key,
                url=data[key][0]['url'],
            ))

        result['default_url'] = result['more_options'][0]['url']

        return Ret(result)
