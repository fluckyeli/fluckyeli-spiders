import shlex
import json
from typing import Dict, Any
from urllib.parse import urlparse, parse_qs


class CurlParser:
    """
    一个用于解析 curl 命令字符串，并提取所有关键请求组件（headers, cookies, data, params）的工具类。
    """

    @staticmethod
    def _parse_cookie_string(cookie_line: str) -> Dict[str, str]:
        """解析分号分隔的 cookie 字符串为字典。"""
        cookies: Dict[str, str] = {}
        for cookie_part in cookie_line.split(';'):
            if '=' in cookie_part:
                name, value = cookie_part.split('=', 1)
                cookies[name.strip()] = value.strip()
        return cookies

    @staticmethod
    def parse(curl_command: str) -> Dict[str, Any]:
        """
        解析 curl 命令并返回结构化的请求组件。

        Args:
            curl_command (str): 待解析的 curl 命令字符串。

        Returns:
            Dict[str, Any]: 包含 'url', 'method', 'headers', 'cookies', 'params', 'data' 的字典。
        """
        if not curl_command.strip().startswith('curl'):
            return {"error": "Input does not appear to be a curl command."}

        # 1. 使用 shlex.split 安全地分割 curl 命令参数
        try:
            command_parts = shlex.split(curl_command)
        except ValueError as e:
            return {"error": f"Error splitting curl command with shlex: {e}"}

        # 2. 初始化结果字典
        result: Dict[str, Any] = {
            "url": None,
            "method": "GET",
            "headers": {},
            "cookies": {},
            "params": {},
            "data": None
        }

        # 3. 解析参数
        i = 0
        while i < len(command_parts):
            part = command_parts[i]

            # URL
            if i == 1 and not part.startswith('-'):
                result['url'] = part
                i += 1
                continue

            # 头部 (-H, --header)
            if part in ('-H', '--header'):
                i += 1
                if i < len(command_parts):
                    header_line = command_parts[i]
                    if ':' in header_line:
                        name, value = header_line.split(':', 1)
                        result['headers'][name.strip()] = value.strip()
                i += 1
                continue

            # 数据 (-d, --data, --data-raw)
            if part in ('-d', '--data', '--data-raw'):
                result['method'] = "POST"
                i += 1
                if i < len(command_parts):
                    result['data'] = command_parts[i]
                i += 1
                continue

            # Cookie (-b, --cookie)
            if part in ('-b', '--cookie'):
                i += 1
                if i < len(command_parts):
                    cookie_line = command_parts[i]
                    result['cookies'] = CurlParser._parse_cookie_string(cookie_line)
                i += 1
                continue

            # 请求方法 (-X, --request)
            if part in ('-X', '--request'):
                i += 1
                if i < len(command_parts):
                    result['method'] = command_parts[i].upper()
                i += 1
                continue

            i += 1

        # 4. 提取 URL 中的查询参数 (params)
        if result['url']:
            parsed_url = urlparse(result['url'])
            # parse_qs 返回的字典中值是列表，需要转换为普通字符串
            query_params = parse_qs(parsed_url.query)
            result['params'] = {k: v[0] for k, v in query_params.items()}

            # 清理 URL，只保留路径部分，以防requests重复编码
            result['url'] = parsed_url._replace(query="").geturl()

        return result


