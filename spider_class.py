import requests
from bs4 import BeautifulSoup

class spider(object):
    def __init__(self):
        self.cookies=None
        
    

    def login(self,url,login_data_parser=None,target_url=None):
        '''
        login
        :param url: the url you want to login
        :param login_data_parser: a callback function to get the login_data you need when you login,return (login_data,response.cookies)
        :param target_url: Used to determine if you have logged in successfully

        :return: response of login
        '''
        
        headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
        }

        login_data=None

        #get the login data
        if(login_data_parser!=None and callable(login_data_parser)):
            login_data,cookies=login_data_parser(url)

        #login
        response=requests.post(url,headers=headers,data=login_data,cookies=cookies)

        if(target_url!=None and response.url==target_url):
            print("login successfully")

        self.cookies=cookies
        return response
        

            

        
    
    def parse(self):
        pass

    def save(self):
        pass



def chd_login_data_parser(url):
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




if __name__ == "__main__":
    login_url="http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F"
    target_url="http://portal.chd.edu.cn/"
    sp=spider()
    sp.login(login_url,chd_login_data_parser,target_url)




