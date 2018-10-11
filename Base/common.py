""" 171203 Adel Liu """

DEBUG = True


def deprint(*args):
    """
    系统处于调试状态时输出数据
    """
    if DEBUG:
        print(*args)


def md5(s):
    """获取字符串的MD5"""
    import hashlib
    md5_ = hashlib.md5()
    md5_.update(s.encode())
    return md5_.hexdigest()
