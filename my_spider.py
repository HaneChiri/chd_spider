import requests

'''
模块名：my_spider
定义的类：MySpider
简介：定义了爬虫类的基类，构造时需要传入MyParser类的解析器，和MyArchiver类的存档器
'''

class MySpider(object):
    def __init__(self,parser,archiver,**config):
        self.parser=parser#解析器，类型为MyParser
        self.archiver=archiver#存档器，类型为MyArchiver
        self.config=config#配置

        self.cookies=None
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }

    def login(self,login_url,home_page_url):
        '''
        登录
        :param login_url: 登录页面的网址
        :param home_page_url: 登录之后跳转到的页面，一般而言是主页，以下称其为主页

        流程：
        1.获取登录表单信息（例如账号密码以及隐藏域）
        2.一步步跳转到主页以获取完整cookies并储存在对象属性当中

        '''

        login_data=None

        #获取登录信息
        login_data,cookies=self.parser.login_data_parser(login_url)

        #获取cookies
        response=requests.post(login_url,headers=self.headers,data=login_data,cookies=cookies,allow_redirects=False)
        while(home_page_url!=None and response.url!=home_page_url):#如果未跳转到主页，那么就继续跳转
            #合并新获取到的cookies
            cookies=dict(cookies,**response.cookies)
            cookies=requests.utils.cookiejar_from_dict(cookies)
            next_station=response.headers['Location']#这是下一个需要跳转的url
            response=requests.post(next_station,headers=self.headers,cookies=cookies,allow_redirects=False)

        cookies=dict(cookies,**response.cookies)
        cookies=requests.utils.cookiejar_from_dict(cookies)

        self.cookies=cookies

        #提示信息
        if(home_page_url!=None and response.url==home_page_url):
            print("login successfully")

        

    def crawl(self,login_url,home_page_url,catalogue_url):
        '''
        爬取。生成一个MySpider之后，只要一声令下（调用此函数），就可以开始爬取网站。

        :param login_url: 登录页面的网址
        :param home_page_url: 登录之后跳转到的页面，一般而言是主页，以下称其为主页
        :param catalogue_url: 有着需要爬取的网页的url的目录网页的url

        流程：
        1.登录
        2.从目录网页获取需要爬取的url列表
        3.用解析器解析网页并利用存档器保存

        '''
        #登录
        self.login(login_url,home_page_url)
        #获取需要爬取的url列表
        url_list=self.parser.get_urls(catalogue_url,cookies=self.cookies,headers=self.headers)
        url_list=self.archiver.reduce_crawled_url(url_list)#去除已经爬取的url免得重复爬取
        #获取url列表里面每个url指向的网页的内容
        counter=0
        total=len(url_list)
        for url in url_list:
            counter+=1
            #提示信息
            print('[@spider]:get content({}%): {}/{}'.format(round((counter/total)*100,2),counter,total))
            #获取单个页面
            record_dict=self.parser.get_content(url,cookies=self.cookies,headers=self.headers)
            self.archiver.save(record_dict)


    def __del__(self):
        pass