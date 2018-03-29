# encoding: utf-8
#!/usr/bin/env python
'''
Created on 2018年2月6日

@author: WangCong
'''

import url_manage, web_download, web_parsing
import requests  # http://blog.csdn.net/gyq1998/article/details/78583841
# from lxml import etree  # https://www.cnblogs.com/BigFishFly/p/6380016.html
import re
import numpy as np
import sqlite3

url_root = 'http://www.qichacha.com'
url = url_root + '/search?key={keyword}#p:{num}&'
headers = {
    'Connection' : 'keep-alive',
    'Cookie' : 'zg_did=%7B%22did%22%3A%20%22161656e666717f-05e041ab0f746e8-4c322172-1fa400-161656e666878f%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201518079785363%2C%22updated%22%3A%201518079847203%2C%22info%22%3A%201517825189486%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22localhost%3A8888%22%2C%22cuid%22%3A%20%226c19524a673ac045babafcedac2b6453%22%7D; _uab_collina=151782519867722924826534; UM_distinctid=161656ffdee4ff-052af228aec4738-4c322172-1fa400-161656ffdef769; CNZZDATA1254842228=1930218608-1517821373-%7C1517821373; _umdata=486B7B12C6AA95F25F430F3BD1C599F0B8963DA670190565365CACB94D015DE2A931945AA222E77FCD43AD3E795C914C016A68544FB1EDAB47A8332C57BAF16F; acw_tc=AQAAABabtxmL5A4AMxIdPHGnakvlsg6k; PHPSESSID=t3k1p8vb6btch0apml7or9phq7; hasShow=1',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
}
keywords = ['小米', '啊', 'a']  # 公司关键词。
num = np.arange(1, 2)  # 页码，普通注册用户 10 页， VIP 500 页。 

def get_url(url, keywords, num):
    '''
    拼接 URL
    '''
    url_temp = url
    for i in keywords:
        for j in num:
            url = url_temp.format(keyword=i, num=j)
            yield url, i

for url, keyword in get_url(url, keywords, num):
    r = requests.get(url, headers=headers, timeout=10)
    
    if '您的搜索词太宽泛，建议更换一下搜索词' in r.text:
        print('这个词不好：', keyword)
        continue
    elif "// window.zhuge.track('首页');" in r.text:
        print('返回首页了：', keyword)
    else:
        html = re.findall('<tbody>[\s\S]*</tbody>', r.text)
        
        # 公司 URL
        url_frim = re.findall('/firm_[\s\S]*?.html', html[0])
        url_frim = map(lambda x: url_root + x, url_frim)
        
        # 法定代表人 URL，不需要这个，公司页面里有管理者 URL，两个 URL 不同，但内容相同，这点对 SEO 很不好，为什么这么大的网站没注意？ 
    #     url_people = re.findall('/people?[\s\S]*?"', html[0])
    #     url_people = map(lambda x: (url_root + x[0:-1]), url_people)
    
        for i in url_frim:
            r = requests.get(i, headers=headers, timeout=10)
            frim_name = re.findall('<div class="row title" style="margin-top: -2px;margin-bottom: 14px;">([\s\S]*?)\n', r.text)
            print(frim_name, i)  # 公司详情页属性太多了，只简单获取了 公司名和 URL，有时间再慢慢加。
        
     
# 数据库
conn = sqlite3.connect('./qichacha.sqlite')  # 建立 SQL
cur = conn.cursor()  # 游标
conn.text_factory = str                 #中文处理









