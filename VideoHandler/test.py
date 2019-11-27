import json
import re
import zlib
from urllib import parse, request


host = 'https://107cine.com/'
urls = [
    "community/magazine/817d1e94c78b4c2580025ae322b92347",
    "community/magazine/47341f0beb0a4297989bc47771e19872",
    "community/magazine/47dddeff6ff1407fbf45c3eb6cbb22c1",
    "community/magazine/366ac92c08c7474ca18cb38cc5567b0e",
    "community/magazine/0cb5a004d6d646e6a9afae30cf9a5132",
    "community/magazine/dbe869bc5d544f55ba194b09995dccdf",
    "community/magazine/39019b195d704cbd98bb438dc88457b5",
    "community/magazine/1928317052644274965ee35d1f387ecb",
    "community/magazine/da203ed32e1448f8861f9676806fa5ab",
    "community/magazine/c412494008cd4d07ba3a08181a197bf7",
    "community/magazine/bfe97ba83d724f4b8b6eb88bad0023b2",
    "community/magazine/27c81a3f9faa4f55903f75b290306ced",
    "community/magazine/8408a23990204a84a2fc9ea422843e9f",
    "community/magazine/b26ef20f7b4e44cc85ec69cecbf2ca81",
    "community/magazine/c6c01ee99cca49e59c6e043d5f893dfb",
    "community/magazine/364ba292514b483b88ba269c2690f995",
    "community/magazine/c588141b363d4bb9a08077b9d0e23490",
    "community/magazine/ac34aa4d8b6045ec9dccadba5cc1fdad",
    "community/magazine/439ba42e151b40a69d85bb34de2e12cb",
    "community/magazine/f248dccd5a6c42229c4485ed0f51a04d",
    "community/magazine/55cb61d848444183b7d902b4a494ec54",
    "community/magazine/996a7d1372314dd198c3bdd0fd36c458",
    "community/magazine/54f2166ec8b049e880b6df476f032944",
    "community/magazine/6edd671a6f034074a62256a5d4ad7237",
    "community/magazine/4edae84e7a3844a08e271f5c6bda1704",
    "community/magazine/f646d80658ee4d4897dd3b5c83092479",
    "community/magazine/3497d41f4c854853ba36f725cb800808",
    "community/magazine/65cc3d497f844b00b4f6de45f57fc1e4",
    "community/magazine/93e834f780354181be184ddee3e802c1",
]


def get_pdf_url(url):
    url = host + url
    req = request.Request(url)

    req.add_header("Accept",
                   "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
    req.add_header("Accept-Encoding", "gzip")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8")
    req.add_header("Cache-Control", "max-age=0")
    req.add_header("Connection", "keep-alive")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:69.0) Gecko/20100101 Firefox/69.0")
    req.add_header("Cookie",
                   " Hm_lvt_5ad3c04369b50e2caf373d1fa90f177e=1567750523,1567750544,1567752056; kohanasession=ldcfd65c74n4h30nght5h2dg84; payload=eyJhbGciOiJSUzI1NiJ9.eyJpc3MiOiIxMDdjaW5lIiwiZXhwIjoxNTY4MDE0NjE4LCJpYXQiOjE1NjgwMTQ1ODgsInVpZCI6MTI0ODAyOSwidXVpZCI6IjE0MjAxODRlLTU5OTEtNGM2ZS04YTQxLWY2N2E4MjlhNTljMyIsInVuYW1lIjoiMTc4MTY4NzE5NjEiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBaQ0k2TVRJME9EQXlPU3dpZFhWcFpDSTZJakUwTWpBeE9EUmxMVFU1T1RFdE5HTTJaUzA0WVRReExXWTJOMkU0TWpsaE5UbGpNeUlzSW1WNGNDSTZNVFU1T1RJeU9EVXlObjAuTjZSQ2lIYXVuSmJHaV9HcUt3LXd0Q1c1RlhrX3NLRC1GdDhWdFIwVXNRcyIsIm5ld2JpZSI6dHJ1ZX0.SbRnMpSelFmB5C-fuQ2Y-3PMBear2Ilckxm9jFiHHz0OmJPAgYwzdP6f9m5lAYb3KogBRO_rFopI2nY8q1_g8QeDmtjyafygDAHdSdAdl5z-CTFFAR5WDT-sq2I7GV81_XZa479UKn3RYHtDQ-EfDnk-NEmzNI7xr6kNOaAvOO7GO9lfi0piGnpjFc3sq6ILvgsPP4UYHpToJVrdQfXTA8ds86KIPPc9CSTRfDBx5h27YEoKSPhZrIC-owXrXyfHp3oKOrlU__TNqpKqrfiJZzdozV-8xlayZ58EOOMISnl6E4VP3-3jKcqUGPYxy192qsF_rlj7LENtY8zh2pTQdg; kohanasession_data=c2Vzc2lvbl9pZHxzOjI2OiJsZGNmZDY1Yzc0bjRoMzBuZ2h0NWgyZGc4NCI7dG90YWxfaGl0c3xpOjI7X2tmX2ZsYXNoX3xhOjA6e311c2VyX2FnZW50fHM6ODI6Ik1vemlsbGEvNS4wIChNYWNpbnRvc2g7IEludGVsIE1hYyBPUyBYIDEwLjE1OyBydjo2OS4wKSBHZWNrby8yMDEwMDEwMSBGaXJlZm94LzY5LjAiO2lwX2FkZHJlc3N8czoxNToiMTIyLjIyNS4yMjAuMTY0IjtsYXN0X2FjdGl2aXR5fGk6MTU2ODAxNDU4OTt1aWR8aToxMjQ4MDI5O3VuYW1lfHM6MTE6IjE3ODE2ODcxOTYxIjt1dWlkfHM6MzY6IjE0MjAxODRlLTU5OTEtNGM2ZS04YTQxLWY2N2E4MjlhNTljMyI7dG9rZW58czoxNjg6ImV5SmhiR2NpT2lKSVV6STFOaUo5LmV5SnBaQ0k2TVRJME9EQXlPU3dpZFhWcFpDSTZJakUwTWpBeE9EUmxMVFU1T1RFdE5HTTJaUzA0WVRReExXWTJOMkU0TWpsaE5UbGpNeUlzSW1WNGNDSTZNVFU1T1RJeU9EVXlObjAuTjZSQ2lIYXVuSmJHaV9HcUt3LXd0Q1c1RlhrX3NLRC1GdDhWdFIwVXNRcyI7bWVtYmVyX2lkfGk6MTAwMzEwNzttZW1iZXJfZW1haWx8czoyMzoiMTI0ODAyOUBwYWlwaWFuYmFuZy5jb20iO21lbWJlcl9uYW1lfHM6OToi5YiY5aWH54WaIjs%3D")

    res = request.urlopen(req)
    gzipped = res.headers.get('Content-Encoding')  # 判断是否压缩
    compressed_data = res.read()
    res.close()
    if gzipped:
        content = zlib.decompress(compressed_data, 16 + zlib.MAX_WBITS)  # 解压
    else:
        content = compressed_data
    content = content.decode("utf-8")

    pdf = re.search('file=(.*?)&uuid', content, flags=re.S).groups()[0]
    return host + 'asset/' + pdf + '.pdf'


for url in urls:
    print(get_pdf_url(url))
