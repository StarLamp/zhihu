import json

import scrapy
from zhihu import items

class BaiduComSpider(scrapy.Spider):
    name = 'baiduSpider'
    allowed_domains = ['baidu.com']
    start_urls = ['http://baidu.com/']

    def parse(self, response):
        key_word = '哈士奇'
        base_url = 'https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&word={0}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&pn=90&rn=30&gsm=3c&1507915209449='\
            .format(key_word)
        item = items.BaiduPicItem()
        request = scrapy.Request(base_url,callback=self.parse_body,dont_filter=True)
        request.meta['item'] = item
        yield request

    def parse_body(self,response):
        response_json = response.text  # 存储返回的json数据
        response_dict = json.loads(response_json)  # 转化为字典
        response_dict_data = response_dict['data']  # 图片的有效数据在data参数中
        item = response.meta['item']
        for pic in response_dict_data:  # pic为每个图片的信息数据，dict类型
            if pic:
                item['image_urls'] = [pic['middleURL']] # 百度图片搜索结果url (setting中pic_url应该为数组形式)
                yield item


class MySpider(scrapy.Spider):
    name = 'myspider'
    def start_requests(self):
        return [scrapy.FormRequest("http://www.example.com/login",
                                   formdata={'user': 'john', 'pass': 'secret'},callback=self.login)]
    def login(self, response):
        pass
