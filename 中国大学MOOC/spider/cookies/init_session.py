import json
import os
import random
import time
import warnings
from http.cookiejar import MozillaCookieJar

from requests import Session

from 中国大学MOOC.login_flow.gtGetTk import getLoginTicket
from 中国大学MOOC.login_flow.iniGetCookie import getCookies_channel_0
from 中国大学MOOC.login_flow.l_login import login
from 中国大学MOOC.login_flow.powGetP import get_pVParam

warnings.filterwarnings("ignore")


def valid_cookie(cookie_jar):
    """检查Cookie是否有效"""
    if len(cookie_jar) == 0:
        return False  # CookieJar 为空，说明没有有效的Cookie

    current_time = time.time()  # 获取当前时间戳
    for cookie in cookie_jar:
        # 检查是否有过期时间
        if cookie.expires:
            # 如果过期时间小于当前时间，说明已过期
            if cookie.expires < current_time:
                return False
    return True

def __get_headers():
    return {
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


def init_logined_session():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    account_filename = f'{current_dir}/account.tmp'  # 账号密码文件
    cookie_filename = f'{current_dir}/cookies.tmp'  # 10 天有效期Cookie

    session = Session()
    session.headers = __get_headers()
    cookie_jar = MozillaCookieJar()
    session.cookies = cookie_jar  # 绑定
    # 优先使用 cookies 登录，但需要保证 cookies 有效
    if os.path.exists(cookie_filename):
        # print("使用已保存的 cookies 登录 : ", cookie_filename)
        cookie_jar.load(cookie_filename, ignore_expires=True)  # 保存 Cookie 到文件
    if valid_cookie(cookie_jar):
        print("使用已保存且有效的 cookies 登录 : ", cookie_filename)
        session.get('https://www.icourse163.org/home.htm')
        return session
    else:
        # 使用账号密码登录
        print(f"读取账号密码 : ", account_filename)
        account = open(account_filename, "r", encoding="utf-8").readlines()
        email = account[0].strip()
        password = account[1].strip()
        # 获取 email 登录渠道的Cookie
        cookies_email = getCookies_channel_0()
        # 获取并完成VDF计算任务
        pVParam = get_pVParam(cookies_email)
        # 获取登录令牌 tk
        tk = getLoginTicket(cookies_email, email)
        time.sleep(random.randint(3, 5))
        # SSO单点登录: 获取网易单点登录的 NTES_PASSPORT
        login(session, email, password, cookies_email, tk, pVParam)
        # 获取并设置MOOC身份标识 Cookie: STUDY_INFO、STUDY_PERSIST、STUDY_SESS
        params = {
            'type': 'urs',
            'returnUrl': 'aHR0cHM6Ly93d3cuaWNvdXJzZTE2My5vcmcv',
            'edusave': '1',
            'loginWay': '0',
        }
        session.get(
            'https://www.icourse163.org/passport/logingate/changeCookie.htm',
            params=params,
            verify=False,
        )
        session.get('https://www.icourse163.org/home.htm')
        print(f"保存cookies : ", cookie_filename)
        cookie_jar.save(cookie_filename)
        return session


if __name__ == '__main__':
    session = init_logined_session()
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
