import json

import jieba
import wordcloud
import csv
import string
import re
import nltk


def to_cloud():
    pass


def read_save_text(file_name):
    stopwords = [l.strip() for l in open("./stopwords_zh.txt")]
    with open("./data/description_{}.data".format(file_name), "r") as d:
        lines = d.readlines()

        temp_dict = {}
        for line in lines:
            word_list = jieba.lcut(line.split("\t")[1])
            zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
            word_zh = filter(lambda x: zh_pattern.match(x), word_list)

        # print(string.punctuation)
        # print(dict(nltk.FreqDist(word_zh)))

            for word in word_zh:
                if word in temp_dict.keys():
                    temp_dict[word] += 1
                else:
                    temp_dict[word] = 1

        stop = set(stopwords) & set(temp_dict.keys())
        for s in stop:
            temp_dict.pop(s)

        word_sorted = sorted(temp_dict.items(), key=lambda i: i[1], reverse=True)
        with open("./data/word_sorted_{}.data".format(file_name), "a") as w:
            writer = csv.writer(w, delimiter='\t')
            for item in word_sorted:
                writer.writerow(list(item))


def test_data(file_name):
    id_arr = []
    with open("./data/position_" + file_name + ".data", "r") as p:
        lines = p.readlines()
        for line in lines:
            d = json.loads(line)
            id_arr.append(d['positionId'])
    print(len(id_arr))
    print(len(set(id_arr)))


if __name__ == '__main__':
    # read_save_text('sjwj')
    test_data('sjwj')