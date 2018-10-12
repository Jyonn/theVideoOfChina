from Base.decorator import require_get
from Base.error import Error
from Base.response import response, error_response
from VideoHandler.ergeng import ErGeng
from VideoHandler.pearvideo import PearVideo
from VideoHandler.xinpianchang import XinPianChang

websites = [
    XinPianChang,
    ErGeng,
    PearVideo,
]


@require_get(['url'])
def get_dl_link(request):
    url = request.d.url

    for web in websites:
        if web.detect(url):
            ret = web.handler(url)
            if ret.error is not Error.OK:
                return error_response(ret)
            return response(body=ret.body)

    return error_response(Error.UNRESOLVED_LINK)
