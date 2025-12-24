import requests

cookies = {
    # 'EDUWEBDEVICE': '',
    # '__yadk_uid': '5hJveYnxCtgaU8QpsbE40m9ncfDgvlp2',
    # 'MOOC_PRIVACY_INFO_APPROVED': 'true',
    # 'NTES_PASSPORT': '.',
    # 'WM_NI': 'F8Da2MQPSJ%2Bd8c9TcCGG8VClDqN7dY%2B27k54UdIT%2FRb1o9ZR5ZxwzWDss5QbE5sAViGL3tnZLI%2BrQ8zvsXVlIFPFTfmYpl282H6WkxdGMJl95vYUJyRseQOgOey%2B3Fm2b28%3D',
    # 'WM_NIKE': '',
    # 'WM_TID': 'vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi',
    # 'hasVolume': 'true',
    # 'videoVolume': '0.8',
    'NTESSTUDYSI': '',
    # 'STUDY_INFO': '"ocean_yyl@163.com|-1|1024616784|1766573084792"',
    'STUDY_SESS': '"CkRzH3oHpH+/+rs1VHEyXQz//Qou"',
    # 'STUDY_PERSIST': '"dKmEJ3j368/+JrTEC+ndjqrZ++/whN5US+/p6McDuKTrgiDUd4B+BtnaE3iVxVnHK+JxQ6ysgx9z5+VL2fRN/dmv03G2rSEL9OSdFA6J5jrZLCRv8JU8qN8WQLi3xTJ45sq/acjsEWiA=="',
    # 'NETEASE_WDA_UID': '#|#1488366520887',
    # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766560974,1766564460,1766572740,1766573087',
    # 'HMACCOUNT': '1C35BFE2DDEED52B',
    # 'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766573140',
}

headers = {
    # 'accept': '*/*',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'content-type': 'text/plain',
    # 'dnt': '1',
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

data = 'callCount=1\nscriptSessionId=${scriptSessionId}190\nhttpSessionId=aacb3c6d8bfe41a88b71eb10f63911cd\nc0-scriptName=CourseBean\nc0-methodName=getLessonUnitLearnVo\nc0-id=0\nc0-param0=number:1263014\nc0-param1=number:1\nc0-param2=number:0\nc0-param3=number:1305713611\nbatchId=1766573140956'

response = requests.post(
    'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr',
    cookies=cookies,
    headers=headers,
    data=data,
)
print(response.text)