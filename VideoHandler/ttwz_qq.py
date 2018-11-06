import json
from urllib import parse

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_post, abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput


class TTWZ_QQ(Handler):
    SUPPORT_VERSION = 2
    NAME = '王者荣耀助手视频'

    GET_VID_API = 'http://api.kohsocialapp.qq.com:10001/game/detailinfov2'
    VIDEO_INFO_API = 'http://h5vv.video.qq.com/getinfo?otype=json&platform=11001&vids=%s'

    @staticmethod
    def detect(url):
        o = parse.urlparse(url)
        qs = parse.parse_qs(o.query)
        return o.netloc == 'image.ttwz.qq.com' and 'gameId' in qs and 'iInfoId' in qs

    @classmethod
    def handler(cls, url):
        try:
            o = parse.urlparse(url)
            qs = parse.parse_qs(o.query)
            gameId = qs['gameId'][0]
            iInfoId = qs['iInfoId'][0]

            data = abstract_post(cls.GET_VID_API, data=dict(iInfoId=iInfoId, gameId=gameId, cSystem=1))
            data = json.loads(data)['data']
            vid = data['sVid']

            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=data['sTitle'],
                    cover=data['sImageAbbrAddrMiddle'],
                ),
                only_default=False,
            )

            data = abstract_grab(cls.VIDEO_INFO_API % vid)
            data = json.loads(data[data.index('=')+1:-1])

            fs_dict = dict()
            for item in data['fl']['fi']:
                o = HandlerOutput.Option(quality=item['cname'], url=None)
                result.more_options.append(o)
                fs_dict[item['fs']] = o

            for item in data['vl']['vi']:
                fn = item['fn']
                fvkey = item['fvkey']
                url = item['ul']['ui'][0]['url']
                fs_dict[item['fs']].url = '%s%s?vkey=%s' % (url, fn, fvkey)

            result.more_options = list(filter(lambda x: x.url, result.more_options))
            result.default_url = result.more_options[0].url
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER)

        return Ret(result.to_dict())
