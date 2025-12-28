import time

from 中国大学MOOC.spider.cookies.init_session import init_logined_session
from 中国大学MOOC.spider.spider_unit.DWRResExtractor import extract_dwr_objects

"""
参加课程学习
注意：此处参数 current_term_id 与 课程id 并不是同一个字段
"""


def join_term_learn(current_term_id):
    # 使用登录后保存的 Cookie
    session = init_logined_session()
    cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}

    httpSessionId = cookie_dict.get('NTESSTUDYSI')
    timestamp = int(time.time() * 1000)
    data = ('callCount=1\n'
            'scriptSessionId=${scriptSessionId}190\n'
            f'httpSessionId={httpSessionId}\n'
            'c0-scriptName=CourseBean\n'
            'c0-methodName=startTermLearn\n'
            'c0-id=0\n'
            f'c0-param0=string:{current_term_id}\n'
            'c0-param1=null:null\n'
            f'batchId={timestamp}'
            )
    url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.startTermLearn.dwr'
    response = session.post(
        url,
        data=data,
        verify=False,
    )

    # print(response.text)

    json_res = extract_dwr_objects(response.text) # 2253359955，2253360997
    # 猜测：返回一个服务器内部的学习记录ID，用于后续跟踪学习进度
    if '__DWR_CAPTURE__' in str(json_res):
        return None
    else:
        return json_res



if __name__ == '__main__':
    currentTermId = '1470036447'
    learn_id = join_term_learn(currentTermId)
    print(learn_id)