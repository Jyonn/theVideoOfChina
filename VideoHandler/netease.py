import base64
import binascii
import json
from urllib import parse

from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from SmartDjango import Packing
from django.utils.crypto import get_random_string

from Base.common import deprint
from Base.error import Error
from Base.grab import abstract_post
from VideoHandler.handler import Handler, HandlerOutput, HandlerAdapter


class NetEase(Handler):
    """
    "https://music.163.com/weapi/v1/resource/comments/R_VI_62_357690084A5ACB19443898F05E4FEAB6"
    "{"rid":"R_VI_62_357690084A5ACB19443898F05E4FEAB6","offset":"0","total":"true","limit":"20","csrf_token":""}"

    "/weapi/cloudvideo/v1/allvideo/rcmd"
    "{"id":"357690084A5ACB19443898F05E4FEAB6","type":"1","csrf_token":""}"

    "/weapi/cloudvideo/v1/video/detail"
    "{"id":"357690084A5ACB19443898F05E4FEAB6","csrf_token":""}"

    "/weapi/cloudvideo/v1/video/statistic"
    "{"id":"357690084A5ACB19443898F05E4FEAB6","csrf_token":""}"

    "/weapi/cloudvideo/playurl"
    "{"ids":"[\"357690084A5ACB19443898F05E4FEAB6\"]","resolution":"480","csrf_token":""}"
    """

    SUPPORT_VERSION = 2
    NAME = '网易云音乐MV'

    MV_API = 'https://music.163.com/weapi/cloudvideo/playurl?csrf_token='
    DETAIL_API = 'https://music.163.com/weapi/cloudvideo/v1/video/detail?csrf_token='

    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'PostmanRuntime/7.4.0',
    }

    @staticmethod
    def rsa_encrypt(key):
        e = '010001'
        n = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615' \
            'bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf' \
            '695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46' \
            'bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b' \
            '8e289dc6935b3ece0462db0a22b8e7'
        reverse_key = key[::-1]
        pub_key = RSA.construct([int(n, 16), int(e, 16)])
        hexlify = int(binascii.hexlify(reverse_key.encode()), 16)
        encrypt_key = pub_key.encrypt(hexlify, None)[0]
        return format(encrypt_key, 'x').zfill(256)

    @staticmethod
    def aes_encrypt(text, key, iv="0102030405060708"):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, 2, iv)
        enc_text = encryptor.encrypt(text)
        enc_text_encode = str(base64.b64encode(enc_text))[2:-1]
        return enc_text_encode

    @classmethod
    def netease_encrypt(cls, text):
        """
        :param text: 明文
        :return: 加密后的参数
        """
        assert isinstance(text, str), "明文必需为字符串类型"
        first_aes_key = '0CoJUm6Qyw8W8jud'
        second_aes_key = get_random_string(length=16)
        second_aes_key = "PmlROzmWlU1Bhvgg"
        enc_text = cls.aes_encrypt(text, first_aes_key)
        enc_text = cls.aes_encrypt(enc_text, second_aes_key)
        enc_aes_key = cls.rsa_encrypt(second_aes_key)
        return dict(
            params=enc_text,
            encSecKey=enc_aes_key,
        )

    @staticmethod
    def detect(url):
        return url.find('music.163.com') > -1 and url.find('video') > -1

    @classmethod
    @Packing.pack
    def handler(cls, url):
        try:
            url = url.replace('#/', '')
            o = parse.urlparse(url)
            qs = parse.parse_qs(o.query)
            vid = qs['id'][0]

            data = '{"id":"%s","csrf_token":""}' % vid
            encrypted_data = cls.netease_encrypt(data)
            data = abstract_post(cls.DETAIL_API, encrypted_data, headers=cls.HEADERS)
            data = json.loads(data)['data']

            result = HandlerOutput(
                video_info=HandlerOutput.VideoInfo(
                    title=data['title'],
                    cover=data['coverUrl'],
                ),
                options=[],
            )

            for item in data['resolutions']:
                data = '{"ids":"[\\"%s\\"]","resolution":"%s","csrf_token":""}' % \
                       (vid, item['resolution'])
                encrypted_data = cls.netease_encrypt(data)

                data = abstract_post(cls.MV_API, encrypted_data, headers=cls.HEADERS)
                data = json.loads(data)
                if len(data['urls']) > 1:
                    print(data)
                result.options.append(HandlerOutput.Option(
                    urls=[HandlerOutput.Url(url=data['urls'][0]['url'])],
                    quality=data['urls'][0]['r'],
                ))
        except Exception as err:
            deprint(str(err))
            return Error.ERROR_HANDLER('具体原因：' + cls.NAME + '，' + str(err))

        return HandlerAdapter([result])
