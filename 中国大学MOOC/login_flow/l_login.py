import json
import random
import time
from http.cookiejar import MozillaCookieJar
from requests import Session
from 中国大学MOOC.login_flow.enc_utils.sm4 import sm4_encrypt
from 中国大学MOOC.login_flow.enc_utils.rsa_PKCS_1v1_5 import rsa_encrypt
from 中国大学MOOC.login_flow.enc_utils.rtid import generate_rtid
from 中国大学MOOC.login_flow.enc_utils.time_utils import getTimeStampOfMilliSeconds
from 中国大学MOOC.login_flow.iniGetCookie import getCookies_channel_0
from 中国大学MOOC.login_flow.gtGetTk import getLoginTicket
from 中国大学MOOC.login_flow.powGetP import get_pVParam


def login(email, password, cookies, tk, pVParam):
    pub_key = """-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC5gsH+AA4XWONB5TDcUd+xCz7ejOFHZKlcZDx+pF1i7Gsvi1vjyJoQhRtRSn950x498VUkx7rUxg1/ScBVfrRxQOZ8xFBye3pjAzfb22+RCuYApSVpJ3OO3KsEuKExftz9oFBv3ejxPlYc5yq7YiBO8XlTnQN0Sa4R4qhPO3I2MQIDAQAB-----END PUBLIC KEY-----"""

    data = {
        "un": email,
        "pw": rsa_encrypt(pub_key, password),
        "pd": "imooc",
        "l": 1,
        "d": 10,
        "t": getTimeStampOfMilliSeconds(),
        "pkid": "cjJVGQM",
        "domains": "",
        "tk": tk,
        "pwdKeyUp": 1,
        "pVParam": pVParam,
        "channel": 0,
        "topURL": "https://www.icourse163.org/",
        "rtid": generate_rtid()
    }

    print("登录接口负载：", json.dumps(data))
    json_data = {
        'encParams': sm4_encrypt(data)
    }

    headers = {
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'dnt': '1',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'accept': '*/*',
        'origin': 'https://reg.icourse163.org',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://reg.icourse163.org/webzj/v1.0.1/pub/index_dl2_new.html?cd=%2F%2Fcmc.stu.126.net%2Fu%2Fcss%2Fcms%2F&cf=mooc_urs_login_css.css&MGID=1766228745382.3604&wdaId=UA1438236666413&pkid=cjJVGQM&product=imooc&cdnhostname=webzj.netstatic.net',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'sec-gpc': '1',
        'priority': 'u=1, i',
        'host': 'reg.icourse163.org',
    }

    session = Session()
    cookie_jar = MozillaCookieJar()
    session.cookies = cookie_jar
    response = session.post('https://reg.icourse163.org/dl/zj/mail/l', headers=headers, cookies=cookies,
                             json=json_data)

    if(response.json().get('ret') == '201'):
        print("登录成功！获取网易通行证：")

    print("passport:", session.cookies)
    cookie_jar.save('passport.tmp',ignore_discard=True,ignore_expires=True)

    return session.cookies


if __name__ == '__main__':
    email = "ocean_yyl@163.com"
    password = open("../login_flow/pwd.tmp", "r", encoding="utf-8").read()
    cookies = getCookies_channel_0()
    pVParam = get_pVParam(cookies)
    tk = getLoginTicket(cookies, email)
    time.sleep(random.randint(3, 5))
    passport = login(email, password, cookies, tk, pVParam)
