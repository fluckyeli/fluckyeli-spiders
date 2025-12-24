import requests

cookies = {
    'EDUWEBDEVICE': 'feee490a55214d90a38a19c8aa1857e3',
    '__yadk_uid': '5hJveYnxCtgaU8QpsbE40m9ncfDgvlp2',
    'MOOC_PRIVACY_INFO_APPROVED': 'true',
    'NTES_PASSPORT': '.',
    'WM_NI': 'F8Da2MQPSJ%%2B27k54UdIT%2FRb1o9ZR5ZxwzWDss5QbE5sAViGL3tnZLI%2BrQ8zvsXVlIFPFTfmYpl282H6WkxdGMJl95vYUJyRseQOgOey%2B3Fm2b28%3D',
    'WM_NIKE': '9ca17ae2e6ffcda170e2e6ee89d543f29c8399fc7aac968fa6c84f968e9e83d772bb88fb93b35292eda386ae2af0fea7c3b92a86e88c82b14793909dabaa70fcbdf7b5e2498599f8b7c26888af82d8e753e9eef98cb84097bc87b5ae5aa2efa1dad95af786b898f95d88adbdd6d46a87ebbda2d5638594fd95ed529097e593d434baaabdb9d5688b9aa0a7d76eaf87c08db134f298fab8ea74a89983abef33f7aa97b6c97392adabb2ce6d8dbbb7ccb24eafeeaed3bb37e2a3',
    'WM_TID': 'vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi',
    'NTESSTUDYSI': '',
    'STUDY_INFO': '"@.com|-1||"',
    'STUDY_SESS': '"CkRzH3oHpH+/+/x++/Qou"',
    'STUDY_PERSIST': '"dKmEJ3j368/+JrTEC+//acjsEWiA=="',
    'NETEASE_WDA_UID': '1024616784#|#1488366520887',
    'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766493047,1766555978,1766560974,1766564460',
    'HMACCOUNT': '1C35BFE2DDEED52B',
    'hasVolume': 'true',
    'videoVolume': '0.8',
    'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766569478',
}

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'dnt': '1',
    'edu-script-token': 'abb608c49f0e42f8a91bc33e2dbead4f',
    'origin': 'https://www.icourse163.org',
    'priority': 'u=1, i',
    'referer': 'https://www.icourse163.org/channel/2001.htm',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

params = {
    'csrfKey': 'abb608c49f0e42f8a91bc33e2dbead4f',
}

data = {
    'mocCourseQueryVo': '{"categoryId":-1,"categoryChannelId":2001,"orderBy":0,"stats":30,"pageIndex":3,"pageSize":20}',
}

response = requests.post(
    'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)