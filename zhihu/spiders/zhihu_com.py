import hashlib
import time

import scrapy
from scrapy import Request, Selector, FormRequest
import hmac


class ZhihuComSpider(scrapy.Spider):
    name = 'zhihu.com'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']
    login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

    def __init__(self, name=None, **kwargs):
        super().__init__(name, kwargs)
        self.login_data = {
            'grant_type': "password",
            'client': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'timestamp': str(int(time.time()*1000)),
            'source':'com.zhihu.web',
        }

    def parse(self, response):
        pass

    def start_requests(self):
        #首先进入登录界面
        login_url = 'https://www.zhihu.com'
        header={
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'content-type':'application/x-www-form-urlencoded'
        }
        #界面登录
        return [Request(login_url,callback=self.start_login,meta={'cookiejar':1})]

    def start_login(self,response):
       return [FormRequest(
           self.login_url,
           method='POST',

       )]


    def _get_signature(self):
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=hashlib.sha1())
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        timestamp = self.login_data['timestamp']
        ha.update((grant_type+client_id+source+timestamp).encode('utf-8'))
        return ha.hexdigest()