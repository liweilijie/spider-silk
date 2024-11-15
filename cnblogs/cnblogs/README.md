# cnblogs
crawl的时候需要的技术



## xpath

xpath语法：

article: 选择所有article元素的所有子节点
/article: 选取根元素article
article/a 选择所有属于article的子元素的a元素
//div 选择所有div子元素,无论出现在文档的任何地方
article//div 选取所有属于article元素的后代的div元素，不管它出现在article之下的任何位置 
//@class 选取所有名为class的属性

xpath语法-谓语：

/article/div[1]: 选取属于article子元素的第一个div元素
/article/div[last()]
/article/div[last()-1]
//div[@lang] 选取所有拥有lang属性的div元素
//div[@lang='eng'] 选取所有lange属性为eng的div元素

xpath常用：

/div/* 选取属于div元素的所有子节点
//* 选取所有元素
//div[@*] 选取所有带属性的title元素
//div/a | //div/p 选取所有div元素的a和p元素
//span | //ul 选取文档中的span和ul元素


```python
url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
```

## css selector

语法：

`*` 选择所有节点
`#container` 选择id为container的节点
`.container` 选取所有class包含container的节点
`li a` 选取所有li下的所有a节点
`ul + p` 选择ul后面的第一个p元素
`div#container > ul` 选取id为container的div的ul子元素


```python
url = response.css('div#news_list h2.news_entry a::attr(href)').extract_first("")
```

构建一个selector基于text文本内容：

```python
from scrapy import Selector
sel = Selector(text=response.text)
sel.css('div#news_list h2 a::attr(href)').extract()
sel.xpath('//div[@id="news_list"]//h2/a/@href').extract_first()
```