from Base.decorator import require_get
from Base.error import Error
from Base.response import response, error_response
from VideoHandler.ergeng import ErGeng
from VideoHandler.pearvideo import PearVideo
from VideoHandler.xinpianchang import XinPianChang
from VideoHandler.ttwz_qq import TTWZ_QQ

websites = [
    XinPianChang,
    ErGeng,
    PearVideo,
    TTWZ_QQ,
]


@require_get(['url'])
def get_dl_link(request):
    url = request.d.url

    web_str = ''

    for web in websites:
        web_str += web.NAME + ' '
        if web.detect(url):
            ret = web.handler(url)
            if ret.error is not Error.OK:
                return error_response(ret)
            return response(body=ret.body)

    return error_response(Error.UNRESOLVED_LINK, append_msg='，目前只支持对 %s资源的下载' % web_str)
