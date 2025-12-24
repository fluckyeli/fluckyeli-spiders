import json

from 中国大学MOOC.spider.initSession import *

"""
获取指定课程的课件
'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc'
"""


def down(term_id='1475968443'):
    # 使用账号密码登录
    # pwd = open("../login_flow/pwd.tmp", "r", encoding="utf-8").read()
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
        'termId': term_id,
    }

    response = session.post(
        'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc',
        params=params,
        data=data,
    )

    return response.json()


if __name__ == '__main__':
    term_id = '1475968443'
    res = down(term_id)
    with open('getLastLearnedMocTermDto.json', encoding='utf-8', mode='w') as fw:
        fw.write(json.dumps(res, indent=4, ensure_ascii=False))
    print("课件获取成功！")
