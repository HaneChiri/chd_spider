"""
目前问题：cookie到期之后得手动删除cookie文件才能成功登录

"""
import requests
from bs4 import BeautifulSoup
import pymysql
import re
import http.cookiejar

class spider:
    '''
    爬虫类
    '''

    def __init__(self,headers):
        self.session=requests.session()#初始化登录session
        self.is_login=False#登录状态
        self.headers=headers#头信息
        self.cookiejar=http.cookiejar.LWPCookieJar('cookie.txt')

    def get_login_data(self,login_url):
        '''
        获取登录需要的数据
        :param login_url: 登录页面url
        :return: 一个存有登录数据的字典
        '''
        # 获取登录校验码
        html = self.session.post(login_url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        lt = soup.find('input', {'name': 'lt'})['value']
        dllt = soup.find('input', {'name': 'dllt'})['value']
        execution = soup.find('input', {'name': 'execution'})['value']
        _eventId = soup.find('input', {'name': '_eventId'})['value']
        rmShown = soup.find('input', {'name': 'rmShown'})['value']
        login_data = {
            'username': input("请输入学号："),
            'password': input("请输入密码："),
            'btn': '',
            'lt': lt,
            'dllt': dllt,
            'execution': execution,
            '_eventId': _eventId,
            'rmShown': rmShown
        }
        return login_data

    def login(self,login_url):
        """
            登录并返回已经登录的会话
            :return: 已经登录的会话（session）
        """
        if self.load_cookie():
            self.is_login = True

        else:

            #获取登录信息
            login_data=self.get_login_data(login_url)

            # 登录
            response = self.session.post(login_url, headers=self.headers, data=login_data)
            if response.url!=login_url:
                print("登录成功")
                self.is_login=True
                self.save_cookie()
            else:
                print("登录失败")
        return self.session

    def parse(self, html, tag_type, ret, **attr):
        '''
        解析网页并提取其中的正文
        :param html: 网页的源代码
        :param tag_type:目标标签的种类，如div
        :param ret:目标标签的目标属性，指定要返回的内容，如href中的值
        :param attr:要提取的标签的属性
        :return: 字符串结果集
        '''

        soup = BeautifulSoup(html, 'lxml')
        tag=soup.find(tag_type, attrs=attr)

        if ret== 'get_text':
            result=tag.get_text()
        elif ret=='tagself':
            result=tag
        else:
            result= tag[ret]


        print(result)
        return result

    def post(self,url):
        response=self.session.post(url,headers=self.headers)
        return response

    def get_url_from_cata(self,url,params):
        '''
        返回当前页面的url组成的列表
        :param url: 无参数的url
        :param params:url的？后参数
        :return:以页面指向的标题和url组成的元组为元素的列表，即[(title,content),(title,content)]的形式
        '''

        #获取url域名部分
        base=url.split('/')
        base=base[0]+'//'+base[2]

        #获取当前页所有链接
        html = self.session.post(url,params=params).text#用params参数来拼接参数
        soup = BeautifulSoup(html, 'lxml')
        rss_title = soup.find_all('a', class_='rss-title')#获取所有链接

        result_list=[]
        for url in rss_title:
            title=url.get_text().strip()
            page_url=base+'/'+url['href']#将url拼接完整
            l=(title,page_url)
            result_list.append(l)

        #print(result_list)
        return result_list

    def get_url_from_cata_all(self, url):
        '''
        获取页面的底部跳转到其他页的链接并获取目录，给出一个目录页的url，获取相关的所有目录页的url并获取链接
        :param url: 其中任何一个目录页的url
        :return:以所有页面的标题和url组成的元组为元素的列表，即[(title,content),(title,content)]的形式
        '''

        #获取除去参数之后的url
        base=url.split('?')[0]


        html = self.session.post(url).text
        soup = BeautifulSoup(html, 'lxml')
        #print(soup.prettify())
        # 获取页数
        reg = '共.*?条记录 分(.*?)页显示'
        print(html)
        num = int(re.findall(reg, str(soup.prettify()))[0])

        #获取url
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
        ret=[]
        for i in range(1,2):#=====================这里为了测试，将num+1改为2，以免等待过久
            ret.extend(self.get_url_from_cata(base,params=para))
            para['pageIndex'] = i

        return ret

    def get_page(self,url):
        '''
        提取页面中的公告正文
        :param url: 页面url
        :return: 正文
        '''
        html = self.session.post(url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')


        bulletin_content = soup.find('div', class_='bulletin-content')

        bulletin_content =bulletin_content.get_text()

        return bulletin_content

    def save_by_txt(self,file_content,file_name):
        '''
        获取单个公告页面的公告并保存到txt
        :param file_content:文件内容(str)
        :param file_name:输出文件名(str)
        :return:无
        '''
        # 转换为可以作为文件名字的形式
        reg = r'[\/:*?"<>|]'
        file_name = re.sub(reg, "", file_name)

        with open(file_name, 'w', encoding='utf8') as fout:
            fout.write(file_content)

        print('成功保存到{}'.format(file_name))

    def save_by_db(self,content,title):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='news', charset='utf8')
        cursor = db.cursor()
        cursor.execute("insert into spider(`title`,`content`) values('{0}','{1}')".format(title, content))
        db.commit()
        print('已经成功保存公告到数据库：“{}”'.format(title))

    def save_cookie(self):
        requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies}, self.cookiejar)
        # 保存到本地文件
        self.cookiejar.save('cookies')

    def load_cookie(self):
        '''
        加载cookie
        :return: 是否成功
        '''
        load_cookiejar = http.cookiejar.LWPCookieJar()
        # 从文件中加载cookies(LWP格式)
        try:
            load_cookiejar.load('cookies')
        except:
            print('cookie加载失败')
            return False

        # 转换成字典
        load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
        # 将字典转换成RequestsCookieJar，赋值给session的cookies.
        self.session.cookies = requests.utils.cookiejar_from_dict(load_cookies)
        return True

    def crawl(self,login_url,cata_url):
        self.login(login_url)#登陆
        print(self.is_login)
        item_list=self.get_url_from_cata_all(cata_url)#获取所有标题以及对应链接
        for i in item_list:
            title,url=i#解包
            text=self.get_page(url)#获取内容
            self.save_by_txt(text,title+'.txt')#保存
            #self.save_by_db(text,title)



headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}
login_url='http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
cata_url='http://portal.chd.edu.cn/detach.portal?pageIndex=1&pageSize=&.pmn=view&.ia=false&action=bulletinsMoreView&search=true&groupid=all&.pen=pe65'



#调用
spiderman=spider(headers)
spiderman.crawl(login_url, cata_url)


