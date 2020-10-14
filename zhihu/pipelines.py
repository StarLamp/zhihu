# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
from scrapy.exceptions import DropItem


class ZhihuPipeline:
    def process_item(self, item, spider):
        return item

class CnblogspiderPipeline:
    def __init__(self):
        self.file = open('pager.json','wb')

    def process_item(self,item,spider):
        if item['title']:
            line = json.dumps(dict(item))+"\n"
            self.file.write(line.encode(encoding='utf-8'))
            print(str)
            return item
        else:
            raise  DropItem("Missing title in %s" % item)



