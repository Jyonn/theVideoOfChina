import json
import re

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput


class XinPianChang(Handler):
    SUPPORT_VERSION = 1
    NAME = '新片场'

    RESOURCE_API = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource,resource_origin?'

    @staticmethod
    def detect(url):
        return url.find('xinpianchang.com') > -1

    @classmethod
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            vid_regex = 'vid: "(.*?)",'
            vid = re.search(vid_regex, html, flags=re.S).group(1)

            data = abstract_grab(cls.RESOURCE_API % vid)
            data = json.loads(data)['data']

            result = HandlerOutput(
                default_url=data['resource']['default']['https_url'],
                video_info=HandlerOutput.VideoInfo(
                    title=data['video']['title'],
                    cover=data['video']['cover'],
                ),
                only_default=False,
            )

            for item in data['resource']['progressive']:
                result.more_options.append(HandlerOutput.Option(
                    quality=item['profile'],
                    url=item['https_url'],
                ))
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER)

        return Ret(result.to_dict())
