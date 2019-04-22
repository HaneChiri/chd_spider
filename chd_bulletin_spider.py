from my_spider import MySpider
from my_parser import MyParser
from my_database import MyDatabase
from my_archiver import MyArchiver
from bs4 import BeautifulSoup
import requests
import pymysql

class chdParser(MyParser):
    
    def login_data_parser(self,login_url):
        '''
        This parser is for chd
        :param url: the url you want to login
        :return (a dict with login data,cookies)
        '''
        #report
        print('[@parser]:get login data')

        response=requests.get(login_url)
        html=response.text
        # parse the html
        soup=BeautifulSoup(html,'lxml')
        
        lt=soup.find('input',{'name':'lt'})['value']
        dllt=soup.find('input',{'name':'dllt'})['value']
        execution = soup.find('input', {'name': 'execution'})['value']
        _eventId = soup.find('input', {'name': '_eventId'})['value']
        rmShown = soup.find('input', {'name': 'rmShown'})['value']
        login_data={
            'username': input('input account:'),
            'password': input('input passwd:'),
            'btn':'',
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': _eventId,
            'rmShown': rmShown
        }


        #report
        print('[@parser]:get login data (has done)')

        return login_data,response.cookies

    
    def get_urls(self,catalogue_url,**kwargs):
        '''
        get all urls that needs to crawl.
        '''
        #prepare
        base_url='http://portal.chd.edu.cn/'
        index_url='http://portal.chd.edu.cn/index.portal?.pn=p167'
        cata_base_url=catalogue_url.split('?')[0]
        para = {
            'pageIndex': 1,
            'pageSize': '',
            '.pmn': 'view',
            '.ia': 'false',
            'action': 'bulletinsMoreView',
            'search': 'true',
            'groupid': 'all',
            '.pen': 'pe65'
        }
        requests.post(index_url,**kwargs)
        
        #get page number
        xpath='//*[@id="bulletin_content"]/div[2]/div/span/text()'
        num=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
        num=num[0].strip().split("/")
        total=int(num[0])
        page_num=int(num[1])
        
        #repeat get single catalogue's urls
        xpath='//*[@id="bulletin_content"]//ul[contains(@class,"rss-container")]//a[@class="rss-title"]/@href'
        url_list=[]
        
        
        for i in range(1,page_num+1):
            para['pageIndex'] = i
            #report
            print("[@parser]:get urls({}%): {}/{}".format(round((i/page_num)*100,1),i,page_num))
            #get single catalogue's urls
            urls=self.uni_parser(cata_base_url,xpath,params=para,**kwargs)
            for url in urls:
                url_list.append(base_url+str(url))

        return url_list
    
    
class chdArchiver(MyArchiver):
    pass

class chdSpider(MySpider):
    pass


if __name__ == '__main__':

    login_url="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
    home_page_url="http://portal.chd.edu.cn/"
    catalogue_url="http://portal.chd.edu.cn/detach.portal?.pmn=view&.ia=false&action=bulletinsMoreView&search=true&.f=f40571&.pen=pe65&groupid=all"

    connect_config={
        'host':'127.0.0.1',
        'user':'root',
        'passwd':'password',
        'port':3306,
        'charset':'utf8',
    }
    

    parser=chdParser()
    archiver=chdArchiver('dbase','bulletin',**connect_config)
    
    sp=chdSpider(parser,archiver,**connect_config)
    sp.crawl(login_url,home_page_url,catalogue_url)
    