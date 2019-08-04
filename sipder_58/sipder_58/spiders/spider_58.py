import scrapy
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from ..items import Sipder58Item

class spider_58(scrapy.Spider):
    name = 'spider_58'
    allowed_domains = ['58.com']
    list_keyword = ['新闻','编辑出版','播音主持','产品设计','传播','广播电视','广告','摄影','视觉传达']
    start_urls = ['https://www.58.com/changecity.html']

    #获取城市链接
    def make_requests_from_url(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'content-box')))
        cities = browser.find_elements_by_class_name("content-city")
        for c in cities:
            url = c.get_attribute("href")
            for keyword in self.list_keyword:
                url_city = 'http:' + url + '/job/?key=' + keyword + '&classpolicy=main_null,job_A&final=1&jump=1'
                self.get_url_job(url_city,keyword)
        browser.close()

    #获取职位链接
    def get_url_job(self,url_city,keyword):
        while 1:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.get(url_city)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'list_con')))
            urls_job = browser.find_elements_by_class_name("job_name")
            for url_job in urls_job:
                yield scrapy.Request(url=url_job.get_attribute("href"), callback=self.parse, meta={'keyword': keyword}, dont_filter=True)
            #下一页
            try:
                url_city = browser.find_elements_by_class_name("next").get_attribute("href")
            except:
                url_city = 'javascript:void(0)'
            if url_city == 'javascript:void(0)':
                break

    def parse(self, response):
        html = etree.HTML(response.text)

        job = html.xpath("string(//span[@class='pos_title'])")  # 职位
        requirement = html.xpath("string(//div[@class='pos_base_condition'])")  # 招聘要点
        company = html.xpath("string(//div[@class='baseInfo_link']//a)")  # 公司名称
        salary = html.xpath("string(//span[@class='pos_salary'])")  # 工资
        contact = html.xpath("string(//span[@class='pos_area_span pos_address'])")  # 联系方式
        job_information = html.xpath(
            "string(//div[@class='subitem_con pos_description']//div[@class='posDes'])")  # 职位信息
        place = html.xpath("string(//span[@class='pos_area_item'][1])")  # 工作地点
        welfare = html.xpath("string(//div[@class='pos_welfare'])")  # 福利
        company_message = html.xpath("string(//div[@class='subitem_con comp_intro']//div[@class='txt'])")  # 公司详细信息
        company_direction = html.xpath("string(//p[@class='comp_baseInfo_belong']//a)")  # 公司类型
        company_category = html.xpath("string(//span[@class='identify_item pass_identify']//span)")  # 公司性质
        other = html.xpath("string(//span[@class='pos_name'])")
        item = Sipder58Item()

        try:
            item['place'] = place #工作地点
        except:
            item['place'] = None
        try:
            item['requirement'] = requirement  # 招聘要点
        except:
            item['requirement'] = None
        try:
            item['job'] = job #职位名称
        except:
            item['job'] = None
        try:
            item['company'] = company #公司名称
        except:
            item['company'] = None
        try:
            item['salary'] = salary #工资
        except:
            item['salary'] = None
        try:
            item['contact'] = contact #联系方式
        except:
            item['contact'] = None
        try:
            item['job_information'] = job_information #职位信息
        except:
            item['job_information'] = None
        try:
            item['welfare'] = welfare#福利
        except:
            item['welfare'] = None
        try:
            item['company_category'] = company_category #公司性质
        except:
            item['company_category'] = None
        try:
            item['company_member'] = company_message #公司人数
        except:
            item['company_member'] = None
        try:
            item['company_direction'] = company_direction #公司类别
        except:
            item['company_direction'] = None
        try:
            item['other'] = other #其他
        except:
            item['other'] = None
        item['keyword'] = response.meta['keyword']
        item['link'] = response.url
        item['time'] = str(datetime.date.today())
        yield item