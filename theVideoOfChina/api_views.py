from urllib import parse

from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response, error_response
from VideoHandler.douyin import Douyin, DouyinShort
from VideoHandler.ergeng import ErGeng
from VideoHandler.handler import HandlerOutput
from VideoHandler.pearvideo import PearVideo
from VideoHandler.xinpianchang import XinPianChang
from VideoHandler.ttwz_qq import TTWZ_QQ

websites = [
    XinPianChang,
    ErGeng,
    PearVideo,
    TTWZ_QQ,
    Douyin,
    DouyinShort,
]


def get_url(url):
    url = parse.unquote(url)
    import re
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    urls = re.findall(pattern, url)
    if urls:
        return urls[0]
    raise Exception()


param_list = [
    {
        'value': 'url',
        'process': get_url,
    },
    {
        'value': 'v',
        'default': True,
        'default_value': 1,
        'process': int,
    }
]


def get_dl_link(request):
    url = request.d.url
    v = request.d.v

    web_str = ''

    for web in websites:
        web_str += web.NAME + ' '

    if v < 2:
        return response(
            body=HandlerOutput(
                only_default=False,
                more_options=[
                    HandlerOutput.Option(
                        url='https://s.6-79.cn/7RcehV',
                        quality='Safiri打开s.6-79.cn/zghsp2升级',
                    )
                ],
                video_info=HandlerOutput.VideoInfo(
                    title=None,
                    cover=None,
                ),
                default_url='https://s.6-79.cn/7RcehV',
            ).to_dict()
        )

    web_str = ''

    for web in websites:
        if v < web.SUPPORT_VERSION:
            continue
        web_str += web.NAME + ' '
        if web.detect(url):
            ret = web.handler(url)
            if ret.error is not Error.OK:
                return error_response(ret)
            return response(body=ret.body)

    return error_response(Error.UNRESOLVED_LINK, append_msg='，目前只支持对 %s资源的下载' % web_str)


class LinkView(View):
    @staticmethod
    @require_get(param_list)
    def get(request):
        return get_dl_link(request)

    @staticmethod
    @require_post(param_list)
    def post(request):
        return get_dl_link(request)
