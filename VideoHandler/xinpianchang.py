import json
import re

from Base.error import Error
from Base.grab import abstract_grab
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class XinPianChang(Handler):
    NAME = '新片场'

    RESOURCE_API = 'https://openapi-vtom.vmovier.com/v3/video/%s?expand=resource&usage=xpc_web&appKey=%s'

    @staticmethod
    def detect(url):
        return url.find('xinpianchang.com') > -1

    @classmethod
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            vid_regex = 'var vid = "(.*?)";'
            vid = re.search(vid_regex, html, flags=re.S).group(1)
            app_key_regex = 'var modeServerAppKey = "(.*?)";'
            app_key = re.search(app_key_regex, html, flags=re.S).group(1)

            data = abstract_grab(cls.RESOURCE_API % (vid, app_key))
            data = json.loads(data)['data']

            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=data['video']['title'],
                    cover=data['video']['cover'],
                ),
            )

            for item in data['resource']['progressive']:
                result.options.append(HandlerOutput.Option(
                    quality=item['profile'],
                    urls=[HandlerOutput.Url(item['https_url'])],
                ))
        except Exception as err:
            raise Error.ERROR_HANDLER(debug_message=cls.NAME + '，' + str(err))

        return HandlerAdapter([result])
