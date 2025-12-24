import json

import requests

cookies = {
    # 'EDUWEBDEVICE': 'feee490a55214d90a38a19c8aa1857e3',
    # '__yadk_uid': '5hJveYnxCtgaU8QpsncfDgvlp2',
    # 'MOOC_PRIVACY_INFO_APPROVED': 'true',
    # 'WM_NI': 'F8Da2MQPSJ%2Bd8c9TcCGG8VClDqN7dY%%2FRb1o9ZR5ZxwzWDss5QbE5sAViGL3tnZLI%2BrQ8zvsXVlIFPFTfmYpl282H6WkxdGMJl95vYUJyRseQOgOey%2B3Fm2b28%3D',
    # 'WM_NIKE': '',
    # 'WM_TID': 'vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi',
    'NTESSTUDYSI': 'abb608c49f0e42f8a91bc33e2dbead4f',
    'STUDY_INFO': '"@163.com|-1||"',
    'STUDY_SESS': '"CkRzH3oHpH+/+rs1VHEyXQz/x++/Qou"',
    'STUDY_PERSIST': '"dKmEJ3j368/+JrTEC+ndjlWXNJVwXTTE4ROlI1A8U//acjsEWiA=="',
    # 'NETEASE_WDA_UID': '#|#1488366520887',
    # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766493047,1766555978,1766560974,1766564460',
    # 'HMACCOUNT': '1C35BFE2DDEED52B',
    # 'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766564507',
}

headers = {
    # 'accept': '*/*',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'content-type': 'application/x-www-form-urlencoded',
    # 'dnt': '1',
    # 'edu-script-token': 'abb608c49f0e42f8a91bc33e2dbead4f',
    # 'origin': 'https://www.icourse163.org',
    # 'priority': 'u=1, i',
    # 'referer': 'https://www.icourse163.org/learn/ZJU-199001?tid=1475968443',
    # 'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

params = {
    'csrfKey': 'abb608c49f0e42f8a91bc33e2dbead4f',
}

data = {
    'termId': '1475968443',
}

response = requests.post(
    'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(json.dumps(response.json(), ensure_ascii=False))
