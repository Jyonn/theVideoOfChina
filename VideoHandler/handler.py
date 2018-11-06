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
        return Ret(Error.ERROR_HANDLER)


class HandlerOutput:
    class Option:
        def __init__(self, url, quality='default'):
            self.url = url
            self.quality = quality

        def to_dict(self):
            return dict(
                quality=self.quality,
                url=self.url,
            )

    class VideoInfo:
        def __init__(self, title, cover):
            self.title = title
            self.cover = cover

        def to_dict(self):
            return dict(
                title=self.title,
                cover=self.cover,
            )

    def __init__(self, only_default=True, more_options=list(), default_url=None, video_info=None):
        if only_default:
            self.more_options = [self.Option(url=default_url)]
        else:
            self.more_options = more_options
        self.default_url = default_url
        self.video_info = video_info

    def to_dict(self):
        more_options = []
        for item in self.more_options:
            more_options.append(item.to_dict())

        return dict(
            default_url=self.default_url,
            video_info=self.video_info.to_dict(),
            more_options=more_options,
        )
