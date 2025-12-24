import requests

cookies = {
    'l_s_imooccjJVGQM': '55894076A71C69C5C056693A6972CF712A5006CAFD5FDEF009C18D28F5D930BCBDC2DB08727A1639187093BCCDAA03F70220B41DF63833B6D46E5073A101062D2BC2A143665EA475E45030B8B00A0E87C661ACC07713733C55D0E97AF0EE78F1F0D05AF93A8FF220D7039815520EDA0F',
}

# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json',
#     'DNT': '1',
#     'Origin': 'https://reg.icourse163.org',
#     'Referer': 'https://reg.icourse163.org/webzj/v1.0.1/pub/index_dl2_new.html?cd=%2F%2Fcmc.stu.126.net%2Fu%2Fcss%2Fcms%2F&cf=mooc_urs_login_css.css&MGID=1765970382288.0518&wdaId=UA1438236666413&pkid=cjJVGQM&product=imooc&cdnhostname=webzj.netstatic.net',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

json_data = {
    'encParams': '84497406fe47bded5c26fa9830987a1805fba2d219a6e33487ca832496b52e9446e4e056b148bea9abc9f92e68c95d2affb27ab846cf0c899d0f2d2daea194d715613de33180163a69a798b6d0f688bec91434545c835b8776a6c50c37a0e625d06bdff306aca79a25f41985c4048ceea43d8bf65c0b57ac5203187462376c4d86c83b374357721c3e294b5ec213b4c96529a7a2206da3d39738235b1370ff09',
    #  {"un":"test123@163.com","pkid":"cjJVGQM","pd":"imooc","channel":0,"topURL":"https://www.icourse163.org/","rtid":"Vw0Vm75kYdHiDVNjZRRwi1iKGmqhZs9r"}
}


# response = requests.post('https://reg.icourse163.org/dl/zj/mail/gt', cookies=cookies, headers=headers, json=json_data)
response = requests.post('https://reg.icourse163.org/dl/zj/mail/gt', cookies=cookies,json=json_data)

print(response.text)