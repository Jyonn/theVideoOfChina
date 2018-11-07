from urllib import parse

from django.views import View

from Base.decorator import require_get, require_post
from Base.error import Error
from Base.response import response, error_response, Ret
from VideoHandler.douyin import DouyinShort, DouyinLong
from VideoHandler.ergeng import ErGeng
from VideoHandler.handler import Handler
from VideoHandler.meipian import MeiPianArticle
from VideoHandler.pearvideo import PearVideo
from VideoHandler.xinpianchang import XinPianChang
from VideoHandler.video_qq import ArenaOfValorHelper, WeixinArticle

websites = [
    XinPianChang,
    ErGeng,
    PearVideo,
    ArenaOfValorHelper,
    DouyinShort,
    DouyinLong,
    WeixinArticle,
    MeiPianArticle,
]


def get_url(url):
    import re
    pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式

    urls = re.findall(pattern, url)
    if urls:
        return Ret(urls[0])
    return Ret(Error.NO_URL)


param_list = [
    {
        'value': 'url',
        'process': parse.unquote,
    },
    {
        'value': 'v',
        'default': True,
        'default_value': 1,
        'process': int,
    }
]


def check_support(url, v):
    web_str = ''
    new_support_str = ''

    for web in websites:
        if web.detect(url):
            if v < web.SUPPORT_VERSION:
                return Ret(Error.NEW_VERSION_SUPPORT)
            return Ret(web)
        web_str += web.NAME + ' '
        if v < web.SUPPORT_VERSION:
            new_support_str += web.NAME + ' '

    if v < Handler.LATEST_VERSION:
        append_msg = '，新版本支持对 %s资源的下载' % new_support_str
    else:
        append_msg = '，目前支持对 %s资源对下载' % web_str

    return Ret(Error.UNRESOLVED_LINK, append_msg=append_msg)


def v1_compat(ret, v):
    if v > 1:
        return ret
    return Ret(dict(
        more_options=[dict(
            quality='老版本将于2018年底放弃兼容',
            url='https://s.6-79.cn/7RcehV'
        )]
    ))


def get_dl_link(request):
    url = request.d.url
    v = request.d.v

    ret = get_url(url)
    if ret.error is not Error.OK:
        return ret
    url = ret.body

    ret = check_support(url, v)
    if ret.error is not Error.OK:
        return v1_compat(ret, v)
    web = ret.body

    ret = web.handler(url)
    if ret.error is not Error.OK:
        return ret
    results = ret.body
    return Ret(results.to_dict(v))


class LinkView(View):
    @staticmethod
    @require_get(param_list)
    def get(request):
        ret = get_dl_link(request)
        if ret.error is not Error.OK:
            return error_response(ret)
        return response(ret.body)

    @staticmethod
    @require_post(param_list)
    def post(request):
        ret = get_dl_link(request)
        if ret.error is not Error.OK:
            return error_response(ret)
        return response(ret.body)
