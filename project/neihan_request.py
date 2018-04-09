#!usr/bin/env python
#-*- encoding:utf-8 -*-
__author__ = "Cheung"

import requests
import re


class Spider():
    def __init__(self):
        # 初始化起始页位置
        self.page = 1
        # 爬取开头，若为 True , 则继续爬
        self.switch = True

    def loadPage(self, code='gbk'):
        '''
            作用：下载页面
        '''
        print("正在下载数据。。。")
        url = "http://www.neihan8.com/article/list_5_" + str(self.page) + ".html"
        headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        response = requests.get(url, headers)
        response.encoding = code
        # 获取网页的 HTML 源码
        html = response.text
        # print(html)
        # 创建正则表达式对象，匹配每页中标题部分，re.S 表示匹配全部字符串内容 re.I 表示忽略大小写、
        title_pattern = re.compile(r'<a href="/article/\d+.html">(.*?)</a>.*?</h4>', re.S)
        # 将正则匹配对象应用到html源码字符串里，返回这个页面里的所有标题的列表
        title_list = title_pattern.findall(html)
        # print(title_list)
        # 创建正则表达式对象，匹配每页中段子部分
        content_pattern = re.compile(r'<div\sclass="f18 mb20">(.*?)</div>', re.S)
        # 将正则匹配对象应用到html源码字符串里，返回这个页面里的所有段子的列表
        content_list = content_pattern.findall(html)
        # print(content_list)
        # 调用dealPage() 处理段子里的杂七杂八
        self.dealPage(title_list, content_list)

    def dealPage(self, title_list, content_list):
        '''
            作用：处理下载下来的段子
        '''
        for i in range(len(title_list)):
            title = title_list[i].replace("</b>", "").replace("<b>", "")
            content = content_list[i].replace("<br />", "").replace("<p>", "").replace("</p>", "").replace("\n", "")
            item = title + "\n" + content
        # print(title)
        # print(content)
        # 处理完后调用savePage() 将每个段子写入文件内
            self.savePage(item)

    def savePage(self, item):
        '''
            作用：把每条段子写入文件
        '''
        print("正在保存数据。。。")
        with open("duanzi_request.txt", "a", encoding='utf-8') as f:
            f.write(item + "\n")


    def startWork(self):
        '''
            控制爬虫运行，调度器
        '''
        # 循环执行，直到 self.switch == False
        while self.switch:
            self.loadPage()
            command = input("如果继续爬取，请按回车（退出输入quit)")
            # 如果停止爬取，则输入 quit
            if command == "quit":
                self.switch = False
            # 每次循环，page页码自增1
            self.page += 1
        print("谢谢使用！")

if __name__ == "__main__":
    duanziSpider = Spider()
    # duanziSpider.loadPage()
    duanziSpider.startWork()




