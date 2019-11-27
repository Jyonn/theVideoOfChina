import json
import re

from Base.error import Error
from Base.grab import abstract_grab
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class ErGeng(Handler):
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
            )

            for quality in data:
                o = HandlerOutput.Option(urls=[], quality=quality)
                result.options.append(o)
                for seg in data[quality]:
                    o.urls.append(HandlerOutput.Url(
                        url=seg['url'],
                        index=seg['number'],
                    ))

        except Exception as err:
            raise Error.ERROR_HANDLER(debug_message=cls.NAME + '，' + str(err))

        return HandlerAdapter([result])
