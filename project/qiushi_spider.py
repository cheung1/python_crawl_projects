# !/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'Cheung'

import json
import requests
from lxml import etree

class Qiushi():

    def __init__(self, url):
        '''
            function: accept the crawl url
            url: the website url
        '''
        self.url = url

    def load_html(self):
        '''
            function: download the HTML code on the url
        '''
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"
        }
        response = requests.get(self.url, headers=headers)
        html = response.text
        # print(html)
        # evoke parse_json function, set html as a variable
        self.parse_json(html)

    def parse_json(self, html):
        '''
            function: make the HTML type to HTML DOM type by HTML()method, and use xpath() method to
                    parse the code, save all the information to a dict, use json.dumps() method, convert
                    the dict to a json type data
            html: the HTML data prepared to parse
        '''
        # use HTML() method let json file convert to HTML.DOM type file
        text = etree.HTML(html)
        # use xpath to find all lists' tag
        node_list = text.xpath('//div[contains(@id,"qiushi_tag")]')
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
                "username" : author,
                "content" : content,
                "thumb" : thumb,
                "comment" : comment,
                "image" : ["https:" + i for i in image]
}
            # print(items)
            # use json.dumps() method, convert items to a json type
            array = json.dumps(items, ensure_ascii=False)
            # print(array)
            # evoke write_file() function
            self.write_file(array)
            # print(array)

    def write_file(self, data):
        '''
            function: write data into file, and save it in the local space
            data: the json type data
        '''
        with open("qiushi.json", "a") as f:
            f.write(data.encode('utf-8').decode() + '\n')

    def start_crawl(self):
        '''
            function: control the spider
        '''
        self.load_html()




if __name__ == "__main__":
    url = "https://www.qiushibaike.com/8hr/page/2/"
    qiushi = Qiushi(url)
    qiushi.start_crawl()
    # qiushi.load_html()


