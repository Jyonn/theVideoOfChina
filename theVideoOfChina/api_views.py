from urllib import parse

from SmartDjango import Packing, Param
from django.views import View

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


@Packing.pack
def get_url(url):
    import re
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!#*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    urls = re.findall(pattern, url)
    if urls:
        return urls[0]
    return Error.NO_URL


param_list = [
    Param('url').process(parse.unquote),
    Param('v').dft(1).process(int),
]


@Packing.pack
def check_support(url, v):
    web_str = ''
    new_support_str = ''

    for web in websites:
        if web.detect(url):
            if v < web.SUPPORT_VERSION:
                return Error.NEW_VERSION_SUPPORT
            return web
        web_str += web.NAME + ' '
        if v < web.SUPPORT_VERSION:
            new_support_str += web.NAME + ' '

    if v < Handler.LATEST_VERSION:
        append_msg = '，新版本支持对 %s资源的下载' % new_support_str
    else:
        append_msg = '，目前支持对 %s资源对下载' % web_str

    return Error.UNRESOLVED_LINK(append_msg)


@Packing.pack
def v1_compat(ret, v):
    if v > 1:
        return ret
    return dict(
        more_options=[dict(
            quality='老版本将于2018年底放弃兼容',
            url='https://s.6-79.cn/7RcehV'
        )]
    )


@Packing.pack
def get_dl_link(request):
    url = request.d.url
    v = request.d.v

    ret = get_url(url)
    if not ret.ok:
        return ret
    url = ret.body

    ret = check_support(url, v)
    if not ret.ok:
        return v1_compat(ret, v)
    web = ret.body

    ret = web.handler(url)
    if not ret.ok:
        return ret
    results = ret.body
    return results.to_dict(v)


class LinkView(View):
    @staticmethod
    @Packing.http_pack
    @Param.require(q=param_list)
    def get(request):
        ret = get_dl_link(request)
        if not ret.ok:
            return ret
        return ret.body

    @staticmethod
    @Packing.http_pack
    @Param.require(b=param_list)
    def post(request):
        ret = get_dl_link(request)
        if not ret.ok:
            return ret
        return ret.body
