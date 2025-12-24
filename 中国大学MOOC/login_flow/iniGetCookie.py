import requests
from enc_utils.sm4 import sm4_encrypt
from enc_utils.rtid import generate_rtid

"""
def getCookie_channel_3():
    url = 'https://reg.icourse163.org/zc/zj/yd/ini'
    data = {
        "pd": "imooc",
        "pkid": "cjJVGQM",
        "pkht": "www.icourse163.org",
        "channel": 3,
        "topURL": "https://www.icourse163.org/",
        "rtid": generate_rtid()
    }
    # print(json.dumps(data, ensure_ascii=False))
    encParams = sm4_encrypt(data)
    # print(encParams)
    res = requests.post(url, json={'encParams': encParams})
    return res.headers.get('Set-Cookie')

def getCookie_channel_1():
    url = 'https://reg.icourse163.org/dl/zj/yd/ini'
    data = {"pd":"imooc","pkid":"cjJVGQM","pkht":"www.icourse163.org","channel":1,"topURL":"https://www.icourse163.org/","rtid":generate_rtid()}
    # print(json.dumps(data, ensure_ascii=False))
    encParams = sm4_encrypt(data)

    res = requests.post(url, json={'encParams': encParams})
    return res.headers.get('Set-Cookie')
"""


def getCookies_channel_0():
    url = 'https://reg.icourse163.org/dl/zj/mail/ini'

    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "pd": "imooc",
        "pkid": "cjJVGQM",
        "pkht": "www.icourse163.org",
        "channel": 0,
        "topURL": "https://www.icourse163.org/",
        "rtid": generate_rtid()
    }
    # print(json.dumps(data, ensure_ascii=False))
    encParams = sm4_encrypt(data)

    res = requests.post(url, headers=headers, json={'encParams': encParams})
    setCookieByHeaders = res.headers.get('Set-Cookie')
    cookies = {
        'utid':generate_rtid(),
        'l_s_imooccjJVGQM': setCookieByHeaders.split("=")[1].split(";")[0]
    }

    print("获取到的 cookies:", cookies)

    return cookies


if __name__ == '__main__':
    cookie = getCookies_channel_0()
    print(cookie)
