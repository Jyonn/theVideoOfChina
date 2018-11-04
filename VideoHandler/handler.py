from Base.error import Error
from Base.response import Ret


class Handler:
    SUPPORT_VERSION = 1
    NAME = '通用视频'

    @staticmethod
    def detect(url):
        return False

    @classmethod
    def handler(cls, url):
        return Ret(Error.EMPTY_HANDLER)
