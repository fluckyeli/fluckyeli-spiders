import requests
import json
import random
import time

from 中国大学MOOC.login_flow.enc_utils.sm4 import sm4_encrypt
from 中国大学MOOC.login_flow.enc_utils.rsa_PKCS_1v1_5 import rsa_encrypt
from 中国大学MOOC.login_flow.enc_utils.rtid import generate_rtid
from 中国大学MOOC.login_flow.enc_utils.time_utils import getTimeStampOfMilliSeconds
from 中国大学MOOC.login_flow.iniGetCookie import getCookies_channel_0
from 中国大学MOOC.login_flow.gtGetTk import getLoginTicket
from 中国大学MOOC.login_flow.powGetP import get_pVParam
from l_login import login


def parse_STUDY_SESS(l_login_passport):
    cookies = l_login_passport

    headers = {
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

    cookie_str = response.headers.get('Set-Cookie')
    print("cookie_str:", cookie_str)

    return {
        'STUDY_SESS': cookie_str.split("STUDY_SESS=")[1].split(";")[0],
        'STUDY_INFO': cookie_str.split("STUDY_INFO=")[1].split(";")[0],
        'STUDY_PERSIST': cookie_str.split("STUDY_PERSIST=")[1].split(";")[0],
    }


if __name__ == '__main__':
    email = "ocean_yyl@163.com"
    password = open("../login_flow/pwd.tmp", "r", encoding="utf-8").read()
    cookies = getCookies_channel_0()
    pVParam = get_pVParam(cookies)
    tk = getLoginTicket(cookies, email)
    time.sleep(random.randint(3, 5))
    l_login_passport = login(email, password, cookies, tk, pVParam)
    print("l_login_passport:", l_login_passport)
    cookies = parse_STUDY_SESS(l_login_passport)
    print(cookies)
