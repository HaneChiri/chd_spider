'''
模块名：my_archiver
定义的类：MyArchiver
简介：给MySpider类使用的存档器的基类，目前仅支持基于pymysql的数据库存储，以后可能会增加新的存储方式

'''



from my_database import MyDatabase

class MyArchiver(object):
    def __init__(self,database_name,table_name,**config):
        self.config=config#配置
        self.database_name=database_name#使用的数据库名
        self.table_name=table_name#使用的表名
        self.db=MyDatabase(**config)#创建一个

    def save(self,record_dict):
        '''
        MySpider类当中调用此方法，派生类如果需要使用其他保存方法，只需覆盖此方法
        :param record_dict:存有记录的字典
        '''
        self.save_in_db(record_dict)

    def save_in_db(self,record_dict):
        '''
        保存到数据库

        :param record_dict:存有记录的字典
        '''
        self.db.insert(self.database_name,self.table_name,record_dict)

    def isexist(self,primary_key,find_value):
        '''
        返回find_value是否在primary_key字段内存在
        '''
        return self.db.record_isexist(self.database_name,self.table_name,primary_key,find_value)

    def reduce_crawled_url(self,url_list):
        '''
        将获取到的url_list去除数据库中已有的部分

        :param url_list:需要处理的url列表

        :return: url_list当中，未被存储到数据库中的url的列表
        '''
        result=self.db.select(self.database_name,self.table_name,['url'])

        db_url_list=[]
        for i in result:
            db_url_list.append(i[0])

        uncrawed_url=list(set(url_list) - set(db_url_list))
        return uncrawed_url
        

if __name__ == '__main__':
    connect_config={
        'host':'127.0.0.1',
        'user':'root',
        'passwd':'password',
        'port':3306,
        'charset':'utf8',
    }
    
    archiver=MyArchiver('dbase','spider',**connect_config)
    print(archiver.reduce_crawled_url(['http://portal.chd.edu.cn/detach.portal?.pmn=view&.ia=false&action=bulletinBrowser&.pen=pe65&bulletinId=035be7f3-6022-11e9-952d-7ba9f1ad5e4b']))

    

