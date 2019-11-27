import json
from urllib import parse

from Base.error import Error
from Base.grab import abstract_grab
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class EyePetizer(Handler):
    SUPPORT_VERSION = 2
    NAME = '开眼'

    INFO_API_URL = 'http://baobab.kaiyanapp.com/api/v1/video/%s?f=web'

    @staticmethod
    def detect(url):
        o = parse.urlparse(url)
        qs = parse.parse_qs(o.query)
        return 'eyepetizer.net' in o.netloc and 'vid' in qs

    @classmethod
    def handler(cls, url):
        try:
            o = parse.urlparse(url)
            qs = parse.parse_qs(o.query)
            vid = qs['vid'][0]

            data = abstract_grab(cls.INFO_API_URL % vid)
            data = json.loads(data)
            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=data['title'],
                    cover=data['coverForDetail']
                )
            )
            for item in data['playInfo']:
                result.options.append(HandlerOutput.Option(
                    quality=item['name'] + '(' + item['type'] + ')',
                    urls=[HandlerOutput.Url(url=item['url'])]
                ))
        except Exception as err:
            raise Error.ERROR_HANDLER(debug_message=cls.NAME + '，' + str(err))

        return HandlerAdapter([result])
