from requests import Session
from http.cookiejar import MozillaCookieJar
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
from 中国大学MOOC.login_flow.l_login import login
import warnings

warnings.filterwarnings("ignore")


def _get_headers():
    return  {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'content-type': 'application/x-www-form-urlencoded',
        'dnt': '1',
        'edu-script-token': 'abb608c49f0e42f8a91bc33e2dbead4f',
        'origin': 'https://www.icourse163.org',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }

def init_logined_Session_with_account(email, password):
    # 获取 email 登录渠道的Cookie
    cookies_email = getCookies_channel_0()
    # 获取并完成VDF计算任务
    pVParam = get_pVParam(cookies_email)
    # 获取登录令牌 tk
    tk = getLoginTicket(cookies_email, email)
    time.sleep(random.randint(3, 5))
    # SSO单点登录: 获取网易单点登录的 NTES_PASSPORT
    l_login_passport = login(email, password, cookies_email, tk, pVParam)

    session = Session()
    cookie_jar = MozillaCookieJar()
    for cookie in l_login_passport:
        cookie_jar.set_cookie(cookie)
    cookie_jar.save('passport.tmp', ignore_discard=True, ignore_expires=True)  # 保存passport 到文件（！敏感：通行证类似于账号密码）
    session.cookies = cookie_jar  # 绑定

    params = {
        'type': 'urs',
        'returnUrl': 'aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv',
        'edusave': '1',
        'loginWay': '0',
    }

    session.headers = _get_headers()

    # 获取并设置MOOC身份标识 Cookie: STUDY_INFO、STUDY_PERSIST、STUDY_SESS
    session.get(
        'https://www.icourse163.org/passport/logingate/changeCookie.htm',
        params=params,
        verify=False,
    )

    ### 获取设置 Cookie: NTESSTUDYSI
    STUDY_INFO = {cookie.name: cookie.value for cookie in cookie_jar}.get('STUDY_INFO')
    # 'STUDY_INFO': '"ocean_yyl@163.com|-1|1024616784|1766475649341"',
    userId = STUDY_INFO.split('|')[2]
    session.get('https://www.icourse163.org/home.htm', params={'userId': userId})

    cookie_jar.save('cookies.tmp', ignore_expires=True, ignore_discard=True)

    return session


def init_logined_Session_with_passport(passport_cookie_file='passport.tmp'):
    session = Session()
    cookie_jar = MozillaCookieJar()

    cookie_jar.load(passport_cookie_file, ignore_discard=True, ignore_expires=True)  # 保存passport 到文件（！敏感：通行证类似于账号密码）
    session.cookies = cookie_jar  # 绑定

    params = {
        'type': 'urs',
        'returnUrl': 'aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv',
        'edusave': '1',
        'loginWay': '0',
    }

    session.headers = _get_headers()
    # 获取并设置MOOC身份标识 Cookie: STUDY_INFO、STUDY_PERSIST、STUDY_SESS
    session.get(
        'https://www.icourse163.org/passport/logingate/changeCookie.htm',
        params=params,
        verify=False,
    )

    cookie_dict = {cookie.name: cookie.value for cookie in cookie_jar}
    print("changeCookie :", json.dumps(cookie_dict, ensure_ascii=False))

    ### 获取设置 Cookie: NTESSTUDYSI
    STUDY_INFO = cookie_dict.get('STUDY_INFO')
    # 'STUDY_INFO': '"ocean_yyl@163.com|-1|1024616784|1766475649341"',
    userId = STUDY_INFO.split('|')[2]
    session.get('https://www.icourse163.org/home.htm', params={'userId': userId})

    cookie_jar.save('cookies.tmp', ignore_expires=True, ignore_discard=True)

    return session


def init_logined_Session_with_Cookie(cookie_file='cookies.tmp'):
    session = Session()
    cookie_jar = MozillaCookieJar()
    cookie_jar.load(cookie_file, ignore_discard=True, ignore_expires=True)  # 保存 Cookie 到文件
    session.headers = _get_headers()
    session.cookies = cookie_jar  # 绑定
    return session


if __name__ == '__main__':
    # 使用账号密码登录
    # pwd = open("pwd.tmp", "r", encoding="utf-8").read()
    # session = init_logined_Session_with_account('ocean_yyl@163.com', pwd)

    # 使用保存的 passport sso登录
    # session = init_logined_Session_with_passport()

    # 使用登录后保存的 Cookie
    session = init_logined_Session_with_Cookie()
    cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}

    params = {
        'csrfKey': cookie_dict.get('NTESSTUDYSI')
    }

    data = {
        'type': '30',
        'p': '1',
        'psize': '8',
        'courseType': '1',
    }

    response = session.post(
        'https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc',
        params=params,
        data=data,
    )
    print(json.dumps(response.json(), ensure_ascii=False))
