import requests

cookies = {
    # 'EDUWEBDEVICE': '1f69e68e2d9c466b91b8883efbd63b12',
    # 'Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b': '1765289499',
    # 'utid': 'yd0rkTPAaxGfRdIATjpDosx6ZVeXXZ6S',
    # 'NTES_WEB_FP': '6d57e82ceabb1b924feb80dd9e2a995d',
    # 'ntes_zc_cid': 'f337abd2-5a4a-4ecb-b604-4047f58014ff',
    # 'THE_LAST_LOGIN': 'ocean_yyl@163.com',
    # 'MOOC_PRIVACY_INFO_APPROVED': 'true',
    # 'NTESSTUDYSI': 'b4accc28e43a460abea03a38b8ec983b',
    # 'ntes_zc_yd_cjJVGQM': '55894076A71C69C5C056693A6972CF712A5006CAFD5FDEF009C18D28F5D930BC6DA9430A9F76BD3682B0812CFF2090F20A015A74DEC6AAF193F25CA775206961477D522BA45E34F3E442FBFDDFD3CA13',
    # 'l_yd_s_imooccjJVGQM': '55894076A71C69C5C056693A6972CF712A5006CAFD5FDEF009C18D28F5D930BC6DA9430A9F76BD3682B0812CFF2090F236FC35A5A37A9617BDCC3CACCE7DCDC7FC5A21D7A118DB9DB800E12A115046BE8D0D23A659F9CBA3B5ADAA31E716385FB507F1650343597299388D82EE369C33',
    'l_s_imooccjJVGQM': '55894076A71C69C5C056693A6972CF712A5006CAFD5FDEF009C18D28F5D930BC6DA9430A9F76BD3682B0812CFF2090F256D3B3A7B12C60130708637F93A5142A1EA0E4380F7BDADD58BA766CE76B36F3417215F6568696E00EFBE91E9AA7BC561003075CAEC1967CE7923EE538AC8E8F',
}

headers = {
    # 'Accept': '*/*',
    # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    # 'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'DNT': '1',
    # 'Origin': 'https://reg.icourse163.org',
    # 'Referer': 'https://reg.icourse163.org/webzj/v1.0.1/pub/index_dl2_new.html?cd=%2F%2Fcmc.stu.126.net%2Fu%2Fcss%2Fcms%2F&cf=mooc_urs_login_css.css&MGID=1766202302280.2288&wdaId=UA1438236666413&pkid=cjJVGQM&product=imooc&cdnhostname=webzj.netstatic.net',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'same-origin',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'sec-ch-ua': '"Microsoft Edge";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    # 'sec-ch-ua-mobile': '?0',
    # 'sec-ch-ua-platform': '"Windows"',
    # 'sec-gpc': '1',
}

json_data = {
    'encParams': 'ed72279d0e51430a02d946f482f3f26ef55fe67674fce34b9c0f09f4b0c2e7cbfbb302f361b69dfae639d48f839abf7f3520d346ebea5c6d7fb9914d66d0c5993af0176b1c7f13691d1286f4e51310c0c05db0f66823c415890640128efd23e068710144d49e906b482e0d96e130b65cc6d30b1396a35c5d7121ffa0c09320dc',
}

response = requests.post('https://reg.icourse163.org/dl/zj/mail/powGetP', cookies=cookies, headers=headers, json=json_data)

print(response.text)