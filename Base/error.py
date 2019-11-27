""" 180222 Adel Liu

错误表，在编码时不断添加
"""
from SmartDjango import E


@E.register()
class Error:
    UNRESOLVED_LINK = E("无法解析的链接")
    ERROR_HANDLER = E("处理错误")
    NEW_VERSION_SUPPORT = E("新版本支持下载此视频")
    NO_URL = E("找不到URL链接")
