import json
import random
import time
import os

from 中国大学MOOC.spider.join_course.startTermLearn import join_term_learn

"""
参加所有课程的脚本
"""


def join_lessions(filename):
    def _join_term(current_term_id):
        learn_id = join_term_learn(current_term_id)
        return learn_id

    base_url = 'https://www.icourse163.org/learn'
    res_filename = f'{filename.split('.')[0]}_join_lessions.log'
    start_index = 0
    if os.path.exists(res_filename):
        # 不是第一次执行（log文件存在）
        with open(res_filename, 'r', encoding='utf-8') as f_start_index:
            last_line = f_start_index.readlines()[-1]
            start_index = int(last_line.split('|||')[0].split('/')[0])  # [之前已到的序列号]从第492个课程开始参加

    with open(res_filename, 'a', encoding='utf-8') as fw:
        with open(filename, 'r', encoding='utf-8') as fr:
            json_list = json.load(fr)
        sum_count = len(json_list)
        json_list = json_list[start_index:]
        current_count = start_index
        for item in json_list:
            # print(json.dumps(item, ensure_ascii=False))
            current_count += 1
            time.sleep(random.randint(1, 3))
            mocCourseBaseCardVo = item['mocCourseBaseCardVo']
            if not mocCourseBaseCardVo:
                print("课程加入异常:",json.dumps(item, ensure_ascii=False))
                continue
            lession_id = mocCourseBaseCardVo['id']
            lession_name = mocCourseBaseCardVo['name']
            schoolName = mocCourseBaseCardVo['schoolName']
            schoolSN = mocCourseBaseCardVo['schoolSN']
            currentTermId = mocCourseBaseCardVo['currentTermId']
            # closeVisableStatus = mocCourseBaseCardVo['closeVisableStatus'] # 1已关闭选课，0未关闭。并不完全正确
            lession_url = f'{base_url}/{schoolSN}-{lession_id}'
            try:
                learn_id = _join_term(currentTermId)
                if learn_id:
                    fw.write(
                        f'{current_count}/{sum_count}|||成功参加课程【{schoolName}】《{lession_name}》|||{lession_url}\n')
                    print(
                        f'{current_count}/{sum_count}|||成功参加课程【{schoolName}】《{lession_name}》|||{lession_url}\n')
                else:
                    fw.write(
                        f'{current_count}/{sum_count}|||参加课程【{schoolName}】《{lession_name}》失败|||{lession_url}\n')
                    print(
                        f'{current_count}/{sum_count}|||参加课程【{schoolName}】《{lession_name}》失败|||{lession_url}\n')
            except Exception as e:
                fw.write(
                    f'{current_count}/{sum_count}|||参加课程【{schoolName}】《{lession_name}》失败，原因{str(e).replace("\n", " ")}\n')
                print(
                    f'{current_count}/{sum_count}|||参加课程【{schoolName}】《{lession_name}》失败，原因{str(e).replace("\n", "")}\n')


if __name__ == '__main__':
    filename = '经济管理3004.json'
    join_lessions(filename)
