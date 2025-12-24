import requests
from enc_utils.sm4 import sm4_encrypt
from enc_utils.rtid import generate_rtid
from iniGetCookie import getCookies_channel_0


def getLoginTicket(cookies, email):
    url = 'https://reg.icourse163.org/dl/zj/mail/gt'
    data = {
        "un": email,
        "pkid": "cjJVGQM",
        "pd": "imooc",
        "channel": 0,
        "topURL": "https://www.icourse163.org/",
        "rtid": generate_rtid()
    }

    encParams = sm4_encrypt(data)
    # print(encParams)
    res = requests.post(url, cookies=cookies, json={'encParams': encParams})
    tk = res.json().get('tk')
    print("获取令牌tk:", tk)
    return tk

if __name__ == '__main__':
    email = "test112233@163.com"
    cookies = getCookies_channel_0()
    tk = getLoginTicket(cookies,email)
    print(tk)
