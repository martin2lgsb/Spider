import csv
import json
import logging
import math
import pinyin
from time import sleep

import requests
from lxml import etree

from data_process import read_save_text

def get_json(url, num, pos):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest'
    }

    my_data = {
        'first': 'true',
        'pn': num,
        'kd': pos
    }

    res = requests.post(url, headers=my_headers, data=my_data)
    if res.status_code == requests.codes.ok:
        res.encoding = 'utf-8'
        page = res.json()
        return page
    else:
        return None


def get_description(positionId):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=',
    }

    url = 'https://www.lagou.com/jobs/' + str(positionId) + '.html'
    res = requests.get(url, headers=my_headers)
    res.raise_for_status()
    res.encoding = 'utf-8'
    html = etree.HTML(res.text)
    description = html.xpath('//*[@class="job_bt"]/div//text()')

    return description


def save_position(res_position, file_sufix):
    pos_id_arr = []
    for res in res_position:
        pos_id_arr.append(res['positionId'])
        with open('./data/position_' + file_sufix + '.data', 'a') as p:
            json.dump(res, p, ensure_ascii=False)
            p.write('\n')
    logging.info("---- 已记录一页相关描述 | 职位 ----")
    return pos_id_arr


def save_description(pos_id_arr, file_sufix):
    for position_id in pos_id_arr:
        debug_save_description(position_id, file_sufix)
        sleep(3)


def debug_save_description(position_id, file_sufix):
    details = get_description(position_id)

    try_count = 0
    while len(details) == 0:
        try_count += 1
        logging.info("---- 项目 {} 已重试次数 | {} c----".format(position_id, try_count))

        if try_count == 1:
            sleep(25)
        elif try_count < 15:
            sleep(10)
        elif try_count >= 15:
            logging.info("---- 项目 {} 记录尝试失败 ----")
            break
        sleep(5)
        details = get_description(position_id)

    details_str = ''.join(details).replace('\r', '').replace('\n', '').replace('\t', '').strip()
    description = [position_id, details_str]
    with open('./data/description_' + file_sufix + '.data', 'a') as d:
        writer = csv.writer(d, delimiter='\t')
        writer.writerow(description)
    logging.info("---- 已记录一条相关描述 | 详情 ----")


def get_information(pos, pos_pinyin):

    url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    position = get_json(url, 1, pos)
    while position is None:
        logging.info("---- 查询间歇，请稍等 ----")
        sleep(30)
        position = get_json(url, 1, pos)

    try:
        total_count = position['content']['positionResult']['totalCount']
    except Exception:
        print(position)
        total_count = 0

    logging.info("---- 查询返回共 {} 条结果 ----".format(total_count))
    if total_count == 0:
        logging.info("---- 未返回任何查询结果 ----")
        exit(0)
    total_pages_num = int(math.ceil(total_count / 15))

    for num in range(1, total_pages_num + 1):
        position = get_json(url, num, pos)
        while position is None:
            logging.info("---- 查询间歇，请稍等 ----")
            sleep(30)
            position = get_json(url, num, pos)

        try:
            res_position = position['content']['positionResult']['result']
        except Exception:
            logging.info("---- 第 {} 页项目数据无法正确获取 ----".format(num))
            continue
        else:
            pos_arr = save_position(res_position, pos_pinyin)
            save_description(pos_arr, pos_pinyin)
            sleep(45)

        # print(json.dumps(position['content']['positionResult']['result'][0], indent=4, ensure_ascii=False)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    pos_input = str(input("请输入你需要查找的职位名称（北京）: ")).strip()
    if pos_input == "":
        logging.info("---- 用户未输入任何信息 ----")
        exit(0)

    pos_input_pinyin = pinyin.get_initial(pos_input).replace(" ", "")

    # 获取数据
    get_information(pos_input, pos_input_pinyin)
    # 存储词频
    read_save_text(pos_input_pinyin)

