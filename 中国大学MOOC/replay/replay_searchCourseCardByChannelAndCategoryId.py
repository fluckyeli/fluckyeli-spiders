import requests
import json

cookies = {
    'NTESSTUDYSI': 'c17011b05edc4addba6f2bf3f34ebf0d',
    # 'EDUWEBDEVICE': 'e49976bae49c4380a00b5483bd162e79',
    # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766587522',
    # 'HMACCOUNT': 'D4F747A2F49A726E',
    # 'WM_NI': 'wQp8ZaraGVfPiDrlEZsdEnEMWOdsjOobjhvJiU66Fh1q5BL8jIVDx27hUJW8HCYY8lNL7jnt3dtjpEn8wjqdrY9%2Fny1GCF3SafFd%2BAtQGFgTqjDy8Vb4SmQmxisMDY6iTkM%3D',
    # 'WM_NIKE': '9ca17ae2e6ffcda170e2e6eeb1ed50a9f0b9b0d221f7a88aa7c85f839e9e86db67ae869ad5fb68bce8af8dcc2af0fea7c3b92ab58fc0d9d96bb2bf89b7e55cab9cbe8dc852b1bc8b8fc8479591ac94e945adbea689f542ab8bfad7c564f3affba3cf34aa979aa5fb3af5b89babd6348c9d97babb688e94f98bed80f1bcbc8bf34faee8b98bf470b287f7d0ed73f3998da7b259a3ba8a85aa4bb88f89a7e660b3b68c9abb5ea2ec9d8ed467bcb7bdaec753f6b79c8cd037e2a3',
    # 'WM_TID': 'yhsa3SgV%2BHdFRFFEEBPTjzJVplxl9agd',
    # '__yadk_uid': '05Ivu3DmjXe8BLHwlQqsb0e8R2ziL2QL',
    # 'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1766587526',
}

headers = {
    # 'accept': '*/*',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    # 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    # 'dnt': '1',
    # 'edu-script-token': 'c17011b05edc4addba6f2bf3f34ebf0d',
    # 'origin': 'https://www.icourse163.org',
    # 'priority': 'u=1, i',
    # 'referer': 'https://www.icourse163.org/channel/2001.htm',
    # 'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-fetch-dest': 'empty',
    # 'sec-fetch-mode': 'cors',
    # 'sec-fetch-site': 'same-origin',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'NTESSTUDYSI=c17011b05edc4addba6f2bf3f34ebf0d; EDUWEBDEVICE=e49976bae49c4380a00b5483bd162e79; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1766587522; HMACCOUNT=D4F747A2F49A726E; WM_NI=wQp8ZaraGVfPiDrlEZsdEnEMWOdsjOobjhvJiU66Fh1q5BL8jIVDx27hUJW8HCYY8lNL7jnt3dtjpEn8wjqdrY9%2Fny1GCF3SafFd%2BAtQGFgTqjDy8Vb4SmQmxisMDY6iTkM%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb1ed50a9f0b9b0d221f7a88aa7c85f839e9e86db67ae869ad5fb68bce8af8dcc2af0fea7c3b92ab58fc0d9d96bb2bf89b7e55cab9cbe8dc852b1bc8b8fc8479591ac94e945adbea689f542ab8bfad7c564f3affba3cf34aa979aa5fb3af5b89babd6348c9d97babb688e94f98bed80f1bcbc8bf34faee8b98bf470b287f7d0ed73f3998da7b259a3ba8a85aa4bb88f89a7e660b3b68c9abb5ea2ec9d8ed467bcb7bdaec753f6b79c8cd037e2a3; WM_TID=yhsa3SgV%2BHdFRFFEEBPTjzJVplxl9agd; __yadk_uid=05Ivu3DmjXe8BLHwlQqsb0e8R2ziL2QL; Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b=1766587526',
}

params = {
    'csrfKey': 'c17011b05edc4addba6f2bf3f34ebf0d',
}

data = {
    'mocCourseQueryVo': '{"categoryId":-1,"categoryChannelId":2001,"orderBy":0,"stats":30,"pageIndex":2,"pageSize":20}',
}

response = requests.post(
    'https://www.icourse163.org/web/j/mocSearchBean.searchCourseCardByChannelAndCategoryId.rpc',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(json.dumps(response.json(), ensure_ascii=False))
