# 长安大学信息门户爬虫

爬取学校信息门户公告，并存到数据库

# 我的相关博客

- [1 小说爬虫](https://hanechiri.github.io/post/python_spider_note1simple_spider/)
- [2 模拟登录与数据库](https://hanechiri.github.io/post/python_spider_note2login_and_database/)
- [3 爬虫类](https://hanechiri.github.io/post/python_spider_note3class_spider/)
- [4 模拟登录函数的优化](https://hanechiri.github.io/post/python_spider_note4optimization_of_the_login_function/#more)
- [5 爬虫类结构优化](https://hanechiri.github.io/post/python_spider_note5optimization_of_the_spider_class/#more)



# 模块简介

注：历史版本存放在`practice`目录下

| 模块                   | 简介                                                         |
| ---------------------- | ------------------------------------------------------------ |
| newsSpider.py          | 第一版实现功能的代码，只是简单地将代码装在函数内             |
| bulletin_spider.py     | 第二版，简单封装为类        |
| spider_class.py        | 第三版，进一步优化                                           |
| my_database.py         | 对pymysql模块的简单封装                                      |
| my_spider.py           | 定义了爬虫类的基类，构造时需要传入MyParser类的解析器，和MyArchiver类的存档器 |
| my_parser.py           | 给MySpider类使用的解析器的基类                               |
| my_Archiver.py         | 给MySpider类使用的存档器的基类，目前仅支持基于pymysql的数据库存储，以后可能会增加新的存储方式 |
| chd_bulletin_spider.py | 第四版，爬取长安大学信息门户公告，并存到数据库               |



# 进度

- [x] 模拟登录

- [x] 解析内容

- [x] 本地存储

- [x] 博客总结

- [x] 面向对象

- [x] 结构优化

- [x] 全面注释

- [x] 爬取去重

- [ ] 实时更新

- [ ] 异常处理

  