from 中国大学MOOC.spider.initSession import *
from DWRResExtractor import extract_dwr_objects

"""
下载指定的课件
【测验contentType=5】
'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'
"""


def get_testing_type_5(unit_id='1305713611', content_id='1263014'):
    # 使用账号密码登录
    # pwd = open("../login_flow/pwd.tmp", "r", encoding="utf-8").read()
    # session = init_logined_Session_with_account('ocean_yyl@163.com', pwd)

    # 使用保存的 passport sso登录
    # session = init_logined_Session_with_passport()

    # 使用登录后保存的 Cookie
    session = init_logined_Session_with_Cookie()
    cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}

    httpSessionId = cookie_dict.get('NTESSTUDYSI')
    timestamp = int(time.time() * 1000)
    contentType = 5  # 测验
    data = (f"callCount=1\n"
            "scriptSessionId=${scriptSessionId}190\n"
            f"httpSessionId={httpSessionId}\n"
            f"c0-scriptName=CourseBean\n"
            f"c0-methodName=getLessonUnitLearnVo\n"
            f"c0-id=0\n"
            f"c0-param0=number:{content_id}\n"
            f"c0-param1=number:{contentType}\n"
            f"c0-param2=number:0\n"
            f"c0-param3=number:{unit_id}\n"
            f"batchId={timestamp}")
    # print(data)

    url = 'https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr'

    response = session.post(
        url,
        data=data,
    )

    '''
    这是一个 DWR (Direct Web Remoting) 响应，具体是 JavaScript 代码片段，用于动态更新页面内容。
    DWR 是一种用于实现 Ajax 的 Java 库，
    它允许服务器端 Java 对象的方法在客户端 JavaScript 中直接调用，并返回 JavaScript 代码作为响应。
    '''
    # print(response.text)

    json_res = extract_dwr_objects(response.text)

    # print(json.dumps(json_res, ensure_ascii=False))
    return json_res.get('paper')


if __name__ == '__main__':
    unit_id = '1305713637'
    content_id = '1247392509'
    res = get_testing_type_5(unit_id, content_id)
    print(json.dumps(res, ensure_ascii=False))
