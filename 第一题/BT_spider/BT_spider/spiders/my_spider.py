# -*- coding: utf-8 -*-
import scrapy
from BT_spider.items import BtSpiderItem
import re

class MySpiderSpider(scrapy.Spider):
    name = 'my_spider'
    allowed_domains = ['www.5186.net']  #
    start_urls = ['https://www.5186.net/article-index-id-7-p-{}'.format(i) for i in range(100,103)]
    URLS = []
    TITLES = []
    def parse(self, response):
        a_all=response.xpath('//dl/dd/h3/a[re:test(@href,"/article-show-id-\d+")]')
        for a in a_all:
            url=a.xpath('./@href').extract()[0]
            title=a.xpath('./@title').extract()[0]
            url=response.urljoin(url)
            if not url in self.URLS and not title in self.TITLES:  #标题和url没有抓取过
                yield scrapy.Request(url,callback=self.conten_parse,meta={'url':url,'title':title})
    def conten_parse(self,response):
        item=BtSpiderItem()
        title=response.meta['title']
        url=response.meta['url']
        conten=response.xpath('//div[@class="article-content"]').extract()[0]
        item['ID']=url
        r1=u'文章转载于\S+|<.*?>|[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        title=re.sub(r1,'',title)#正则过滤
        item['title']=title.replace('')
        item['conten']=conten
        yield item
        self.URLS.append(url)
        self.TITLES.append(title)





