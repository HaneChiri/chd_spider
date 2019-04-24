'''
模块名：my_database
定义的类：MyDatabase
简介：对pymysql模块的简单封装

'''

import pymysql


class MyDatabase(object):
    def __init__(self,*args,**kwargs):
        self.conn=pymysql.connect(*args,**kwargs)
        self.cursor=self.conn.cursor()

    def execute(self,sql):
        '''
        执行sql语句
        :param sql: 需要执行的sql语句字符串
        '''
        self.cursor.execute(sql)
        self.conn.commit()
        return self.cursor.fetchall()

    def insert(self,db,table,record_dict):
        '''
        插入记录
        :param db:字符串，指定数据库名
        :param table:字符串，指定表名
        :param record_dict:字典，包含记录的数据

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
    
    def select(self,db,table,column_list):
        sql='use {}'.format(db)
        self.execute(sql)


        sql='select '
        i=0
        for column in column_list:
            
            sql+=str(column)
            i+=1
            if i<len(column_list):
                sql+=','
            
        
        sql+=' from {}'.format(table)

        return self.execute(sql)


    def table_isexist(self,db,table):
        '''
        检测表是否存在

        :param db:字符串，指定数据库名
        :param table:字符串，指定表名
        '''
        sql='use {}'.format(db)
        self.execute(sql)

        sql='show tables;'
        for i in self.execute(sql):
            if table in i:
                return True
        else:
            return False

    def db_isexist(self,db):
        '''
        检测数据库是否存在
        :param db:字符串，指定数据库名
        '''
        sql='show databases;'
        self.cursor.execute(sql)
        for i in self.execute(sql):
            if db in i:
                print('True')
                return True
        else:
            print('False')
            return False

    def record_isexist(self,db,table,primary_key,find_value):
        '''
        检测记录是否存在

        :param db:字符串，指定数据库名
        :param table:字符串，指定表名
        :param primary_key:字符串，指定主键字段名
        :param find_value:字符串，可以区分记录是否存在的值
        '''
        sql='use {}'.format(db)
        self.execute(sql)

        sql='select * from {} where {}="{}"'.format(table,primary_key,find_value)
        res=self.execute(sql)

        if res!=tuple():
            return True

        else:
            return False


    def create_db(self,db):
        '''
        创建数据库
        :param db:字符串，指定数据库名
        '''
        sql='create database {};'.format(db)
        self.execute(sql)
    
    def create_table(self,db,table,column):
        '''
        创建表
        :param table:字符串，指定表名
        '''
        sql='use {}'.format(db)
        self.execute(sql)

        sql='create table {};'.format(table)
        self.execute(sql)

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

    for i in mydb.select('dbase','spider',['url','title']):
        print(i)

    
