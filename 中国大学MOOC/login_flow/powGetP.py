import json
import random

import requests
from iniGetCookie import getCookies_channel_0
from enc_utils.sm4 import sm4_encrypt
from enc_utils.py_exec_js_vdf import web_worker_compute_sync

def powGetP(cookies):
    headers = {
        'Content-Type': 'application/json',
    }

    data = {
        "pkid": "cjJVGQM",
        "pd": "imooc",
        "channel": 0,
        "topURL": "https://www.icourse163.org/",
        "rtid": "5fHXtlQT4qwRL1NeId1MltndDKqWVwlZ"
    }

    json_data = {
        'encParams': sm4_encrypt(data),
    }

    response = requests.post('https://reg.icourse163.org/dl/zj/mail/powGetP', cookies=cookies, headers=headers,
                             json=json_data)

    powP = response.json().get('pVInfo')

    return powP


def get_pVParam(cookies):
    powP = powGetP(cookies)

    print("获取到VDF计算任务 powP:", powP)

    pVParam = web_worker_compute_sync(powP)
    # 强制设置为大于最小时间（spendTime实际计算的是计算开始一直到输入账号秘密的时间）
    # pVParam['spendTime'] = powP['minTime'] + random.randint(0, pVParam['maxTime'] - pVParam['minTime']) # 在minTime和maxTime之间随机
    pVParam['spendTime'] = powP['minTime'] # 直接设置spendTime 为 minTime

    # maxTime 不需要
    if 'maxTime' in pVParam:
        del pVParam['maxTime']

    print("完成计算任务 pVParam:", pVParam)

    # pVParam[]
    return pVParam


if __name__ == '__main__':
    cookies = getCookies_channel_0()
    # res = powGetP(cookies)
    # print(res)
    pVParam = get_pVParam(cookies)
    print("pVParam:", json.dumps(pVParam))
