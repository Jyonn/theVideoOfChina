import json
import re
from urllib import parse

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_post, abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class VideoQQ:
    VIDEO_INFO_API = 'http://h5vv.video.qq.com/getinfo?otype=json&vid=%s&defn=%s'
    SEG_VIDEO_API = \
        'http://h5vv.video.qq.com/getkey?otype=json&vid=%s&format=%s&filename=%s&platform=10901'

    @classmethod
    def get_video_link(cls, vid):
        definitions = ['shd', 'hd', 'sd']

        options = []
        for defn in definitions:
            data = abstract_grab(cls.VIDEO_INFO_API % (vid, defn))
            data = json.loads(data[data.index('=') + 1:-1])

            qualities = dict()
            for item in data['fl']['fi']:
                qualities[item['fs']] = item

            for item in data['vl']['vi']:
                option = HandlerOutput.Option(quality=qualities[item['fs']]['cname'], urls=[])
                options.append(option)
                url_prefix = item['ul']['ui'][0]['url']
                if item['cl']['fc']:
                    for seg in item['cl']['ci']:
                        keyid = seg['keyid']
                        filename = keyid.replace('.10', '.p', 1) + '.mp4'
                        data = abstract_grab(cls.SEG_VIDEO_API % (
                            vid, qualities[item['fs']]['id'], filename))
                        data = json.loads(data[data.index('=') + 1:-1])
                        option.urls.append(
                            HandlerOutput.Url(
                                url='%s%s?vkey=%s' % (url_prefix, filename, data['key']),
                                index=seg['idx'] - 1,
                            )
                        )
                else:
                    fn = item['fn']
                    fvkey = item['fvkey']
                    option.urls.append(
                        HandlerOutput.Url('%s%s?vkey=%s' % (url_prefix, fn, fvkey))
                    )

        return options


class WeixinArticle(Handler):
    NAME = '微信公众号文章内置视频'
    SUPPORT_VERSION = 3

    @staticmethod
    def detect(url):
        return url.find('mp.weixin.qq.com/s/') > -1

    @classmethod
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            vid_regex = ';vid=(.*?)">'
            vids = re.findall(vid_regex, html, flags=re.S)

            title_regex = 'msg_title = "(.*?)";'
            title = "《" + re.search(title_regex, html, flags=re.S).group(1) + "》"

            cover_regex = 'msg_cdn_url = "(.*?)";'
            cover = re.search(cover_regex, html, flags=re.S).group(1)

            results = []
            for index, vid in enumerate(vids):
                result = HandlerOutput(
                    video_info=HandlerOutput.VideoInfo(
                        title=title + ' 文章内视频%s' % index,
                        cover=cover,
                    ),
                    options=VideoQQ.get_video_link(vid),
                )
                results.append(result)
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER, append_msg='，具体原因：' + cls.NAME + '，' + str(err))

        return Ret(HandlerAdapter(results))


class ArenaOfValorHelper(Handler):
    NAME = '王者荣耀助手视频'
    SUPPORT_VERSION = 2

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
            game_id = qs['gameId'][0]
            i_info_id = qs['iInfoId'][0]

            data = abstract_post(cls.GET_VID_API,
                                 data=dict(iInfoId=i_info_id, gameId=game_id, cSystem=1))
            data = json.loads(data)['data']
            vid = data['sVid']

            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=data['sTitle'],
                    cover=data['sImageAbbrAddrMiddle'],
                ),
                options=VideoQQ.get_video_link(vid),
            )

            result.default_option = result.options[0].url
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER, append_msg='，具体原因：' + cls.NAME + '，' + str(err))

        return Ret(HandlerAdapter([result]))

# print(
# HandlerOutput(
#     options=VideoQQ.get_video_link('m0028s08v11')
# ).to_dict())
