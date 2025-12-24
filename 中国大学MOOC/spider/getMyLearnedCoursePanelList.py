import json

from 中国大学MOOC.spider.initSession import *

"""
获取已选课程列表
https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc
"""


def down():
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

    res_course_list = []

    data = {
        'type': '30',
        'p': '1',
        'psize': '30',
    }

    response = session.post(
        'https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc',
        params=params,
        data=data,
    )

    res_course_list.extend(response.json().get('result').get('result'))
    pagination = response.json().get('result').get('pagination')
    totlePageCount = pagination.get('totlePageCount')
    totleCount = pagination.get('totleCount')
    print(f"已选课程总数: {totleCount}")
    for page in range(2, totlePageCount + 1):
        print("获取第{}页课程列表".format(page))
        time.sleep(random.randint(3, 10))
        data['p'] = str(page)
        response = session.post(
            'https://www.icourse163.org/web/j/learnerCourseRpcBean.getMyLearnedCoursePanelList.rpc',
            params=params,
            data=data,
        )
        res_course_list.extend(response.json().get('result').get('result'))

    return res_course_list


if __name__ == '__main__':
    res_course_list = down()
    with open('getMyLearnedCoursePanelList.tmp', encoding='utf-8', mode='w') as fw:
        fw.write(json.dumps(res_course_list, indent=4, ensure_ascii=False))
    print("总共获取的课程信息数: {}".format(len(res_course_list)))
