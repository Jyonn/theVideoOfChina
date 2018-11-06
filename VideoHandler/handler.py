from Base.error import Error
from Base.response import Ret


class Handler:
    SUPPORT_VERSION = 3
    NAME = '视频'

    @staticmethod
    def detect(url):
        return False

    @classmethod
    def handler(cls, url):
        return Ret(Error.ERROR_HANDLER)


class HandlerOutput:
    class Url:
        def __init__(self, url=str(), index=int()):
            self.index = index
            self.url = url

        def to_dict(self):
            return dict(
                index=self.index,
                url=self.url,
            )

    class Option:
        def __init__(self, urls=list(), quality='默认'):
            self.urls = urls
            self.quality = quality

        def to_dict(self):
            urls = []
            for url in self.urls:
                urls.append(url.to_dict())

            return dict(
                quality=self.quality,
                urls=urls,
            )

    class VideoInfo:
        def __init__(self, title=str(), cover=str()):
            self.title = title
            self.cover = cover

        def to_dict(self):
            return dict(
                title=self.title,
                cover=self.cover,
            )

    def __init__(self, options=list(), video_info=VideoInfo(), one_option=None, one_url=None):
        if one_url:
            one_option = self.Option(urls=[self.Url(url=one_url)])
        if one_option:
            self.options = [one_option]
        else:
            self.options = options
        self.video_info = video_info

    def to_dict(self):
        options = []
        for option in self.options:
            options.append(option.to_dict())

        return dict(
            video_info=self.video_info.to_dict(),
            options=options,
        )
