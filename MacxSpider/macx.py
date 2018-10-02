import requests as re
from lxml import etree
import numpy as np
import csv
import datetime

def crapyPrice():
    url_jiage = "https://www.macx.cn/html/jiage.html?22210c"
    html = re.get(url_jiage).content.decode('gbk')
    dom_tree = etree.HTML(html)
    phones1 = dom_tree.xpath("//div[@class='pz1111']/div[@class='pz-2211']//div[@class='jiage-11111']/text()")
    phones2 = dom_tree.xpath("//div[@class='pz11111']/div[@class='pz-22111']//div[@class='jiage-111111']/text()")
    phones_union = phones1 + phones2
    # print(prices1)
    # print(phones2)
    price_array = np.array(phones_union).reshape(int(len(phones_union) / 3), 3)
    price_min = [str(x[0]).strip() for x in iter(price_array)]
    # print('iPhone XS Max: ' + min(price_min[3:]))
    # print('MACX PRICES: ' + str(price_min))
    price_min.append(datetime.datetime.now().strftime("%Y-%m-%d"))
    price_min.append(min(price_min[3:(len(price_min) - 1)]))
    print(price_min)
    with open("iphone_macx_price.csv", 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(price_min)

if __name__ == '__main__':
    crapyPrice()

