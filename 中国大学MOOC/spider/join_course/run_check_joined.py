import json
import random
import time
import os

from 中国大学MOOC.spider.join_course.startTermLearn import join_term_learn
from 中国大学MOOC.spider.join_course.checkTermLearn import check_term_learned

"""
check 所有课程是否参加的脚本
"""
def check_joined(filename):
    base_url = 'https://www.icourse163.org/learn'
    res_filename = f'{filename.split('.')[0]}_check_joined.log'
    start_index = 0
    if os.path.exists(res_filename):
        # 不是第一次执行（log文件存在）
        with open(res_filename, 'r', encoding='utf-8') as f_start_index:
            last_line = f_start_index.readlines()[-1]
            start_index = int(last_line.split('|||')[0].split('/')[0]) # [之前已到的序列号]从第492个课程开始参加

    with open(res_filename, 'a', encoding='utf-8') as fw:
        with open(filename, 'r', encoding='utf-8') as fr:
            json_list = json.load(fr)
        sum_count = len(json_list)
        json_list = json_list[start_index:]
        current_count = start_index
        for item in json_list:
            current_count += 1
            time.sleep(random.randint(1, 10))
            mocCourseBaseCardVo = item['mocCourseBaseCardVo']
            lession_id = mocCourseBaseCardVo['id']
            lession_name = mocCourseBaseCardVo['name']
            schoolName = mocCourseBaseCardVo['schoolName']
            schoolSN = mocCourseBaseCardVo['schoolSN']
            currentTermId = mocCourseBaseCardVo['currentTermId']
            closeVisableStatus = mocCourseBaseCardVo['closeVisableStatus']
            status = '已关闭选课' if closeVisableStatus == 1 else '开放选课'
            lession_url = f'{base_url}/{schoolSN}-{lession_id}'
            joined = check_term_learned(currentTermId)
            if joined:
                fw.write(
                    f'{current_count}/{sum_count}|||已参加课程【{schoolName}】《{lession_name}》|||{status}|||{lession_url}\n')
                print(
                    f'{current_count}/{sum_count}|||已参加课程【{schoolName}】《{lession_name}》|||{status}|||{lession_url}\n')
            else:
                fw.write(
                    f'{current_count}/{sum_count}|||未参加课程【{schoolName}】《{lession_name}》|||{status}|||{lession_url}\n')
                print(
                    f'{current_count}/{sum_count}|||未参加课程【{schoolName}】《{lession_name}》|||{status}|||{lession_url}\n')


if __name__ == '__main__':
    filename = '2001.json'
    check_joined(filename)
