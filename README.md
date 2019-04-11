# Spider

This is a repository for spider learning.

# My blog

- [python_spider_note 1 | simple_spider](https://hanechiri.github.io/post/python_spider_note1simple_spider/)

- [python_spider_note 2 | login_and_database](https://hanechiri.github.io/post/python_spider_note2login_and_database/)

- [python_spider_note 3 | spider_class](https://hanechiri.github.io/post/python_spider_note3class_spider/)


# Module Brief

| module             | brief                                                        |
| ------------------ | ------------------------------------------------------------ |
| newsSpider.py      | It can crawl the news of chd information site,and save them by txt |
| bulletin_spider.py | A modified version of  `newsSpider.py`,with some bugs        |
| spider_class.py    | A modified version of  `bulletin_spider.py`,without completing |
| my_database.py     | Simple packaging for `pymysql` to adapt to my spider         |



# Current Progress

- [x] spider.login()
- [x] MyDatabase.insert()
- [ ] spider.get_urls()#get all urls to crawl,return a url list
- [ ] spider.parse()#parse single page by a callback function,return a result dict
- [ ] spider.crawl()#call spider's method to crawl a site
- [ ] etc.