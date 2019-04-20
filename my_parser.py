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
        #insert parser,following is an example
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
        cata_base_url=catalogue_url.split('?')[0]
        para = {
            'pageIndex': 1
        }
        
        #get the number of pages
        xpath='//*[@id="page_num"]/text()'
        page_num=int(self.uni_parser(cata_base_url,xpath,params=para,**kwargs))
        
        #repeat get single catalogue's urls
        xpath='//a/@href'#link tag's xpath
        url_list=[]
        
        for i in range(1,page_num+1):
            para['pageIndex'] = i
            #get single catalogue's urls
            urls=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
            for url in urls:
                url_list.append(base_url+str(url))
            

        return url_list


    def get_content(self,url,**kwargs):
        '''
        get content from the parameter "url"
        '''
        html=requests.post(url,**kwargs).text
        soup=BeautifulSoup(html,'lxml')
        content=soup.find('div',id='content')
        content=str(content)
        return content