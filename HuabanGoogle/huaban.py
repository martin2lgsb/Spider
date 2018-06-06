# m2lgsb HuabanGoogle
# !/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import sys, os, re, requests, urllib, json


class HuabanSpider():

    def __init__(self):
        self.imgs = []
        self.homeUrl = self.method()

        input_num = input("How many pics do u need: ") # TODO: 画板功能下，0 -> 下载所有
        while not input_num.isdigit():
            input_num = input('Please input Number: ')

        if int(input_num) < 0:
            print('U Need Nothing, Bye!')
            sys.exit(0)
        self.img_num = int(input_num)

        if not os.path.exists('./images'):
            os.mkdir('./images')

    def method(self):
        method = input("What kind of method do u want to use for Download? Theme(T)/Board(B)/Google(G): ").lower()
        if method == "t":
            return "http://huaban.com/favorite/"  + input("Theme: ") # 指定主题下载
        elif method == "b":
            return "http://huaban.com/boards/" + input("Board-ID: ") # TODO: 指定画板ID下载， bug: list index out of range
        elif method == "g":
            return "https://huaban.com/search/?q=" + input("HuabanGoogle: ") # 搜索功能，需要登录
        else:
            self.method()

    def homePage(self):
        return requests.get(url = self.homeUrl).content

    # 获取图片信息
    def getPinsDic(self, html):
        html = html.decode('utf-8') #python3
        preg = re.compile('app\.page\["pins"\].*')
        appPins = preg.findall(html)
        if appPins == []:
            return None

        result = json.loads(appPins[0][19:-1])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
            info['type'] = i["file"]["type"][6:]
            self.imgs.append(info)

    # 刷新图片
    def make_ajax_url(self, No):
        return self.homeUrl + "?i5p998kw&max=" + No + "&limit=20&wfl=1"

    def refresh(self, maxID):
        return requests.get(url = self.make_ajax_url(maxID)).content

    def getImgUrl(self):
        self.getPinsDic(self.homePage())
        for i in range(int((self.img_num / 20) - 1)):
            self.getPinsDic(self.refresh(self.imgs[-1]["id"]))

    # 下载图片
    def downImages(self):
        print("{} images will be download".format(len(self.imgs))) # TODO: 需要调整
        for key, image in enumerate(self.imgs):
            print('Downloading {} ...'.format(key + 1)) # TODO: 添加下载进度条
            try:
                req = requests.get(image["url"])
            except:
                print('Error!')
            imageName = os.path.join("./images", image["id"] + "." + image["type"])
            self.saveImages(imageName, req.content)

    def saveImages(self, imageName, content):
        with open(imageName, 'wb') as img:
            img.write(content)


if __name__ == '__main__':
    Huaban = HuabanSpider()
    Huaban.getImgUrl()
    Huaban.downImages()
    print('Done!')
