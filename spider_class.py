import requests
from bs4 import BeautifulSoup

class spider(object):
    def __init__(self):
        self.cookies=None
        self.headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }
        
    

    def login(self,login_url,login_data_parser=None,target_url=None):
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

        #login
        response=requests.post(login_url,headers=self.headers,data=login_data,cookies=cookies)

        if(target_url!=None and response.url==target_url):
            print("login successfully")

        self.cookies=cookies
        return response
        
    def get_urls(self,url):
        pass
            

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

    
    def parse(self):
        pass

    def save(self):
        pass



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



#http://api.xzxyun.com/



if __name__ == "__main__":
    login_url="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
    target_url="http://portal.chd.edu.cn/"

    login_url_ucard='http://api.xzxyun.com/Account/Login/'

    img_url='https://HaneChiri.github.io/blog_images/article/simple_inverted_index.png'
    sp=spider()
    #sp.login(login_url,chd_login_data_parser,target_url)
    sp.login(login_url_ucard,sp.ucard_login_data_parser)
    #sp.get_img(img_url)




