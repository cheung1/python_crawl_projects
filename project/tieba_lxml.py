#!usr/bin/env python
#-*- encoding:utf-8 -*-
__author__ = "Cheung"

import requests
from urllib import parse
from lxml import etree

class imageSpider():
    def __init__(self, begin_page, end_page, kw):
        self.begin_page = int(begin_page)
        self.end_page = int(end_page)
        self.key = parse.urlencode({"kw": kw})

    def loadPage(self, url):
        '''
            作用：下载网页 HTML 源码
            url:需要爬取的url地址
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
        }
        # 获取网页html源码
        response = requests.get(url)
        html = response.text
        # print(html)
        # 解析HTML文档 为HTML.DOM 模型
        content = etree.HTML(html)
        # print(content)
        # 返回所有成功匹配的列表集合
        link_list = content.xpath('//div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit "]/@href')
        for link in link_list:
            fulllink = "http://tieba.baidu.com" + link
            # print(fulllink)
            self.loadImage(fulllink)

    def loadImage(self, link):
        '''
            作用：下载页面图片
            link：图片连接
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
        }
        response = requests.get(link, headers=headers)
        html = response.text
        # 解析
        content = etree.HTML(html)
        # 取出帖子里每层层主发送的图片连接集合
        # print(content)
        link_list = content.xpath('//img[@class="BDE_Image"]/@src')
        # 取出每个图片的链接
        for link in link_list:
            self.writeImage(link)

    def writeImage(self, link):
        '''
            作用：写入图片至本地
            link：图片连接
        '''
        print("正在保存。。。")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
        }
        response = requests.get(link, headers=headers)
        # 图片原始数据
        image = response.content
        # 取出连接后10位做为文件名
        filename = link[-10:]
        # 写入到本地文件
        with open(filename, 'wb') as f:
            f.write(image)
        print("已经成功下载" + filename)

    def startSpider(self):
        '''
            作用：控制爬虫下载
        '''
        url = "http://tieba.baidu.com/f?"
        # 拼接 Url
        tempurl = url + self.key
        # print(tempurl)
        for page in range(self.begin_page, self.end_page + 1):
            pn = (page - 1)*50
            fullurl = tempurl + "&pn=" + str(pn)
            # print(fullurl)
            self.loadPage(fullurl)
        print("Thank you!")


if __name__ == "__main__":
    kw = input("which keyword you want to search: ")
    begin_page = input("the begin page: ")
    end_page = input("the end page: ")

    spider = imageSpider(begin_page, end_page, kw)
    spider.startSpider()









