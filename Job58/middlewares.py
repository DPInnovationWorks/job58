# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import logging
from fake_useragent import UserAgent

class RedirectMiddleware(object):
    def process_response(self, request, response, spider):
        http_code = response.status
        logging.info(response.url)
        if 'verifycode' in response.url:
            logging.warning("请求过于频繁，触发验证码机制")
            spider.crawler.engine.close_spider(spider, "关闭爬虫")
            return request
        else:
            return response
class RandomUserAgentMiddleware(object):
    def __init__(self,crawler):
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)

    def process_request(self,request,spider):
        request.headers.setdefault("User-Agent",self.ua.random)