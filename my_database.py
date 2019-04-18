import pymysql


class MyDatabase(object):
    def __init__(self,*args,**kwargs):
        self.conn=pymysql.connect(*args,**kwargs)
        self.cursor=self.conn.cursor()
        
        

    def insert(self,db,table,record_dict):
        '''

        :param db:name of database that you want to use
        :param table:name of table that you want to use
        :param record_dict:key for column,value for value

        '''
        sql='use {}'.format(db)
        self.cursor.execute(sql)
        self.conn.commit()

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


        print(sql)

            


        self.cursor.execute(sql)
        self.conn.commit()
    
    def show(self):
        pass


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
    mydb.insert('news','new_table',test_record)
    del mydb
