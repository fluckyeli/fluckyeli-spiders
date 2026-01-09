"""
获取指定课程的课件
'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc'
"""
import json

from 中国大学MOOC.spider.cookies.init_session import init_logined_session


def get_units(term_id, session=None):
    # 使用登录后保存的 Cookie
    if session is None:
        session = init_logined_session()
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
    term_id = '1475140442'
    res = get_units(term_id)
    with open('getLastLearnedMocTermDto.json', encoding='utf-8', mode='w') as fw:
        fw.write(json.dumps(res, indent=4, ensure_ascii=False))
    print("课件获取成功！")
