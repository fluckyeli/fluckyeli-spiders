"""
下载指定课程的所有课件到本地
"""
import json
import os
import sys

from getLastLearnedMocTermDto import get_units
from spider_unit.down_mooc_m3u8 import down_m3u8_mooc
from spider_unit.get_unit_type1 import get_video_url_type_1
from spider_unit.get_unit_type3 import get_file_url_type_3
from spider_unit.get_unit_type4 import get_html_content_type_4
from spider_unit.get_unit_type5 import get_testing_type_5
from spider_unit.get_unit_type6 import get_forum_type_6
from 中国大学MOOC.spider.cookies.init_session import init_logined_session
from 中国大学MOOC.spider.spider_unit.download_utils import simple_download


def _clean_filename(filename):
    # 去除文件名不允许的特殊字符
    return (filename.replace('？', '').replace('：', '').replace('、', '').replace('，', '').replace('！', '')
            .replace('*', '').replace('"', '').replace('<', '').replace('>', '')
            .replace('|', '').replace('\\', '').replace('/', '').strip())


def _mkdir(base, dir):
    # 去除文件夹不允许的特殊字符
    cleaned_dir = _clean_filename(dir)
    path_dir = os.path.join(base, cleaned_dir)
    is_exists = os.path.exists(path_dir)
    if not is_exists:
        os.makedirs(path_dir)
        print(f'创建文件夹 : {path_dir}')
        return path_dir
    else:
        print(f'文件夹 {path_dir} 已存在。')
        return path_dir


def _join_path(base, filename):
    cleaned_filename = _clean_filename(filename)
    return os.path.join(base, cleaned_filename)


def _down_unit(unit_id, content_id, content_type, filename):
    if content_type == 1:
        if os.path.exists(f'{filename}.mp4') or os.path.exists(f'{filename}.flv'):
            print(f'文件 {filename}.mp4 已存在，跳过下载。')
            return
        json_res = get_video_url_type_1(unit_id, content_id)
        mp4_url = json_res.get('mp4ShdUrl')
        if not mp4_url:
            mp4_url = json_res.get('mp4HdUrl')
        if not mp4_url:
            mp4_url = json_res.get('mp4SdUrl')

        if mp4_url:
            print(f"正在下载 {filename}.mp4 视频...")
            simple_download(url=mp4_url, file_path=f'{filename}.mp4')
        else:
            # 没有 mp4 视频地址，尝试下载 m3u8 视频
            down_m3u8_mooc(unit_id, f'{filename}')

    elif content_type == 3:
        json_res = get_file_url_type_3(unit_id, content_id)
        file_url = json_res.get('textUrl')
        if not file_url:
            file_url = json_res.get('textOrigUrl')

        if file_url:
            file_extention = file_url.split('download=')[-1].split('&')[0].split('.')[-1]

            if os.path.exists(f'{filename}.{file_extention}'):
                print(f'文件 {filename}.{file_extention} 已存在，跳过下载。')
                return
            print(f"正在下载 {filename}.{file_extention} 文件...")
            simple_download(url=file_url, file_path=f'{filename}.{file_extention}')
        else:
            print(f'{filename} 文件下载地址获取失败，无法下载该单元。')

    elif content_type == 4:
        if os.path.exists(f'{filename}.html'):
            print(f'文件 {filename}.html 已存在，跳过下载。')
            return
        json_res = get_html_content_type_4(unit_id, content_id)
        html_content = json_res.get('htmlContent')
        if html_content:
            print(f'获取富文本内容，正在保存 {filename}.html 文件...')
            with open(f'{filename}.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            print(f'{filename} 富文本内容获取失败，无法下载该单元。')

    elif content_type == 5:
        if os.path.exists(f'{filename}.json'):
            print(f'文件 {filename}.json 已存在，跳过下载。')
            return
        json_res = get_testing_type_5(unit_id, content_id)
        if json_res:
            print(f'获取测验内容，正在保存 {filename}.json 文件...')
            with open(f'{filename}.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_res, ensure_ascii=False, indent=4))
        else:
            print(f'{filename} 测验内容获取失败，无法下载该单元。')

    elif content_type == 6:
        if os.path.exists(f'{filename}.html'):
            print(f'文件 {filename}.html 已存在，跳过下载。')
            return
        json_res = get_forum_type_6(unit_id, content_id)
        content = json_res.get('content')
        title = json_res.get('title')
        if content:
            print(f'获取讨论内容，正在保存 {filename}.html 文件...')
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
    course_name = res_json_units.get('result', {}).get('mocTermDto', {}).get('courseName', term_id)
    base_dir = _mkdir(base_dir, course_name)
    moc_term_dto = res_json_units.get('result', {}).get('mocTermDto') or {}
    chapters = moc_term_dto.get('chapters') or []
    exams = moc_term_dto.get('exams') or []
    for chapter in chapters:
        chapter_name = chapter.get('name', 'unknown_chapter')
        chapter_dir = _mkdir(base_dir, chapter_name)
        lessons = chapter.get('lessons') or []
        for lesson in lessons:
            lesson_name = lesson.get('name', 'unknown_lesson')
            lesson_dir = _mkdir(chapter_dir, lesson_name)
            units = lesson.get('units') or []
            for unit in units:
                unit_id = unit.get('id')
                content_id = unit.get('contentId')
                content_type = unit.get('contentType')
                unit_name = unit.get('name', '未知资源')
                unit_file_name = _join_path(lesson_dir, unit_name)
                print(f'---- 下载 unit: {unit_file_name} ----')
                try:
                    _down_unit(unit_id, content_id, content_type, unit_file_name)
                except Exception as e:
                    print(f'下载单元 {unit_file_name} 时出错: {e}', file=sys.stderr)
                    sys.exit(-1)


if __name__ == '__main__':
    # test_term_id = '1475968443'  # 程序设计入门——C语言
    # test_term_id = '1475637487'  # 一刻钟学会：游戏开发基础
    test_term_id = '1475140442'  # 人工智能：模型与算法
    download_units(test_term_id)
