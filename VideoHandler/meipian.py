import re

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_grab
from Base.response import Ret
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class MeiPianArticle(Handler):
    SUPPORT_VERSION = 3
    NAME = '美篇文章内置视频'

    @staticmethod
    def detect(url):
        return url.find('meipian.cn') > -1

    @classmethod
    def handler(cls, url):
        try:
            html = abstract_grab(url)
            video_regex = '<video src="(.*?)".*?poster="(.*?)"'
            videos = re.findall(video_regex, html, flags=re.S)
            title_regex = 'name="keywords" content="(.*?)"'
            title = "《" + re.search(title_regex, html, flags=re.S).group(1) + "》"
        except Exception as err:
            deprint(str(err))
            return Ret(Error.ERROR_HANDLER, append_msg='，具体原因：' + cls.NAME + '，' + str(err))

        results = []
        for index, video in enumerate(videos):
            result = HandlerOutput(
                one_url=video[0],
                video_info=HandlerOutput.VideoInfo(
                    cover=video[1],
                    title=title + ' 文章内视频%s' % index,
                )
            )
            results.append(result)

        return Ret(HandlerAdapter(results))
