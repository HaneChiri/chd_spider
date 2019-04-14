from lxml import etree
import requests

xml='''


<!DOCTYPE html>
<html lang="zh-cn">
<head>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-878633-1"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-878633-1');
</script>

<meta charset="gbk" />
<meta name="robots" content="all" />
<meta name="author" content="w3school.com.cn" />
<link rel="stylesheet" type="text/css" href="/c5.css" />
<link rel="icon" type="image/png" sizes="16x16" href="/ui2019/w3_16x16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/ui2019/w3_32x32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/ui2019/logo-48-red.png">
<link rel="icon" type="image/png" sizes="96x96" href="/ui2019/logo-96-red.png">
<link rel="apple-touch-icon-precomposed" sizes="180x180" href="/ui2017/logo-180.png">


<title>XPath</title>

</head>

<body class="xml">

<div id="wrapper">
...


</div>
</body>
</html>
'''


xml=etree.HTML(xml)
list=xml.xpath('/html')

print(type(list))

print(list)
for i in list:
    print(i)