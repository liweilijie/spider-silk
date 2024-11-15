# spider-silk
All spider program.

## python and scrapy

virtualenv最流行的虚拟环境管理工具。

```bash
pip3 install virtualenv
python3 -m venv article
source article/bin/activate

pip list
pip freeze > requirements.txt
pip install -r requirements.txt
deactivate
```

**scrapy**使用的twitted架构，原理还是事件循环+回调模式，单线程机制处理的任务。

![scrapy](images/scrapy.jpeg)

```bash
# create project
scrapy startproject article
# generic one spider
scrapy genspider cnblogs "www.cnblogs.cn"
# run spider
scrapy crawl cnblogs
```

## cnblogs
