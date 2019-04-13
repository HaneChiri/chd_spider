from lxml import etree
import requests
url='https://www.biquge.biz/2_2224/'

response=requests.get(url)
html=etree.HTML(response.text)
content=html.xpath('/html/head/title')

print(content.text)

for i in content:
    print(i.text)