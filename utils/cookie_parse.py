import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import re


class CookieParser:
    """Cookie解析器，支持Set-Cookie格式与JSON格式互转"""

    @staticmethod
    def parse_cookie_string(cookie_str: str) -> List[Dict[str, Any]]:
        """
        解析Set-Cookie格式字符串为字典列表

        Args:
            cookie_str: Cookie字符串，如 "name=value; Domain=example.com; Path=/"

        Returns:
            Cookie字典列表，每个字典代表一个cookie
        """
        if not cookie_str:
            return []

        cookies = []
        # 分割多个cookie，注意用逗号分隔，但需要考虑Expires中的逗号
        # 简单的分割方式：按 "), " 分割，因为每个cookie通常以Path=/结尾
        cookie_parts = re.split(r'/, (?=\w+=)', cookie_str)

        for cookie_part in cookie_parts:
            # 确保以/结尾的cookie补上逗号
            if not cookie_part.endswith('/'):
                cookie_part = cookie_part + '/'

            cookie_dict = {}
            # 分割属性和值
            attributes = re.split(r';\s*', cookie_part.strip())

            # 第一个是name=value
            if attributes and '=' in attributes[0]:
                name_value = attributes[0].split('=', 1)
                cookie_dict['name'] = name_value[0]
                cookie_dict['value'] = name_value[1]

                # 处理其他属性
                for attr in attributes[1:]:
                    if not attr:
                        continue

                    if '=' in attr:
                        key, value = attr.split('=', 1)
                        key = key.strip().lower()

                        # 处理特殊属性
                        if key == 'expires':
                            # 尝试解析日期
                            try:
                                # 转换为标准ISO格式
                                dt = datetime.strptime(value, '%a, %d-%b-%Y %H:%M:%S GMT')
                                cookie_dict['expires'] = dt.isoformat() + 'Z'
                            except:
                                cookie_dict['expires'] = value
                        elif key == 'max-age':
                            cookie_dict['max_age'] = int(value)
                        else:
                            cookie_dict[key] = value
                    else:
                        # 布尔属性，如HttpOnly, Secure
                        cookie_dict[attr.strip().lower()] = True

            if cookie_dict:
                cookies.append(cookie_dict)

        return cookies

    @staticmethod
    def parse_cookie_to_json(cookie_str: str) -> str:
        """
        解析Cookie字符串为JSON格式

        Args:
            cookie_str: Cookie字符串

        Returns:
            JSON格式的字符串
        """
        cookies = CookieParser.parse_cookie_string(cookie_str)
        return json.dumps(cookies, indent=2, ensure_ascii=False)

    @staticmethod
    def cookies_to_dict(cookies: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        将cookie列表转换为以name为key的字典

        Args:
            cookies: Cookie字典列表

        Returns:
            以cookie名称为key的嵌套字典
        """
        result = {}
        for cookie in cookies:
            name = cookie.get('name')
            if name:
                # 移除name字段，将其他属性作为值
                cookie_copy = cookie.copy()
                cookie_value = cookie_copy.pop('value', '')
                result[name] = {
                    'value': cookie_value,
                    **cookie_copy
                }
        return result

    @staticmethod
    def dict_to_cookie_string(cookie_dict: Dict[str, Dict[str, Any]]) -> str:
        """
        将cookie字典转换回Set-Cookie格式字符串

        Args:
            cookie_dict: Cookie字典，格式为 {name: {attributes}}

        Returns:
            Set-Cookie格式字符串
        """
        cookie_strings = []

        for name, attrs in cookie_dict.items():
            parts = [f"{name}={attrs.get('value', '')}"]

            # 添加其他属性（按常见顺序）
            domain = attrs.get('domain') or attrs.get('Domain')
            if domain:
                parts.append(f"Domain={domain}")

            expires = attrs.get('expires') or attrs.get('Expires')
            if expires:
                # 如果是ISO格式，转换为GMT格式
                try:
                    if 'Z' in expires or '+' in expires:
                        dt = datetime.fromisoformat(expires.replace('Z', '+00:00'))
                        gmt_str = dt.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
                        parts.append(f"Expires={gmt_str}")
                    else:
                        parts.append(f"Expires={expires}")
                except:
                    parts.append(f"Expires={expires}")

            max_age = attrs.get('max_age') or attrs.get('max-age')
            if max_age is not None:
                parts.append(f"Max-Age={max_age}")

            path = attrs.get('path') or attrs.get('Path', '/')
            parts.append(f"Path={path}")

            # 布尔属性
            if attrs.get('secure') or attrs.get('Secure'):
                parts.append("Secure")
            if attrs.get('httponly') or attrs.get('HttpOnly'):
                parts.append("HttpOnly")
            if attrs.get('samesite') or attrs.get('SameSite'):
                samesite = attrs.get('samesite') or attrs.get('SameSite')
                parts.append(f"SameSite={samesite}")

            cookie_strings.append("; ".join(parts))

        return ", ".join(cookie_strings)

    @staticmethod
    def json_to_cookie_string(json_str: str) -> str:
        """
        将JSON字符串转换回Set-Cookie格式

        Args:
            json_str: JSON格式的cookie字符串

        Returns:
            Set-Cookie格式字符串
        """
        try:
            data = json.loads(json_str)
            if isinstance(data, list):
                cookie_dict = {}
                for cookie in data:
                    name = cookie.get('name')
                    if name:
                        cookie_dict[name] = cookie
                return CookieParser.dict_to_cookie_string(cookie_dict)
            elif isinstance(data, dict):
                return CookieParser.dict_to_cookie_string(data)
            else:
                raise ValueError("Invalid JSON format")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string")

    @staticmethod
    def parse_simple_cookie(cookie_str: str) -> Dict[str, str]:
        """
        解析简单的Cookie字符串（只有name=value对）

        Args:
            cookie_str: 简单的Cookie字符串，如 "name1=value1; name2=value2"

        Returns:
            简单的name-value字典
        """
        result = {}
        if not cookie_str:
            return result

        pairs = cookie_str.split(';')
        for pair in pairs:
            pair = pair.strip()
            if '=' in pair:
                name, value = pair.split('=', 1)
                result[name.strip()] = value.strip()

        return result


# 使用示例
if __name__ == "__main__":
    # 示例Cookie字符串
    cookie_string = "NTESSTUDYSI=78563e284471489699c1378237a0d0ba; Domain=icourse163.org; Path=/, EDUWEBDEVICE=82aa1e25957948d88740df1f76254e07; Domain=icourse163.org; Expires=Sun, 22-Dec-2030 09:23:46 GMT; Path=/"

    parser = CookieParser()

    # 1. 解析为字典列表
    print("1. 解析为字典列表:")
    cookies_list = parser.parse_cookie_string(cookie_string)
    for cookie in cookies_list:
        print(f"  - {cookie}")

    # 2. 解析为JSON
    print("\n2. 转换为JSON:")
    json_output = parser.parse_cookie_to_json(cookie_string)
    print(json_output)

    # 3. 转换为嵌套字典格式
    print("\n3. 转换为嵌套字典格式:")
    nested_dict = parser.cookies_to_dict(cookies_list)
    print(json.dumps(nested_dict, indent=2, ensure_ascii=False))

    # 4. 将嵌套字典转换回Cookie字符串
    print("\n4. 转换回Cookie字符串:")
    new_cookie_string = parser.dict_to_cookie_string(nested_dict)
    print(new_cookie_string)

    # 5. 解析简单Cookie
    print("\n5. 解析简单Cookie:")
    simple_cookie = "session_id=abc123; user_id=456; token=xyz789"
    simple_dict = parser.parse_simple_cookie(simple_cookie)
    print(simple_dict)

    # 6. JSON转Cookie字符串
    print("\n6. JSON转Cookie字符串:")
    test_json = '''[
        {
            "name": "SESSION",
            "value": "abc123def456",
            "domain": "example.com",
            "path": "/",
            "expires": "2030-12-31T23:59:59Z",
            "secure": true,
            "httponly": true
        }
    ]'''
    cookie_from_json = parser.json_to_cookie_string(test_json)
    print(cookie_from_json)