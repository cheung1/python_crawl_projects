#!usr/bin/env python
#-*- encoding:utf-8 -*-
__author__ = "Cheung"

import threading
from queue import Queue
from lxml import etree
import requests
import json
import time


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue, dataQueue):
        '''
            初始化方法
        '''
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        #线程名
        self.threadName = threadName
        # 页码队列
        self.pageQueue = pageQueue
        # 数据队列
        self.dataQueue = dataQueue
        # 请求报头
        self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        '''
            功能：启动采集线程
        '''
        print("启动 " + self.threadName)
        while not CRAWL_EXIT:
            try:
                # 可选参数block，默认值为True
                #1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
                #2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
                page = self.pageQueue.get(False)
                url = "http://www.qiushibaike.com/8hr/page/" + str(page) +"/"
                content = requests.get(url, headers=self.headers).text
                time.sleep(1)
                self.dataQueue.put(content)
            except:
                continue
        print("end " + self.threadName)


class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, filename, lock):
        '''
            初始化方法
        '''
        super(ThreadParse, self).__init__()
        # 线程名
        self.threadName = threadName
        # 数据队列
        self.dataQueue = dataQueue
        # 保存解析后数据的文件名
        self.filename = filename
        # 锁
        self.lock = lock

    def run(self):
        '''
            功能：启动解析线程
        '''
        print("start" + self.threadName)
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                # print(html)
                self.parse(html)
            except:
                continue
        print("end " + self.threadName)

    def parse(self, html):
        '''
            功能：解析HTML网页
            html: 需要解析的html页面
        '''
        html = etree.HTML(html)
        # use xpath to find all lists tag
        node_list = html.xpath('//div[contains(@id,"qiushi_tag")]')
        # define a dict to save the data, json.dumps{} accept a dict like type data
        items = {}
        for node in node_list:
            # use xpath to analyse author
            author = node.xpath('.//h2')[0].text
            # print(author)
            # use xpath to analyse content
            content = node.xpath('.//div[@class="content"]/span')[0].text
            # use xpath to analyse thumbs
            thumb = node.xpath('.//span[@class="stats-vote"]/i')[0].text
            # use xpath to analyse comments
            comment = node.xpath('.//span[@class="stats-comments"]//i')[0].text
            # use xpath to analyse image
            image = node.xpath('./div[@class="thumb"]//@src')
            items = {
                "username": author,
                "content": content,
                "thumb": thumb,
                "comment": comment,
                "image": ["https:" + i for i in image]
            }
            # print(items)
            # with 后面有两个必须执行的操作：__enter__ 和 _exit__
            # 不管里面的操作结果如何，都会执行打开、关闭
            # 打开锁、处理内容、释放锁
            with self.lock:
                # write the saved analyses data
                self.filename.write(json.dumps(items, ensure_ascii=False).encode('utf-8').decode() + "\n")


CRAWL_EXIT = False
PARSE_EXIT = False

def main():
    # 页码的队列，暂定为20
    pageQueue = Queue(20)
    for i in range(20):
        pageQueue.put(i)

    #存放采集结果的数据队列，参数为空表示不限制
    dataQueue = Queue()

    filename = open("duanzi.json", "a")
    # 创建锁
    lock = threading.Lock()

    # 三个采集线程的信息
    crawlList = ["采集线程1", "采集线程2", "采集线程3"]
    # 存储采集线程的列表集合
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        # 开启线程
        thread.start()
        threadcrawl.append(thread)

    # 三个解析线程的信息
    parseList = ["解析线程1", "解析线程2", "解析线程3"]
    # 存储解析线程的列表集合
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, filename, lock)
        thread.start()
        threadparse.append(thread)

    # 等待 pageQueue 队列为空，即等待之前操作执行完毕
    while not pageQueue.empty():
        continue

    # 如果 pageQueue 为空，退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print("pageQueue is empty")

    for thread in threadcrawl:
        thread.join()
        print("1")

    while not dataQueue.empty():
        continue

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadparse:
        thread.join()
        print("2")

    with lock:
        # close file
        filename.close()
    print("thank you")


if __name__ == '__main__':
    main()






