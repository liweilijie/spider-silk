import json
import re
from gc import callbacks
from typing import Iterable
from urllib import parse


import scrapy
import undetected_chromedriver
from scrapy import Request
import requests

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["news.cnblogs.com"]
    start_urls = ["https://news.cnblogs.com"]

    custom_settings = {
        "COOKIES_ENABLED": True # cookies自动往后面传给其他爬取的链接
    }

    def start_requests(self):
        import undetected_chromedriver as uc
        CHROME_DRIVER_PATH = '/usr/local/bin/chromedriver'
        driver = uc.Chrome(driver_executable_path=CHROME_DRIVER_PATH)
        driver.get('https://account.cnblogs.com/signin')
        input("回车继续：")
        cookies = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie['name']] = cookie['value']

        for url in self.start_urls:
            headers = {
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0',
            }
            yield scrapy.Request(url, cookies=cookie_dict, headers=headers, dont_filter=True)


    def parse(self, response):
        # url = response.xpath('//*[@id="entry_780565"]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
        # url = response.css('div#news_list h2.news_entry a::attr(href)').extract_first("")
        # post_nodes = response.css('#news_list .news_block')[:1]
        post_nodes = response.css('#news_list .news_block')
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(href)').extract_first("")
            post_url = post_node.css('h2 a::attr(href)').extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)

        # 提取下一页并交给scrapy进行下载
        # 用css提取
        # next_url = response.css("div.pager a:last-child::text").extract_first("")
        # if next_url == 'Next >':
        #     next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)
        # 用xpath的方式进行提取
        next_url = response.xpath("//a[contains(text(), 'Next >')]/@href").extract_first("")
        yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            post_id = match_re.group(1)
            # title = response.css("#news_title a::text").extract_first("")
            title = response.xpath("//*[@id='news_title]//a/text()").extract_first("")
            # create_date = response.css("#news_info .time::text").extract_first("")
            create_date = response.xpath("//*[@id='news_info']//*[@class='time']/text()").extract_first("")
            match_re = re.match(".*?(\d+.*)", create_date)
            if match_re:
                create_date = match_re.group(1)
            # content = response.css("#news_content").extract()[0]
            content = response.xpath("//*[@id='news_content']").extract()[0]
            # tag_list = response.css(".news_tags a::text").extract()
            tag_list = response.xpath("//*[@class='news_tags']//a/text()").extract()
            tags = ",".join(tag_list)

            # 使用同步的requests进行获取
            # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))
            # j_data = json.loads(html.text)
            #
            # praise_nums = j_data["DiggCount"]
            # fav_nums = j_data["TotalView"]
            # comment_nums = j_data["CommentCount"]

            # 使用异步获取
            yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)), callback=self.parse_nums)

    def parse_nums(self, response):
        j_data = json.loads(response.text)

        praise_nums = j_data["DiggCount"]
        fav_nums = j_data["TotalView"]
        comment_nums = j_data["CommentCount"]
