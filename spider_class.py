import requests
from bs4 import BeautifulSoup
from lxml import etree


class parser():
    def chd_login_data_parser(self,url):
        '''
        This parser is for chd
        :param url: the url you want to login
        :return (a dict with login data,cookies)
        '''
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
        return login_data,response.cookies

    def ucard_login_data_parser(self,url):
        pass
        '''
        response=requests.get(url)
        html=response.text
        # parse the html
        soup=BeautifulSoup(html,'lxml')
        print(soup.prettify())
        next_url = soup.find('input', {'name': 'NextUrl'})['value']
        check_code=''
        img_url= soup.find('img', {'id': 'imgCheckCode'})['src']
        img_url='http://api.xzxyun.com/Account/'+img_url
        img=self.get_img(img_url,'check_code')

        print(img)
        #'http://api.xzxyun.com/Account/Login/Account/GetCheckCodeImg?rad=9'
        #http://api.xzxyun.com/Account/GetCheckCodeImg?rad=52

        openid=''
        login_data={
            'SchoolCode':'xahu',#input('input your school name'),
            'SignType':'SynSno',#input('input your SignType,"SynSno" or "SynCard"')
            'UserAccount':input('input your User Account'),
            'Password':input('input your Password'),
            'NextUrl':next_url,
            'CheckCode':check_code,
            'openid':openid,
        }
        
        return login_data,response.cookies
        '''
    

    def uni_parser(self,url,xpath,**kwargs):
    
        response=requests.post(url,**kwargs)
        html=response.text
        tree=etree.HTML(html)
        result_list=tree.xpath(xpath)

        return result_list
    
    def chd_get_urls(self,**kwargs):
        '''
        get all urls that needs to crawl.
        '''
        #prepare
        base_url='http://portal.chd.edu.cn/'
        index_url='http://portal.chd.edu.cn/index.portal?.pn=p167'
        bulletin_url='http://portal.chd.edu.cn/detach.portal'
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
        num=self.uni_parser(bulletin_url,xpath,params=para,**kwargs)
        num=num[0].strip().split("/")
        total=num[0]
        page_num=num[1]
        
        #repeat get single catalogue's urls
        xpath='//*[@id="bulletin_content"]//ul[contains(@class,"rss-container")]//a[@class="rss-title"]/@href'
        url_list=[]
        
        for i in range(1,1+1):
            #get single catalogue's urls
            rss_title=self.uni_parser(bulletin_url,xpath,params=para,**kwargs)
            for i in rss_title:
                url_list.append(base_url+str(i))
            para['pageIndex'] = i

        #echo
        for i in url_list:
            print(i)
        print(len(url_list))

        return url_list

    def chd_get_content(self,url,**kwargs):
        '''
        get content from the parameter "url"
        '''
        html=requests.post(url,**kwargs).text
        soup=BeautifulSoup(html,'lxml')
        content=soup.find('div',id='content')
        content=str(content)
        return content
        
        



class spider(object):
    def __init__(self):
        self.cookies=None
        self.headers={

            
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        
        self.parser=parser()#spider's parser
        
    

    def login(self,login_url,target_url,login_data_parser=None):
        '''
        login
        :param login_url: the url you want to login
        :param login_data_parser: a callback function to get the login_data you need when you login,return (login_data,response.cookies)
        :param target_url: Used to determine if you have logged in successfully

        :return: response of login
        '''
        
        

        login_data=None

        #get the login data
        if(login_data_parser!=None and callable(login_data_parser)):
            login_data,cookies=login_data_parser(login_url)

        #login without redirecting
        response=requests.post(login_url,headers=self.headers,data=login_data,cookies=cookies,allow_redirects=False)


        cookies_num=1
        while(target_url!=None and response.url!=target_url):#if spider is not reach the target page
            print('[spider]: I am at the "{}" now'.format(response.url))
            print('[spider]: I have got a cookie!Its content is that \n"{}"'.format(response.cookies))
            #merge the two cookies
            cookies=dict(cookies,**response.cookies)
            cookies=requests.utils.cookiejar_from_dict(cookies)
            cookies_num+=1
            print('[spider]: Now I have {} cookies!'.format(cookies_num))
            next_station=response.headers['Location']
            print('[spider]: Then I will go to the page whose url is "{}"'.format(next_station))
            response=requests.post(next_station,headers=self.headers,cookies=cookies,allow_redirects=False)

        cookies=dict(cookies,**response.cookies)
        cookies=requests.utils.cookiejar_from_dict(cookies)
        cookies_num+=1

        


        if(target_url!=None and response.url==target_url):
            print("login successfully")

        self.cookies=cookies
        return response
     

    def get_img(self,url,output_name=None,cookies=None):
        '''
        get a img
        :param url:the url of the img
        :param output_name:the output fileName,if it is None,the img will not be save
        :param cookies:cookies
        '''

        if(cookies==None):
            cookies=self.cookies
        response=requests.get(url,cookies=cookies)
        img=response.content

        if(output_name!=None):
            with open(output_name, 'wb') as f:
                f.write(img)

        return img


    def save(self,content):
        pass

    def crawl(self,)



    



#http://api.xzxyun.com/



if __name__ == "__main__":
    login_url="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
    target_url="http://portal.chd.edu.cn/"

    

    
    login_url_ucard='http://api.xzxyun.com/Account/Login/'

    img_url='https://HaneChiri.github.io/blog_images/article/simple_inverted_index.png'
    sp=spider()
    sp.login(login_url,target_url,sp.parser.chd_login_data_parser)
    sp.parser.chd_get_urls(cookies=sp.cookies,headers=sp.headers)