if __name__ == '__main__':
    # --- 示例调用 ---
    # 使用你提供的 curl 命令
    curl_example = """
    curl 'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc?csrfKey=8fa221231scxz85' \
     -H 'accept: */*' \
     -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
     -H 'content-type: application/x-www-form-urlencoded' \
     -b 'EDUWEBDEVICE=31a6781251ae412d832a20ffa003e2f7; WM_TID=vVBEgBVXdohFRUEBBFaGmO%2B4VnNylwxi; __yadk_uid=rSt3LWMcwYBpO7kfhd6KytOYyg5yKdia; Hm_lvt_77dc9a9d49448cf5e629e5bebaa5500b=1765199403,1765282575; hasVolume=true; videoVolume=0.8; videoRate=1.25; videoResolutionType=1; WM_NI=IN2Uu7pkSor%2B1fgYFeC7y4pOFKy04YG7GLBmcLhxnuW93OU3MMDIfJv2ZqT%2BmXDNWwls3Jc65SIMMd9bWN24kA0b5FTt8dAPFxJ5LrFGfaajAShCnligsEfN6ucy%2BlY7RjU%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee89e25c9389f998c174b7968ab6d44a879e8a83c663f39297b9c26d8ef0fa89f82af0fea7c3b92a8b92feb6f83db4b59d90f121f3baa9bac56f81e9b7d5f3458695b7d1b75385e989adc167a194a899ed7f95e7fdb0d8398f938caae542b6ee9692d721af888cafd67db0adfdabe23ef78d87aed070fbbe99afb140a99f0083b84e98acf885c45c86a886d6cf7a8699aa82e462838da8a4ed68abb9bda6e546f6abad9aaa689be99e8bd837e2a3; close_topBar=1; NTESSTUDYSI=8fa9a1c811d34586af7c596775994c85; NTES_SESS=L8Rj0vgu1PctEuGGocneASmhjWVWd4CZ9MAMIjFo7iB8_Z1KTnM7g6MW0mNLmV0ZsfIS9NBfG8m_pceYT.S3F38Pasy13dvlRZcDWOTwT_Z.LOGawhHfjyne4mnO65.b1RkIbostlVg_Ps380O6InVw8GFuR9nQDbYbjv9mK0UkyC3P.FomLbdehDh6.d9wVUvtiWN6muN1OK; NTES_PASSPORT=HXNW_uiax59KKAPNEhoVoutaIK5Iphxasq7Uw0U5n6qMEIxj1sXN8MXAkuFKuWkI.pLaIJFvf.kGG.Lt77w0_5ApRnOzl26ltpvbitNBF_K5Wb72APykwTPPQvH53C8d8RU_FcqiQdZQeaSdd_7lNvnCQxj_3nMslXNz2QzxeE4BjMuy1cLvVe3M6; STUDY_INFO="ocean_yyl@163.com|-1|1024616784|1765538930006"; STUDY_SESS="CkRzH3oHpH+78iv53u8gsPRgUR1QLGfbhj4z2VY0HGKdbTTx1G/+rs1VHEyXQz/xw8VMk2jxXggJbFEyVM1Pjfv5GVWv326h9xRqsOevsE/zdm4iSMRh9K2N7WLs9AcYWePoU8bG2zXQToe3yWoy4gwc//ohDGUgt8WFvF0L/Osnppr6KrivyjY6FmKs/Qou"; STUDY_PERSIST="dKmEJ3j368/l9gVjCtzSf5rJVeYxUIjP8gdXnmc72Yulh2VTociZwW4Q4yRPs4FzA1U3WiGPUTN6+JrTEC+ndtvKMKXSbA2QLe1pUWnPwVsggObGtjQJ3DtQIM8cH7mGKRADuR8zdu0lIaWt1bkV4n4/mjOm3SKKAzzwkab4ou0caXpq7dtBP5dvMR4BRaLRW6VpawEB5R17LKJP7oRILs0UT5ZbkLdEmUMvyjb2d6JOSdFA6J5jrZLCRv8JU8qN8WQLi3xTJ45sq/acjsEWiA=="; NETEASE_WDA_UID=1024616784#|#1488366520887; MOOC_PRIVACY_INFO_APPROVED=true' \
     -H 'dnt: 1' \
     -H 'edu-script-token: 8fa9a1c811d34586af7c596775994c85' \
     -H 'origin: https://www.icourse163.org' \
     -H 'priority: u=1, i' \
     -H 'sec-ch-ua-mobile: ?0' \
     -H 'sec-ch-ua-platform: "Windows"' \
     -H 'sec-fetch-dest: empty' \
     -H 'sec-fetch-mode: cors' \
     -H 'sec-fetch-site: same-origin' \
     -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36' \
     --data-raw 'termId=1475968443'
    """

    parsed_data = CurlParser.parse(curl_example)

    print("### 📦 解析结果结构化数据：\n")
    print(json.dumps(parsed_data, indent=4, ensure_ascii=False))

    print("\n--- 关键组件提取 ---")
    print(f"URL (不含查询参数): {parsed_data['url']}")
    print(f"请求方法: {parsed_data['method']}")
    print(f"查询参数 (params): {parsed_data['params']}")
    print(f"请求头 (headers) 数量: {len(parsed_data['headers'])}")
    print(f"Cookies 数量: {len(parsed_data['cookies'])}")
    print(f"原始请求体 (data): {parsed_data['data']}")
