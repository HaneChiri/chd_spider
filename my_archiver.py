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


    

