# !/usr/bin/env python
# -*- encoding: utf-8 -*-
__author__ = 'Cheung'

import requests
from bs4 import BeautifulSoup
import re

def getHTMLText(url, code = 'utf-8', timeout=30):
    '''
    作用：通过requests库获取html文本
    url: 请求链接
    code: 编码格式，默认 utf-8
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1'
    }
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = code
        return r.text
    except Exception as e:
        print(e)

def getStockList(lst, stockURL):
    '''
    作用：从 stockURL 中获取所有股票代码，并存入列表中
    lst: 用来存放股票代码
    stockURL: 获取股票代码的链接
    '''
    html = getHTMLText(stockURL, 'GB2312')
    soup = BeautifulSoup(html, 'html.parser')
    # 从链接中找出所有的 'a' 标签
    quotebody = soup.find('div', attrs={'class': 'quotebody'})
    a = quotebody.find_all('a')
    for i in a:
        try:
            href = i.attrs['href']  # 取出所有属性值为 'href' 的
            lst.append(re.findall(r'[s][hz]\d{6}', href)[0])
        except Exception as e:
            print(e)

def getStockInfo(lst, stockURL, fpath):
    '''
    作用：从列表中读取股票代码，与stockURL拼接，请求拼接后的 url，将信息保存到文件路径fpath中
    lst: 存有股票代码的列表
    stockURL: 待拼接的 url
    fpath: 待写入的文件路径
    '''
    count = 0
    # 从列表中读取股票代码，与 stockurl 拼接
    for stock in lst:
        url = stockURL + stock + ".html"
        html = getHTMLText(url)
        try:
            if html == "":
                continue
            infoDict = {}
            soup = BeautifulSoup(html, 'html.parser')
            stockInfo = soup.find('div', attrs={'class': 'stock-bets'})

            name = stockInfo.find_all(attrs={'class': 'bets-name'})[0]
            infoDict.update({'股票名称': name.text.split()[0]})
            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            for i in range(len(keyList)):
                key = keyList[i].text
                val = valueList[i].text
                infoDict[key] = val
            # 写入文件
            with open(fpath, 'a', encoding='utf-8') as f:
                f.write(str(infoDict) + '\n')
                count += 1
                print('\r当前速度：{:.2f}%'.format(count/len(lst)*100), end="")
        except:
            count += 1
            print('\r当前速度：{:.2f}%'.format(count/len(lst)*100), end="")


if __name__ == '__main__':
    stock_list_url = 'http://quote.eastmoney.com/stocklist.html'
    stock_info_url = 'https://gupiao.baidu.com/stock/'
    output_file = 'BaiduStockInfo.txt'
    slist = []
    getStockList(slist, stock_list_url)
    getStockInfo(slist, stock_info_url, output_file)



