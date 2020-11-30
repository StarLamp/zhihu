import base64
import hashlib
import json
import re
import threading
import time
from http import cookiejar
from urllib.parse import urlencode

import scrapy
from PIL import Image
from scrapy import Request, Selector, FormRequest
import hmac
import requests

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
        self.session = requests.session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded'
        }
        self.session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')


    def parse(self, response):
        pass


    def start_requests(self, captcha_lang: str = 'en', load_cookies: bool = True):
        #首先进入登录界面
        login_url = 'https://www.zhihu.com'
        if load_cookies and self.load_cookies():
            print('读取Cookies')
            if self.check_login():
                print('登录成功')
                return True
            print('cookies 已过期')
        self._check_user_pass()
        self.login_data.update({
            'username':self.username,
            'password':self.password,
            'lang': captcha_lang
        })
        #界面登录
        return [Request(login_url,callback=self.start_login,meta={'cookiejar':1})]


    def start_login(self,response):
        self.session.post(self.login_url,self.login_data)


    def _get_signature(self):
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4',digestmod=hashlib.sha1())
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        timestamp = self.login_data['timestamp']
        ha.update((grant_type+client_id+source+timestamp).encode('utf-8'))
        return ha.hexdigest()

    def load_cookies(self):
        '''
        判断cookies是否存在
        :return:
        '''
        try:
            self.session.cookies.values()
            return True
        except FileNotFoundError:
            return False

    def check_login(self):
        """
        检查登录状态，访问登录页面出现跳转则是已登录，
        如登录成功保存当前 Cookies
        :return: bool
        """
        login_url = 'https://www.zhihu.com/signup'
        resp = self.session.get(login_url, allow_redirects=False)
        if resp.status_code == 302:
            return True
        return False

    def _get_xsrf(self):
        """
        从登录页面获取 xsrf
        :return: str
        """
        self.session.get('https://www.zhihu.com/', allow_redirects=False)
        for c in self.session.cookies:
            if c.name == '_xsrf':
                return c.value
        raise AssertionError('获取 xsrf 失败')

    def _get_captcha(self, lang: str):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        根据 lang 参数匹配验证码，需要人工输入
        :param lang: 返回验证码的语言(en/cn)
        :return: 验证码的 POST 参数
        """
        if lang == 'cn':
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        resp = self.session.get(api)
        show_captcha = re.search(r'true', resp.text)

        if show_captcha:
            put_resp = self.session.put(api)
            json_data = json.loads(put_resp.text)
            img_base64 = json_data['img_base64'].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open('./captcha.jpg')
            if lang == 'cn':
                import matplotlib.pyplot as plt
                plt.imshow(img)
                print('点击所有倒立的汉字，在命令行中按回车提交')
                points = plt.ginput(7)
                capt = json.dumps({'img_size': [200, 44],
                                   'input_points': [[i[0] / 2, i[1] / 2] for i in points]})
            else:
                img_thread = threading.Thread(target=img.show, daemon=True)
                img_thread.start()
                # 这里可自行集成验证码识别模块
                capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={'input_text': capt})
            return capt
        return ''

    def _get_signature(self, timestamp: int or str):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + str(timestamp)), 'utf-8'))
        return ha.hexdigest()

    def _check_user_pass(self):
        """
        检查用户名和密码是否已输入，若无则手动输入
        """
        if not self.username:
            self.username = input('请输入手机号：')
        if self.username.isdigit() and '+86' not in self.username:
            self.username = '+86' + self.username

        if not self.password:
            self.password = input('请输入密码：')

    @staticmethod
    def _encrypt(form_data: dict):
        with open('./encrypt.js') as f:
            js = execjs.compile(f.read())
            return js.call('b', urlencode(form_data))