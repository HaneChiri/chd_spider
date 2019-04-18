import pymysql

db_data={
        'host':'127.0.0.1',
        'user':'root',
        'passwd':'password',
        'port':3306,
        'charset':'utf8',
        'db':'news'
    }

#1 连接
conn=pymysql.connect(**db_data)

#2 构建sql语句字符串，能在命令行执行
sql='insert into new_table(idnew_table) value(788)'

#3 创建游标对象

cur=conn.cursor()


#4 执行sql语句

cur.execute(sql)

#4 提交修改

conn.commit()


