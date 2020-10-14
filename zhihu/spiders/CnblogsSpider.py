import scrapy
from scrapy import Selector

from zhihu import items


class CnblogsspiderSpider(scrapy.Spider):
    name = 'cnSpider'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.cnblogs.com/qiyeboy/default.htmlpage=1']

    def parse(self,response):
        #实现网页的解析
        #首先抽取所有的文章
        global item
        papers = response.xpath('.//*[@class="day"]')

        for paper in papers:
            url = paper.xpath(".// *[@class='dayTitle']/a/@href").extract()[0]
            time = paper.xpath(".// *[@class='dayTitle']/a/text()").extract()[0]
            title = paper.xpath(".//*[@class='postTitle']/a/span/text()").extract()[0]
            content = paper.xpath(".// *[@class='postCon']/div/text()").extract()[0]
            item = items.CnblogsItem(url = url,time = time,title = title,content = content)
            request = scrapy.Request(url = url, callback=self.parse_body)
            request.meta['item'] = item  #将item暂存
            yield request

        next_page  = Selector(response).re('<a href="(\S*)">下一页</a>')
        if next_page:
            yield scrapy.Request(url=next_page[0],callback=self.parse)

    def parse_body(self,response):
        item = response.meta['item']
        body = response.xpath(".//*[@class = 'postBody']")
        item['cimage_urls'] = body.xpath('.// img// @src').extract()  # 提取图片链接
        yield item


