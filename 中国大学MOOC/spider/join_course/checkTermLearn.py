from 中国大学MOOC.spider.initSession import *
from 中国大学MOOC.spider.spider_unit.DWRResExtractor import extract_dwr_objects

"""
check 是否已参加此课程学习
注意：此处参数 current_term_id 与 课程id 并不是同一个字段
"""

def check_term_learned(current_term_id):
    # 使用账号密码登录
    # pwd = open("pwd.tmp", "r", encoding="utf-8").read()
    # session = init_logined_Session_with_account('ocean_yyl@163.com', pwd)

    # 使用保存的 passport sso登录
    # session = init_logined_Session_with_passport()

    # 使用登录后保存的 Cookie
    session = init_logined_Session_with_Cookie()
    cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}

    httpSessionId = cookie_dict.get('NTESSTUDYSI')
    timestamp = int(time.time() * 1000)

    data = ('callCount=1\n'
            'scriptSessionId=${scriptSessionId}190\n'
            f'httpSessionId={httpSessionId}\n'
            'c0-scriptName=CourseBean\n'
            'c0-methodName=checkTermLearn\n'
            'c0-id=0\n'
            f'c0-param0=string:{current_term_id}\n'
            f'batchId={timestamp}'
            )

    url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.checkTermLearn.dwr'

    response = session.post(
        url,
        data=data,
        verify=False,
    )
    # print(response.text)

    json_res = extract_dwr_objects(response.text)
    # print(json_res)
    return  json_res == 0


if __name__ == '__main__':
    currentTermId = '1475367443'
    joined = check_term_learned(currentTermId)
    print("是否已参加:", joined)