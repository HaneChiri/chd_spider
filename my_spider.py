import requests

class MySpider(object):
    def __init__(self,parser,save,**save_params):
        self.parser=parser#parser is a object of class
        self.save=save#save is a function
        self.save_params=save_params
        self.cookies=None
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }

    def login(self,login_url,home_page_url):
        '''
        login
        :param login_url: the url you want to login
        :param login_data_parser: a callback function to get the login_data you need when you login,return (login_data,response.cookies)
        :param target_url: Used to determine if you have logged in successfully

        :return: response of login
        '''

        login_data=None

        #get the login data
        login_data,cookies=self.parser.login_data_parser(login_url)

        #login without redirecting
        response=requests.post(login_url,headers=self.headers,data=login_data,cookies=cookies,allow_redirects=False)

        cookies_num=1
        while(home_page_url!=None and response.url!=home_page_url):#if spider is not reach the target page
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

        if(home_page_url!=None and response.url==home_page_url):
            print("login successfully")

        self.cookies=cookies
        return response

    def crawl(self,login_url,home_page_url,catalogue_url):
        self.login(login_url,home_page_url)
        url_list=self.parser.get_urls(catalogue_url,cookies=self.cookies,headers=self.headers)
        for url in url_list:
            content=self.parser.get_content(url,cookies=self.cookies,headers=self.headers)
            self.save(content,**self.save_params)


    def __del__(self):
        pass