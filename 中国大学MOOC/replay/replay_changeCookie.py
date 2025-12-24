import requests
from bs4 import BeautifulSoup

cookies = {
    'NTES_PASSPORT': '',
    # 'EDUWEBDEVICE': '7f37af717f3745229a64dc0d5535929b',
    # 'MOOC_PRIVACY_INFO_APPROVED': 'true',
    # 'NETEASE_WDA_UID': '1024616784#|#1488366520887',
    # 'NTESSTUDYSI': 'd838ea57958b4c9fb52d5bf878daa782',
    'NTES_SESS': '.IhO8KLz.',
    # 'ANTICSRF': '968f6e960e6b259ee0f9e3f42d1f00e0',
    # 'S_INFO': '1766500392|1|0&60##|ocean_yyl',
}

headers = {
    # 'Host': 'www.icourse163.org',
    # 'Dnt': '1',
    # 'Upgrade-Insecure-Requests': '1',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'Sec-Fetch-Site': 'cross-site',
    # 'Sec-Fetch-Mode': 'navigate',
    # 'Sec-Fetch-Dest': 'document',
    # 'Sec-Ch-Ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Referer': 'https://www.icourse163.org/',
    # # 'Accept-Encoding': 'gzip, deflate',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'Sec-Gpc': '1',
    # 'Priority': 'u=0, i',
}

params = {
    'type': 'urs',
    'returnUrl': 'aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv',
    'edusave': '1',
    'loginWay': '0',
}

response = requests.get(
    'https://www.icourse163.org/passport/logingate/changeCookie.htm',
    params=params,
    cookies=cookies,
    headers=headers,
    verify=False,
)

print(response.headers['Set-Cookie'])
