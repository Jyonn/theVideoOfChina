import requests
import json

vid = 'y00221a60w7' # replace with your vid
for definition in ('shd', 'hd', 'sd'):
    params = {
        'isHLS': False,
        'charge': 0,
        'vid': vid,
        'defn': definition,
        'defnpayver': 1,
        'otype': 'json',
        'platform': 10901,
        'sdtfrom': 'v1010',
        'host': 'v.qq.com',
        'fhdswitch': 0,
        'show1080p': 1,
    }
    r = requests.get('http://h5vv.video.qq.com/getinfo', params=params)
    data = r.content.decode()[len('QZOutputJson='):-1]
    data = json.loads(data)
    # print(data)
    # continue

    url_prefix = data['vl']['vi'][0]['ul']['ui'][0]['url']
    for stream in data['fl']['fi']:
        if stream['name'] != definition:
            continue
        stream_id = stream['id']
        urls = []
        for d in data['vl']['vi'][0]['cl']['ci']:
            keyid = d['keyid']
            filename = keyid.replace('.10', '.p', 1) + '.mp4'
            params = {
                'otype': 'json',
                'vid': vid,
                'format': stream_id,
                'filename': filename,
                'platform': 10901,
                'vt': 217,
                'charge': 0,
            }
            r = requests.get('http://h5vv.video.qq.com/getkey', params=params)
            data = r.content.decode()[len('QZOutputJson='):-1]
            data = json.loads(data)
            url = '%s/%s?sdtfrom=v1010&vkey=%s' % (url_prefix, filename, data['key'])
            urls.append(url)

        print('stream:', stream['name'])
        for url in urls:
            print(url)
