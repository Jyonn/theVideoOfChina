from urllib import parse

from SmartDjango import Analyse
from django.views import View
from smartify import P

from Base.error import Error
from VideoHandler.douyin import DouyinShort, DouyinLong
from VideoHandler.ergeng import ErGeng
from VideoHandler.eyepetizer import EyePetizer
from VideoHandler.handler import Handler
from VideoHandler.meipian import MeiPianArticle
from VideoHandler.netease import NetEase
from VideoHandler.pearvideo import PearVideo
from VideoHandler.xinpianchang import XinPianChang
from VideoHandler.video_qq import ArenaOfValorHelper, WeixinArticle, VideoQQ

websites = [
    XinPianChang,
    ErGeng,
    PearVideo,
    ArenaOfValorHelper,
    DouyinShort,
    DouyinLong,
    WeixinArticle,
    MeiPianArticle,
    # VideoQQ,
    EyePetizer,
    NetEase,
]


def get_url(url):
    import re
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!#*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    urls = re.findall(pattern, url)
    if urls:
        return urls[0]
    raise Error.NO_URL


param_list = [
    P('url').process(parse.unquote),
    P('v').default(1).process(int),
]


def check_support(url, v):
    web_str = ''
    new_support_str = ''

    for web in websites:
        if web.detect(url):
            if v < web.SUPPORT_VERSION:
                raise Error.NEW_VERSION_SUPPORT
            return web
        web_str += web.NAME + ' '
        if v < web.SUPPORT_VERSION:
            new_support_str += web.NAME + ' '

    if v < Handler.LATEST_VERSION:
        append_msg = '，新版本支持对 %s资源的下载' % new_support_str
    else:
        append_msg = '，目前支持对 %s资源对下载' % web_str

    raise Error.UNRESOLVED_LINK(append_message=append_msg)


class LinkView(View):
    @staticmethod
    @Analyse.r(b=param_list)
    def post(r):
        url = get_url(r.d.url)
        v = r.d.v

        web = check_support(url, v)

        results = web.handler(url)
        return results.to_dict(v)
