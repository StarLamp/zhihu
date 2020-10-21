# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CnblogsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()

class BaiduPicItme(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    search_word = scrapy.Field()


class UserInfoItem(scrapy.Item):
# define the fields for your item here like:
# id
    user_id = scrapy.Field()
# 头像img
    user_image_url = scrapy.Field()
# 姓名
    name = scrapy.Field()
# 居住地
    location = scrapy.Field()
# 技术领域
    business = scrapy.Field()
# 性别
    gender = scrapy.Field()
# 公司
    employment = scrapy.Field()
# 职位
    position = scrapy.Field()
# 教育经历
    education = scrapy.Field()
# 我关注的人数
    followees_num = scrapy.Field()
# 关注我的人数
    followers_num = scrapy.Field()

class RelationItem(scrapy.Item):
# 用户id
    user_id =scrapy.Field()
# relation 类型
    relation_type =scrapy.Field()
# 和我有关系的人的id列表
    relations_id = scrapy.Field()
