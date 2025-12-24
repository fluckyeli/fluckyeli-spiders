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
     -H 'dnt: 1' \
     -H 'origin: https://www.icourse163.org' \
     -H 'priority: u=1, i' \
     -H 'sec-ch-ua-mobile: ?0' \
     -H 'sec-ch-ua-platform: "Windows"' \
     -H 'sec-fetch-dest: empty' \
     -H 'sec-fetch-mode: cors' \
     -H 'sec-fetch-site: same-origin' \
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
