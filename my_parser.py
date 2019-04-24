'''
模块名: my_parser
定义的类：MyParser
简介：给MySpider类使用的解析器的基类
'''



import requests
from bs4 import BeautifulSoup
from lxml import etree
import pymysql

class MyParser(object):
    def login_data_parser(self,login_url):
        '''
        解析登录表单信息
        :param login_url: 登录页面的url
        :return (登录信息字典,获取时得到的cookies)
        '''
        #提示信息
        print('[@parser]:get login data')

        response=requests.get(login_url)
        html=response.text
        #解析表单域，派生类中可根据具体表单修改
        soup=BeautifulSoup(html,'lxml')
        #此处插入解析语句，下面为模板
        example_data=soup.find('input',{'name': 'example_data'})['value']
        login_data={
            'example_data':example_data
        }


        #提示信息
        print('[@parser]:get login data (has done)')

        return login_data,response.cookies
    
    def uni_parser(self,url,xpath,**kwargs): 
        '''
        通用xpath解析器
        :param url:需要解析的网页url
        :param xpath:xpath字符串

        :return: 结果列表
        '''
        response=requests.post(url,**kwargs)
        html=response.text
        tree=etree.HTML(html)
        result_list=tree.xpath(xpath)
        return result_list

    def get_urls(self,catalogue_url,**kwargs):

        '''
        获取目录页的url

        :param catalogue_url:目录页的url
        :param **kwargs:cookies和headers可以从这里传入
        '''
        #准备
        base_url='http://example.cn/'#用于和相对url拼接的url前半部分
        cata_base_url=catalogue_url.split('?')[0]#获取不带参数的目录页url
        para = {#目录页url的参数
            'pageIndex': 1
        }
        
        #获取目录的实际页数
        xpath='//*[@id="page_num"]/text()'#此处为示范
        page_num=int(self.uni_parser(cata_base_url,xpath,params=para,**kwargs))
        
        #获取所有目录页的url
        xpath='//a/@href'#链接标签的xpath
        url_list=[]
        
        for i in range(1,page_num+1):
            para['pageIndex'] = i
            #提示信息
            print("[@parser]:get urls({}%): {}/{}".format(round((i/page_num)*100,1),i,page_num))
            #获取单页目录的url列表
            urls=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
            for url in urls:
                url_list.append(base_url+str(url))
            

        return url_list


    def get_content(self,url,**kwargs):
        '''
        获取内容
        :param url:需要解析的网页的url

        :return: 用于传给存档器的 记录字典，键为字段名，值为值
        '''

        html=requests.post(url,**kwargs).text
        soup=BeautifulSoup(html,'lxml')
        content=soup.find('div',id='content')
        content=str(content)
        record_dict={
            'content':pymysql.escape_string(content)#转义处理
        }

        return record_dict