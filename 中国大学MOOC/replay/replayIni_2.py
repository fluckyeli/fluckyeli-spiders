import requests

# cookies = {
#     # 'NTESSTUDYSI': '8a7f1da7ea794d93b370a45bffad5147',
#     # 'EDUWEBDEVICE': 'feee490a55214d90a38a19c8aa1857e3',
#     # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1765776070,1765859451,1765973026,1765973097',
#     # 'Hm_lpvt_77dc9a9d49448cf5e629e5bebaa5500b': '1765976198',
#     # 'utid': 'JNeeSpyoNZ0AFzdPqjIJits5Kxksc6RL',
#     # 'ntes_zc_cid': 'bc32867e-57db-4882-8d20-2e80b0f44a43',
#     # 'ntes_zc_yd_cjJVGQM': '55894076A71C69C5C056693A6972CF712A5006CAFD5FDEF009C18D28F5D930BCC4358F767815991455730965B1F7AE9EF79F4DC083D2E18F53F9159EACDA462C660D3F06D0D94B63BC2AC005C6CFDFC5',
# }
#
# headers = {
#     'Accept': '*/*',
#     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
#     'Connection': 'keep-alive',
#     'Content-Type': 'application/json',
#     'DNT': '1',
#     'Origin': 'https://reg.icourse163.org',
#     'Referer': 'https://reg.icourse163.org/webzj/v1.0.1/pub/index_dl2_new.html?cd=%2F%2Fcmc.stu.126.net%2Fu%2Fcss%2Fcms%2F&cf=mooc_urs_login_css.css&MGID=1765976209999.4688&wdaId=UA1438236666413&pkid=cjJVGQM&product=imooc&cdnhostname=webzj.netstatic.net',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
#     'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
# }

json_data = {
    'encParams': '746628c1d80daa15585d90cadd41445fd80bd7c73126c9a49623be514a07a27ed1d900d63d125921f6a73ffdb7c64bf5afdf726003252c5af61bed0fadd5ae40b1e6cecd5374623a7bd48e37ec5e9c62db7e2de2428e97521b82319f78d8813a464277ddb9fc049e063505c072f81910d9dbbad582dea77c1a306554d3dce05106aa3f20e31fe0f9626f4e207cc2dc6f52e51d25bce0cc644589e491271bece9',
}
# {"pd":"imooc","pkid":"cjJVGQM","pkht":"www.icourse163.org","channel":1,"topURL":"https://www.icourse163.org/","rtid":"da7tV6dfP3EwXkQGqkRwqzyOxfqNlzqi"}

response = requests.post('https://reg.icourse163.org/dl/zj/yd/ini', json=json_data)
print(response.headers.get('Set-Cookie'))