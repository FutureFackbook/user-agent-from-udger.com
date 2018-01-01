# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
import urllib
import random
import lxml

def save_file(string):
    with open('c:\\ua.txt', 'a', encoding='utf-8') as f:
        for v in string:
            c = '\'' + v + '\'' + '\r\n'
            f.write(c)

class UaPipeline(object):
    def __init__(self):
        self.b_u_map = {}
        self.ua_url = []
        self.ua_list = []
        self.init_header = ''
        self.ua_xpath = '//td/p/a[contains(@href, "/resources/online-parser?")]/text()'

    def process_item(self, item, spider):
        for i in range(0, 251): # len(item['browser'])):
            prefix = 'https://udger.com' + re.sub('\s', '%20', item['useragent_link'][i])
            x = {item['browser'][i]: prefix}
            self.b_u_map.update(x)
            self.ua_url.append(prefix)

        for u in self.ua_url:
            opener = urllib.request.build_opener()
            if self.ua_list == []:
                opener.add_handler = [('User-Agent', self.init_header)]
            else:
                opener.add_handler = [('User-Agent', self.ua_list[random.randrange(0, len(self.ua_list))])]
            urllib.request.install_opener(opener)
            data = urllib.request.urlopen(u).read().decode('utf-8')

            selector = lxml.etree.HTML(data)
            ua_string = selector.xpath(self.ua_xpath)

            print(ua_string)
            save_file(ua_string)

            for v in ua_string:
                self.ua_list.append(v)

            time.sleep(3)
        
        print(self.ua_list)

        new_ret = list(set(self.ua_list))
        new_ret.sort(key = self.ua_list.index)
        self.ua_list = new_ret
        print('\r\n\r\nfinal ist:\r\n', self.ua_list)
        with open('C:\\programlearn\\scrapy\\ua\\ua.txt', 'w', encoding='utf-8') as f:
            for v in self.ua_list:
                c = '\'' + v + '\'' + '\r\n'
                f.write(c)
        return item
