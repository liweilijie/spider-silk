import scrapy


class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["news.cnblogs.com"]
    start_urls = ["https://news.cnblogs.com"]

    def parse(self, response):
        # url = response.xpath('//*[@id="entry_780565"]/div[2]/h2/a/@href').extract_first("")
        # url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
        url = response.css('div#news_list h2.news_entry a::attr(href)').extract_first("")
        pass
