import requests

cookies = {
    'EDUWEBDEVICE': 'feee490a55214d90a38a19c8aa1857e3',
    '__yadk_uid': '5hJveYnxCtgaU8QpsbE40m9ncfDgvlp2',
    'WM_TID': 'vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi',
    'MOOC_PRIVACY_INFO_APPROVED': 'true',
    'WM_NI': '%2BNYHSFagVOsBjWR3Lyt4CC5cRJ%2FDhiiw8SiEyRyNFk%3D',
    'WM_NIKE': '',
    'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766475642,1766483252,1766483559,1766489147',
    'HMACCOUNT': '429EAEE7CC48C400',
    'NTESSTUDYSI': 'xxxxx',
    'NTES_SESS': '.NJ3BcOb9GOaq1dX15qNvmFR2djmIT1..NUXDIyp74m_zchZ1cDGYUSJkqfxUnRiTcriUVw1B9_5.UwDQZ4.nW4RtNfz9uBRqYZ0dtcE9G38xx6V7GUw2p5CArHadG1xdJD3',
    'NTES_PASSPORT': '.dl.',
    'STUDY_INFO': '"@.com|-1||"',
    'STUDY_SESS': '"CkRzH3oHpH+/+rs1VHEyXQz///Qou"',
    'STUDY_PERSIST': '"dKmEJ3j368/+JrTEC+//HR/wRjeRwSZnFf+WDu1ObWIOzRr5+/acjsEWiA=="',
    'NETEASE_WDA_UID': '1024616784#|#1488366520887',
    'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766489898',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.icourse163.org/passport/logingate/changeCookie.htm?type=urs&returnUrl=aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv&edusave=1&loginWay=0',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

response = requests.get('https://www.icourse163.org/', cookies=cookies, headers=headers)