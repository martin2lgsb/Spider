from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor

from douban_spider.items import DoubanSpiderItem

class DoubanSpider(CrawlSpider):

    name = "douban_movie_spider"

    download_delay = 2
    cookies_enabled = False
    allowed_domains = ['movie.douban.com']
    start_urls = [
        'https://movie.douban.com/top250?start=0&filter=&type='
    ]

    rules = (
        Rule(LinkExtractor(
        allow = (r'https://movie\.douban\.com/top250\?start=\d+&filter=&type=')),
        callback = 'parse_item',
        follow = True
        ),
    )


    def parse_item(self, response):

        print response

        sel = Selector(response)
        item = DoubanSpiderItem()

        item['movie_name'] = sel.xpath('//span[@class="title"][1]/text()').extract()
        item['star'] = sel.xpath('//div[@class="star"]/span[@class="rating_num"]/text()').extract()
        item['quote'] = sel.xpath('//p[@class="quote"]/span[@class="inq"]/text()').extract()
        yield item

        nextPage = sel.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract()[0]
        print nextPage
        if nextPage:
            next_url = 'https://movie.douban.com/top250' + nextPage
            yield Request(next_url, callback = self.parse_item)
