import requests

cookies = {
    # 'EDUWEBDEVICE': 'feee490a55214d90a38a19c8aa1857e3',
    # '__yadk_uid': '5hJveYnxCtgaU8QpsbE40m9ncfDgvlp2',
    # 'WM_TID': 'vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi',
    # 'MOOC_PRIVACY_INFO_APPROVED': 'true',
    # 'WM_NI': 'eAYZyzZXBWqCxGXln7GydfKhuubPxSidzuxWOFg1u3khj1CjfgYzZjwkbXaZ142y3sbgc0eRgrNARdJ5rsmq5FJ73%2BNYHSFagVOsBjWR3Lyt4CC5cRJ%2FDhiiw8SiEyRyNFk%3D',
    # 'WM_NIKE': '9ca17ae2e6ffcda170e2e6eea2e63d818bfc8bf64db58a8bb2d54e969e9a87d763f18d88b7b66b929ebc8bd92af0fea7c3b92aa79f97bbfc729a888eb8f449bc99988ded3d85a7ac87ca64b7abaeb1fb59abbcb696fb5d8d9aa9d2f839a9b8a6d2c262a6b9979bd962b5b5aeb9e452f3ecfe9ab279a2b9add1e85aa5ae82a2d1708aebbe94f07bf79a86d8b2218e8788b4c56ba58a8194c162958efdadfc80f89d8dd6e25a8af18c89ec63b5e89d8ac87392a782a7ea37e2a3',
    # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766117453,1766458229,1766460188,1766475642',
    # 'HMACCOUNT': '429EAEE7CC48C400',
    'NTES_SESS': '.D2SDJ..',
    'NTES_PASSPORT': '.Hybm_IgxS_o..1..6JyRk7xNtL4JB',
    'STUDY_INFO': '"ocean_yyl@.com|-||1766475649341"',
    'STUDY_SESS': '"CkRzH3oHpH+/+rs1VHEyXQz//+OJ2FcaMT+/+mUVcxqt7cD/YyC98nppr6KrivyjY6FmKs/Qou"',
    'STUDY_PERSIST': '"dKmEJ3j368/+JrTEC+ndhIyEObEI5+///acjsEWiA=="',
    # 'NETEASE_WDA_UID': '1024616784#|#1488366520887',
    # 'close_topBar': '1',
    # 'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766481202',
}



headers = {
    # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    # 'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'cache-control': 'max-age=0',
    # 'dnt': '1',
    # 'priority': 'u=0, i',
    # 'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'document',
    # 'sec-fetch-mode': 'navigate',
    # 'sec-fetch-site': 'same-origin',
    # 'sec-fetch-user': '?1',
    # 'upgrade-insecure-requests': '1',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

params = {
    'userId': '1024616784',
}

response = requests.get('https://www.icourse163.org/home.htm', params=params, cookies=cookies, headers=headers)
print(response.headers)
