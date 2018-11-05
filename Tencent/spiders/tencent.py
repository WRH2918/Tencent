# -*- coding: utf-8 -*-
import scrapy
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    base_url = 'https://hr.tencent.com/position.php?&start='
    offset = 0
    start_urls = [base_url+str(offset)]

    def parse(self, response):
        # print(response.body)
        content = response.xpath("//tr[@class='even'] | //tr[@class='odd'] ")
        for node in content:
            item = TencentItem()
            print(node.extract())
            positionName = node.xpath("./td[1]/a/text()").extract()
            positionLink = node.xpath("./td[1]/a/@href").extract()
            if len(node.xpath("./td[2]/text()").extract()):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0]
            else:
                item['positionType'] = ""

            peopleNumber = node.xpath("./td[3]/text() ").extract()
            workLocation = node.xpath("./td[4]/text() ").extract()
            publishTime =  node.xpath("./td[5]/text()").extract()
            item['positionName'] = positionName[0]
            item['positionLink'] = positionLink[0]
            # item['positionType'] = positionType[0]
            item['peopleNumber'] = peopleNumber[0]
            item['workLocation'] = workLocation[0]
            item['publishTime'] = publishTime[0]
            yield item
            # print(positionName)
        # if self.offset<2890:
        #     self.offset+=10
        #     url = self.base_url+str(self.offset)
        #     yield scrapy.Request(url,callback=self.parse)

        #提取下一页的地址，如何最后一页为空，则说明最后一页，利用回调的Request发送
        if not len(response.xpath("// a[ @class ='noactive' and @ id='next']")):
            url = response.xpath("//a[@id='next']/@href").extract()[0]
            yield scrapy.Request("https://hr.tencent.com/"+url,callback=self.parse)
    # def parse_next(self,response):
    #     pass