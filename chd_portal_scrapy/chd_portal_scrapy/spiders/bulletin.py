# -*- coding: utf-8 -*-
#from scrapy.shell import inspect_response
#inspect_response(response, self) # 用于调试
import scrapy
from scrapy.conf import settings
from chd_portal_scrapy.items import BulletinsItem
from urllib.parse import urlencode
import requests

# 调整路径以找到自定义模块
import os,sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))# 获取绝对路径
sys.path.append(BASE_DIR+'\\..\\..\\..')

# print(sys.path)
from my_module.portal_login.login import *

class BulletinSpider(scrapy.Spider):
    name = 'bulletin'
    allowed_domains = ['portal.chd.edu.cn']
    # 公告界面的url
    start_urls = ['http://portal.chd.edu.cn/detach.portal?.pmn=view&.ia=false&action=bulletinsMoreView&search=true&.f=f40571&.pen=pe65&groupid=all']

    def start_requests(self):
        # 获取设置
        self.my_headers={
            'User-Agent':settings.get('USER_AGENT')
        }
        login_url=settings.get('LOGIN_URL')
        home_url=settings.get('HOME_URL')
        # 登录
        self.cookies=login(login_url,self.my_headers,home_url)
        
        self.page_index = 1 # 初始化页数
        for url in self.start_urls:
            self.cookies=dict(self.cookies)
            yield scrapy.Request(url,callback=self.parse_catalogue,cookies=self.cookies)

    def parse_catalogue(self,response):
        '''
        解析公告目录页
        '''
        # print(response.text)
        # 解析本页
        news_list=response.css('.rss-title')
        for news in news_list:
            item=BulletinsItem()
            url=news.css('a::attr(href)').extract_first()
            title=news.css('a span::text').extract_first().strip()
            item['url']=response.urljoin(url)
            item['title']=title
            yield item
        
        # 翻页
        if not hasattr(self,'page_sum'):
            self.page_sum=int(response.selector.re('共\d*?条记录 分(\d*?)页显示')[0])
        if self.page_index <= self.page_sum:

            # http://portal.chd.edu.cn/detach.portal?pageIndex=1&pageSize=&.pmn=view&.ia=false&action=bulletinsMoreView&search=true&groupid=all&.pen=pe65
            data={
                'pageIndex': self.page_index,
                'pageSize': '',
                '.pmn': 'view',
                '.ia': 'false',
                'action': 'bulletinsMoreView',
                'search': 'true',
                'groupid': 'all',
                '.pen': 'pe65'
            }
            self.page_index+=1
            next_url='http://portal.chd.edu.cn/detach.portal?'+urlencode(data)


            yield scrapy.Request(url=next_url,callback=self.parse_catalogue)

        

    def parse(self, response):
        pass


    