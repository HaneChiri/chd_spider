import requests
from bs4 import BeautifulSoup
from lxml import etree

class MyParser(object):
    def login_data_parser(self,login_url):
        '''
        This parser is for chd
        :param url: the url you want to login
        :return (a dict with login data,cookies)
        '''
        response=requests.get(login_url)
        html=response.text
        # parse the html
        soup=BeautifulSoup(html,'lxml')
        #insert parser,following is a example
        example_data=soup.find('input',{'name': 'example_data'})['value']
        login_data={
            'example_data':example_data
        }
        return login_data,response.cookies
    
    def uni_parser(self,url,xpath,**kwargs): 
        response=requests.post(url,**kwargs)
        html=response.text
        tree=etree.HTML(html)
        result_list=tree.xpath(xpath)
        return result_list

    def get_urls(self,catalogue_url,**kwargs):
        '''
        get all urls that needs to crawl.
        '''
        #prepare
        base_url='http://example.cn/'
        cata_base_url='http://example.cn/detach.portal'
        para = {
            'pageIndex': 1
        }
        
        #get the number of pages
        xpath='//*[@id="page_num"]/text()'
        page_num=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
        
        #repeat get single catalogue's urls
        xpath='//a/@href'#link tag's xpath
        url_list=[]
        
        for i in range(1,page_num+1):
            #get single catalogue's urls
            rss_title=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
            for i in rss_title:
                url_list.append(base_url+str(i))
            para['pageIndex'] = i

        #echo
        for i in url_list:
            print(i)
        print(len(url_list))

        return url_list