import requests

cookies = {
    'NTES_P_UTID': '|1766488433',
    'NTES_PASSPORT': '...iA....',
    'SID': 'e2bf5455-a26c-4046-ad97-9dbf3c32d2e6',
    'NTES_SESS': '..',
    'S_INFO': '|1|0&60##|ocean_yyl',
    'ANTICSRF': '5d8808542c0618d1f8fda706c56b77d8',
    'NTESwebSI': '.urs-virt31-regother16.dg.163.org-8009',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Referer': 'https://www.icourse163.org/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}

response = requests.get(
    'https://reg.163.com/chgcookie.jsp?product=imooc&domains=icourse163.org&username=ocean_yyl@163.com&userip=111.132.0.103&persistCookie=_79Z0ZMaCITiDX_QkeehpjbnWldWBPpUMQAYTJYudEQ7Wr3DXPNCo7N0eKfIKper5BZirnflz5ett5ZaAATJVu0B2db41GE1aBlgjaxCOVImd6kWAgrN6drWd1nV2W82VRFx7BifO5vG.ih2lHt3ZbpgA_pu8BJJLdyzNVqF8EhtD7KHXwZlRsF7E&retUrl=https%3A%2F%2Fwww.icourse163.org%2F%3Freferered%3Dhttps%3A%2F%2Fwww.icourse163.org%2F%26referered%3Dhttps%3A%2F%2Fwww.icourse163.org%2F%26referered%3Dhttps%3A%2F%2Fwww.icourse163.org%2F&loginUrl=https%3A%2F%2Fwww.icourse163.org%2Fmember%2Flogin.htm',
    cookies=cookies,
    headers=headers,
)

print(response.text)
print(response.headers)