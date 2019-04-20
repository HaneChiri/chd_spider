#author:憧憬少
#update:2019-3-8
'''
可爬取长安大学信息门户的通知公告，可以选择保存在数据库或者文本文件

'''
import requests
import re
from bs4 import BeautifulSoup
import pymysql


def login():
    """
    登录并返回已经登录的会话
    :return: 已经登录的会话（session）
    """
    #设置
    login_url = 'http://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fportal.chd.edu.cn%2F'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        #'Host':'ids.chd.edu.cn',
        #'Referer':'http://ids.chd.edu.cn/authserver/login?service=http://portal.chd.edu.cn/index.portal',
        #'Origin':'http://ids.chd.edu.cn'
        #去掉多余的头信息才成功登录！！！！！卡了很久没想到是因为这个
    }
    #新建会话
    session=requests.session()

    #获取登录校验码
    html=session.post(login_url,headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    lt=soup.find('input',{'name':'lt'})['value']
    dllt=soup.find('input',{'name':'dllt'})['value']
    execution = soup.find('input', {'name': 'execution'})['value']
    _eventId = soup.find('input', {'name': '_eventId'})['value']
    rmShown = soup.find('input', {'name': 'rmShown'})['value']
    login_data={
        'username': input("请输入学号："),
        'password': input("请输入密码："),
        'btn':'',
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _eventId,
        'rmShown': rmShown
    }

    #登录
    response=session.post(login_url,headers=headers,data=login_data)
    if response.url=='http://portal.chd.edu.cn/':
        print('登录成功！')

    return session

def saveInTXT(url, session, title):
    '''
    获取单个新闻页面的新闻并保存到txt
    :param url: 要获取的页面的url
    :param session:已经登录的会话
    :param title:新闻标题
    :return:无
    '''

    #将标题转换为可以作为文件名字的形式
    reg = r'[\/:*?"<>|]'
    title = re.sub(reg, "", title)

    path= title+'.txt'#保存在py文件目录下的news文件夹内，以txt格式保存
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    '''
    #测试代码，从文件读取手动获取的新闻html页面，单机测试
    with open('new.txt','r',encoding='utf8') as fin:
        html=fin.read()
    '''
    html=session.post(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    #print(soup.prettify())
    article=soup.find('div',class_='bulletin-content')

    news_content=''
    for p in article.find_all('p'):
        if p.span!=None:#如果p含有一层span
            text=str(p.get_text()).strip()
            news_content+=text+'\n'

    with open(path,'w',encoding='utf8') as fout:
        fout.write(news_content)

    print('“{}”成功保存到{}'.format(title,path))


def saveInDB(url, session, title):
    '''
    获取单个新闻页面的新闻并保存到txt
    :param url: 要获取的页面的url
    :param session:已经登录的会话
    :param title:新闻标题
    :return:无
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }

    html=session.post(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    article=soup.find('div',class_='bulletin-content')

    news_content=''
    for p in article.find_all('p'):
        if p.span!=None:#如果p含有一层span
            text=str(p.get_text()).strip()
            news_content+=text+'\n'

    #保存到数据库
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='news', charset='utf8')
    cursor = db.cursor()
    cursor.execute("insert into chdnews(`title`,`content`) values('{0}','{1}')".format(title, news_content))
    db.commit()

    print('已经成功保存新闻到数据库：“{}”'.format(title))



def get_news(page_count):
    '''
    新闻目录有多页，从第一页开始获取，往后获取page_count页的目录，并读取目录指向的所有新闻
    :param page_count: 要爬取的目录页面的数量
    :return: 无
    '''
    para={
        'pageIndex':1,
        'pageSize':'',
        '.pmn':'view',
        '.ia':'false',
        'action':'bulletinsMoreView',
        'search':'true',
        'groupid':'all',
        '.pen':'pe65'
    }
    catalogue_url='http://portal.chd.edu.cn/detach.portal'#未加参数的新闻目录页url
    session = login()  # 获取已登录的session
    for i in range(1,page_count+1):
        para['pageIndex']=i#设置新闻当前页的索引

        # 从目录页获取新闻页面链接
        html = session.post(catalogue_url,params=para).text
        soup = BeautifulSoup(html, 'lxml')
        rss_title = soup.find_all('a', class_='rss-title')
        #将得到的链接与标题组装成字典
        news_dict = {}
        for url in rss_title:
            news_title = str(url.span.string).strip()
            news_url = 'http://portal.chd.edu.cn/' + url['href']
            news_dict.setdefault(news_title, news_url)#添加一条新闻记录

        #保存新闻到数据库
        for news_title, news_url in news_dict.items():
            saveInTXT(news_url, session, news_title)#这个是保存到txt文件的函数，用于测试
            #saveInDB(news_url, session, news_title)

#调用
get_news(10)