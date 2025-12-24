from utils.curl_parser import CurlParser
import requests

with open("../中国大学MOOC/curl_cmd.tmp", encoding="utf-8") as fr:
    cur_cmd = fr.read()

parsed_data = CurlParser.parse(cur_cmd)


response = requests.post(
    'https://www.icourse163.org/web/j/courseBean.getLastLearnedMocTermDto.rpc',
    params=parsed_data.get('params', {}),
    headers=parsed_data.get('headers', {}),
    cookies=parsed_data.get('cookies', {}),
    data=parsed_data.get('data', {})
)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Request failed with status code: {response.status_code}")
