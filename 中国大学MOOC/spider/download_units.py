"""
下载指定课程的所有课件到本地
"""
import json
import os

import requests

from getLastLearnedMocTermDto import get_units
from spider_unit.get_unit_type1 import get_video_url_type_1
from spider_unit.get_unit_type3 import get_file_url_type_3
from spider_unit.get_unit_type4 import get_html_content_type_4
from spider_unit.get_unit_type5 import get_testing_type_5
from spider_unit.get_unit_type6 import get_forum_type_6
from 中国大学MOOC.spider.cookies.init_session import init_logined_session


def _down_unit(unit_id, content_id, content_type, filename):
    if content_type == 1:
        json_res = get_video_url_type_1(unit_id, content_id)
        mp4_url = json_res.get('mp4ShdUrl')
        if not mp4_url:
            mp4_url = json_res.get('mp4HdUrl')
        if not mp4_url:
            mp4_url = json_res.get('mp4SdUrl')

        if mp4_url:
            print(f'获取视频下载地址: {mp4_url}，正在下载...')
            with open(f'{filename}.mp4', 'wb') as f:
                f.write(requests.get(mp4_url).content)
        else:
            print(f'{filename} 视频下载地址获取失败，无法下载该单元。')

    elif content_type == 3:
        json_res = get_file_url_type_3(unit_id, content_id)
        file_url = json_res.get('textUrl')
        if not file_url:
            file_url = json_res.get('textOrigUrl')

        if file_url:
            print("获取文件下载地址:", file_url, "，正在下载...")
            file_extention = file_url.split('download=')[-1].split('&')[0].split('.')[-1]
            with open(f'{filename}.{file_extention}', 'wb') as f:
                file_response = requests.get(file_url)
                f.write(file_response.content)
        else:
            print(f'{filename} 文件下载地址获取失败，无法下载该单元。')

    elif content_type == 4:
        json_res = get_html_content_type_4(unit_id, content_id)
        html_content = json_res.get('htmlContent')
        if html_content:
            print(f'获取富文本内容，正在保存...')
            with open(f'{filename}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            print(f'{filename} 富文本内容获取失败，无法下载该单元。')

    elif content_type == 5:
        json_res = get_testing_type_5(unit_id, content_id)
        if json_res:
            print(f'获取测验内容，正在保存原始json...')
            with open(f'{filename}.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_res, ensure_ascii=False, indent=4))
        else:
            print(f'{filename} 测验内容获取失败，无法下载该单元。')


    elif content_type == 6:
        json_res = get_forum_type_6(unit_id, content_id)
        content = json_res.get('content')
        title = json_res.get('title')
        if content:
            print(f'获取讨论内容，正在html文件')
            with open(f'{filename}.html', 'w', encoding='utf-8') as f:
                f.write("<html><head><meta charset='utf-8'><title>")
                f.write(title)
                f.write("</title></head><body>")
                f.write(content)
                f.write("</body></html>")
        else:
            print(f'{filename} 讨论内容获取失败，无法下载该单元。')

    else:
        print(f'{filename} 下载时遇到未知的 content_type: {content_type}，无法下载该单元。')


def download_units(term_id, base_dir='./', session=None):
    if session is None:
        session = init_logined_session()

    res_json_units = get_units(term_id, session=session)
    chapters = res_json_units.get('result', {}).get('mocTermDto', {}).get('chapters', [])
    exams = res_json_units.get('result', {}).get('mocTermDto', {}).get('exams', [])
    for chapter in chapters:
        chapter_name = chapter.get('name', 'unknown_chapter')
        chapter_dir = os.path.join(base_dir, chapter_name)
        os.mkdir(chapter_dir)
        print(f'创建文件夹 : {chapter_dir}')
        lessons = chapter.get('lessons', [])
        for lesson in lessons:
            lesson_name = lesson.get('name', 'unknown_lesson')
            lesson_dir = os.path.join(chapter_dir, lesson_name)
            os.mkdir(lesson_dir)
            print('-- 创建文件夹 :', lesson_dir)
            units = lesson.get('units', [])
            for unit in units:
                unit_id = unit.get('id')
                content_id = unit.get('contentId')
                content_type = unit.get('contentType')
                unit_name = unit.get('name', '未知资源')
                unit_file_name = os.path.join(lesson_dir, unit_name)
                print(f'---- 下载 unit: {unit_name} (ID: {unit_id}, Content ID: {content_id}, Type: {content_type})')
                _down_unit(unit_id, content_id, content_type, unit_file_name)


if __name__ == '__main__':
    test_term_id = '2024012345'  # 替换为实际的term_id进行测试
    download_units(test_term_id)
