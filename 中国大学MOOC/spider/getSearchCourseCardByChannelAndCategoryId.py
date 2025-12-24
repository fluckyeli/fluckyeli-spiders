from requests import Session
import json
import time
import random


def get_course_list(category_channel_id=2001):
    session = Session()
    session.headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'dnt': '1',
        'edu-script-token': 'c17011b05edc4addba6f2bf3f34ebf0d',
        'origin': 'https://www.icourse163.org',
        'priority': 'u=1, i',
        'referer': 'https://www.icourse163.org/channel/2001.htm',
        'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    }
    session.get('https://www.icourse163.org/home.htm')  # 获取Cookie NTESSTUDYSI, 必须先访问首页
    # print(session.cookies)

    params = {
        'csrfKey': session.cookies.get('NTESSTUDYSI'),
    }

    query_dict = {
        "categoryId": -1,
        "categoryChannelId": category_channel_id,
        "orderBy": 0,
        "stats": 30,
        "pageIndex": 1,
        "pageSize": 20
    }

    data = {
        'mocCourseQueryVo': json.dumps(query_dict),
    }

    res_course_list = []

    response = session.post(
        'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc',
        params=params,
        data=data,
    )

    res_course_list.extend(response.json().get('result').get('list'))
    pagination = response.json().get('result').get('query')
    totlePageCount = pagination.get('totlePageCount')
    totleCount = pagination.get('totleCount')
    print(f"获取到的课程总数: {totleCount}，总页数: {totlePageCount}")
    for page in range(2, totlePageCount + 1):
        print("获取第{}页课程列表".format(page))
        time.sleep(random.randint(3, 10))
        query_dict['pageIndex'] = page
        data = {
            'mocCourseQueryVo': json.dumps(query_dict),
        }

        response = session.post(
            'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc',
            params=params,
            data=data,
        )
        res_course_list.extend(response.json().get('result').get('list'))

    return res_course_list

if __name__ == '__main__':
    category_channel_id = 2001 # 国家精品课程
    res_course_list = get_course_list(category_channel_id)
    with open('国家精品2001.json', encoding='utf-8', mode='w') as fw:
        fw.write(json.dumps(res_course_list, indent=4, ensure_ascii=False))
    print("总共获取的课程信息数: {}".format(len(res_course_list)))
