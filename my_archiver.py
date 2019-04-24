from my_database import MyDatabase

class MyArchiver(object):
    def __init__(self,database_name,table_name,**config):
        self.config=config
        self.database_name=database_name
        self.table_name=table_name
        self.db=MyDatabase(**config)

    def save(self,record_dict):#call
        self.save_in_db(record_dict)

    def save_in_db(self,record_dict):
        #todo: error deal
        flag=self.isexist('url',record_dict['url'])
        if flag:
            print('this record has existed') 
        else:
            self.db.insert(self.database_name,self.table_name,record_dict)

    def isexist(self,primary_key,find_value):
        return self.db.record_isexist(self.database_name,self.table_name,primary_key,find_value)

    def reduce_crawled_url(self,url_list):
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

    

