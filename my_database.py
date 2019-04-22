import pymysql


class MyDatabase(object):
    def __init__(self,*args,**kwargs):
        self.conn=pymysql.connect(*args,**kwargs)
        self.cursor=self.conn.cursor()

    def execute(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def insert(self,db,table,record_dict):
        '''

        :param db:name of database that you want to use
        :param table:name of table that you want to use
        :param record_dict:key for column,value for value

        '''
        sql='use {}'.format(db)
        self.execute(sql)

        sql='insert into {}('.format(table)
        
        record_list=list(record_dict.items())

        for r in record_list:
            sql += str(r[0])
            if r != record_list[-1]:
                sql += ','

        sql+=') values('

        for r in record_list:
            sql += '"'
            sql += str(r[1])
            sql += '"'
            if r != record_list[-1]:
                sql += ','


        sql+=')'


        self.execute(sql)
    
    def table_isexist(self,db,table):
        sql='use {}'.format(db)
        self.execute(sql)

        sql='show tables;'
        for i in self.execute(sql):
            if table in i:
                return True
        else:
            return False

    def db_isexist(self,db):
        sql='show databases;'
        self.cursor.execute(sql)
        for i in self.execute(sql):
            if db in i:
                print('True')
                return True
        else:
            print('False')
            return False

    def create_db(self,db):
        sql='create database {};'.format(db)
        self.execute(sql)
    
    def create_table(self,db,table,column):
        sql='use {}'.format(db)
        self.execute(sql)

        sql='create table {};'.format(table)
        self.execute(sql)


    def record_isexist(self,db,table,primary_key,find_value):
        sql='use {}'.format(db)
        self.execute(sql)

        sql='select * from {} where {}="{}"'.format(table,primary_key,find_value)
        res=self.execute(sql)

        if res!=tuple():
            return True

        else:
            return False



    



    def __del__(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    db_data={
        'host':'127.0.0.1',
        'user':'root',
        'passwd':'password',
        'port':3306,
        'charset':'utf8'
    }
    test_record={
        'idnew_table':'233'
    }

    mydb=MyDatabase(**db_data)
    
    mydb.record_isexist('news','spider','title','2019年度因公国公示12')
    
