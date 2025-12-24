import requests

headers = {
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://reg.icourse163.org/',
    'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'sec-fetch-storage-access': 'none',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
}

params = {
    'clusterName': 'urs-webzj-static-passive',
    'modelName': 'webzj_response_webzc',
    'one': '1',
    'dataTime': '1766411325419',
    'name': 'webzj_power_mailzc',
    'sp': '1',
    'timeout': '0',
    'wapi': 'safelogin',
}

response = requests.get('https://pr.nss.netease.com/sentry/passive', params=params, headers=headers)
print(response.text)
print(response.headers)

"""
'kubeinsight-dst-application': 'sentry_passive_receiver',
'kubeinsight-dst-product': '哨兵系统',
'kubeinsight-dst-cluster': 'sentry_passive_receiver-docker-ops_online'

"""