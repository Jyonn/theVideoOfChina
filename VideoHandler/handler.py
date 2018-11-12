from Base.error import Error
from Base.response import Ret


class Handler:
    DETAILED_DATE = '181112'
    SUPPORT_VERSION = 1
    LATEST_VERSION = 3

    NAME = '通用视频'

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

        def to_dict(self, v):
            if v == 1 or v == 2:
                return dict(
                    quality=self.quality,
                    url=self.urls[0].url,
                )
            else:
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

        def to_dict(self, v):
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

    def to_dict(self, v):
        options = []
        for option in self.options:
            options.append(option.to_dict(v))

        if v == 1 or v == 2:
            return dict(
                video_info=self.video_info.to_dict(v),
                more_options=options,
                default_url=options[0]['url'],
            )
        else:
            return dict(
                video_info=self.video_info.to_dict(v),
                options=options,
            )


class HandlerAdapter:
    """
    多版本兼容输出类
    v1: GET {default_url, more_options=[{url, quality}], video_info={title, cover}}
        扩充视频库 二更视频 梨视频 新片场 抖音短分享链接

    v2: 兼容POST 提取URL json格式不变
        扩充视频库 抖音长分享链接 王者荣耀助手分享

    v3: 多视频爬取，视频分段 [{options=[{urls=[{url, index}], quality}], video_info={title, cover}}]
        扩充视频库 微信公众号文章内置视频 美篇文章内置视频
    """
    def __init__(self, results=list()):
        self.results = results

    def to_dict(self, v):
        if v == 1 or v == 2:
            return self.results[0].to_dict(v)
        else:
            result_list = []
            for result in self.results:
                result_list.append(result.to_dict(v))
            return result_list
