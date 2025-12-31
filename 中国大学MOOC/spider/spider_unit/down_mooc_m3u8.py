import time
from 中国大学MOOC.spider.cookies.init_session import init_logined_session
from utils.m3u8_download_utils import run_n_m3u8dl_cli
import hashlib


def _tokenEncrypt_python(bizId, bizType, contentType, timestamp, window_id=""):
    """
    Python 简化版本
    参数:
    c: 任何对象，会转换为字符串
    d: 字符串，会转换为小写
    e: 字符串
    f: 任何对象，会取长度
    window_id: 可选的窗口ID,原js中的 var h
    # var h = window['localStorage'] && window['sessionStorage']['id'] ? window['localStorage']['id'] : '';
    """
    # 转换为字符串
    c_str = str(bizId)
    d_lower = str(bizType).lower()
    f_len = len(str(timestamp))

    # 构建待加密字符串
    plaintext = f"{c_str}{d_lower}{f_len}88{contentType}|{window_id}"

    # MD5 哈希
    return hashlib.md5(plaintext.encode('utf-8')).hexdigest()

def down_m3u8_mooc(unit_id='1305160316',filename='down.mp4'):
    session = init_logined_session()

    bizId = unit_id  # unit_id
    bizType = '1'
    contentType = '1'
    timestamp = str(int(time.time() * 1000))
    data = {
        'bizId': bizId,
        'bizType': bizType,
        'contentType': contentType,
        'sign': _tokenEncrypt_python(bizId, bizType, contentType, timestamp),
        'timestamp': timestamp
    }

    cookie_dict = {cookie.name: cookie.value for cookie in session.cookies}

    csrf_key = cookie_dict.get('NTESSTUDYSI')

    response = session.post(
        'https://www.icourse163.org/web/j/resourceRpcBean.getResourceTokenV2.rpc',
        params={'csrfKey': csrf_key},
        data=data,
    )

    # print(response.text)
    resource_token_v_2 = response.json()
    video_sign_dto = resource_token_v_2.get('result').get('videoSignDto') or {}
    videoId = video_sign_dto.get('videoId')
    duration = video_sign_dto.get('duration')
    signature = video_sign_dto.get('signature')
    name = video_sign_dto.get('name')

    params = {
        'videoId': videoId,
        'signature': signature,
        'clientType': '1',
    }

    response = session.get('https://vod.study.163.com/eds/api/v1/vod/video', params=params)

    res_json = response.json()
    # print(response.text)
    videoUrl = res_json.get('result').get('videos')[-1].get('videoUrl')
    run_n_m3u8dl_cli(url=videoUrl, work_dir='',save_name='')

if __name__ == '__main__':
    down_m3u8_mooc(unit_id='1305160317')