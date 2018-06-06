# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf8')


class DoubanSpiderPipeline(object):
    # def __init__(self):
        # self.file = codecs.open('douban_movie_top250.json', mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        db = pymysql.connect('localhost', 'root', '', 'scrapy', charset="utf8")
        cursor = db.cursor()
        sql_create = """create table if not exists douban_movie_top250 (
                        id int(5) NOT NULL auto_increment primary Key,
                        movie_name varchar(255),
                        star decimal(2, 1),
                        quote varchar(255)
                        )"""
        cursor.execute(sql_create)

        # line = ''
        for i in range(len(item['movie_name'])):
            sql_insert = """insert into douban_movie_top250 (movie_name, star, quote)
                            values (%s, %s, %s)"""

            try:
                cursor.execute(sql_insert, (
                    item['movie_name'][i],
                    item['star'][i],
                    item['quote'][i]
                ))
                db.commit()
            except pymysql.Error, e:
                print e

        #     movie_name = {"movie_name":item['movie_name'][i]}
        #     star = {"start":item['star'][i]}
        #     quote = {"quote":item['quote'][i]}
        #     line = line + json.dumps(movie_name, ensure_ascii=False)
        #     line = line + json.dumps(star, ensure_ascii=False)
        #     line = line + json.dumps(quote, ensure_ascii=False)+"\n"
        # self.file.write(line)

    def close_spider(self,spider):
        self.file.close()
