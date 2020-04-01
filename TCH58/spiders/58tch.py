# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
import re
from lxml import etree
from urllib.parse import urlencode

class A58tchSpider(scrapy.Spider):
    name = '58tch'
    allowed_domains = ['58.com']
    start_urls = ['https://www.58.com/changecity.html']

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('lang=zh_CN.UTF-8')
        self.chrome_options.add_argument('disable-infobars')
        self.chrome_options.add_argument('accept-encoding=gzip, deflate, br')
        self.chrome_options.add_argument('cache-control=max-age=0')
        self.chrome_options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        self.chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"')
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        self.wait = WebDriverWait(self.browser, 30)

    def __del__(self):
        self.browser.close()
        print("爬取结束")

    def parse(self, response):
        # print(response.text)
        self.browser.get(response.url)
        doc = pq(self.browser.page_source)
        urls = doc('.content-letter')
        urls = str(urls)
        urls = re.findall('href="(.*?)"', urls)
        for url in urls:
            base_url = "https:" + url + '/job'
            return Request(base_url, self.parse_example)
            # print(base_url)

    def get_targetPage(self):
        handle = self.browser.current_window_handle
        handles = self.browser.window_handles
        try:
            for newhandle in handles:
                # 筛选新打开的窗口
                if newhandle != handle:
                    self.browser.switch_to_window(newhandle)
                    print('爬取url： ', self.browser.current_url)
                    self.parse_message(self.browser.page_source)
                    self.browser.close()
                    print('关闭浏览器')
                    self.browser.switch_to_window(handles[0])
        except:
            print('获取详情页出错')



    def parse_example(self,response):
        self.browser.get(response.url)
        try:
            links = self.get_job_element()
        except:
            print('网页信息有误')
            return None
        print("一共有{}条记录".format(len(links)))
        for link in links:
            link.click()
            self.get_targetPage()
        try:
            print('进入下一页')
            next = self.browser.find_element_by_class_name("next")
            while next:
                next.click()
                print('\n现在的Url是:{}\n'.format(self.browser.current_url))
                links = self.get_job_element()
                for link in links:
                    link.click()
                    self.get_targetPage()
                next = self.browser.find_element_by_class_name("next")
        except:
            print('没有下一页了')

    def get_job_element(self):
        try:
            links = self.browser.find_elements_by_xpath(
                "//li[contains(@class,'job_item')]/div[contains(@class,'job_title')]//a")
            return links
        except:
            print('网页信息有误')
            return None

    def parse_message(self,response):
        print('开始爬取详情页')
        soup = BeautifulSoup(response, 'html.parser')
        try:
            print('文件打开')
            file = open('record.txt', 'a+', encoding='utf-8')
        except:
            print('文件打开出错')
        try:
            # item = Tch58Item()
            job = soup.select('.pos_title')
            company = soup.select('.baseInfo_link')
            salery = soup.select('.pos_salary')
            message_1 = soup.select('.pos_base_condition')
            message_2 = soup.select('.pos_welfare')
            message_job1 = soup.select('.des')
            message_job2 = soup.select('.pos_name')
            contact = soup.select('.pos_area_span')
            message_company = soup.select('.shiji')
            place = soup.select('.pos_area_item')
            message_company2_1 = soup.select('.pass_identify')
            message_company2_2 = soup.select('.comp_baseInfo_scale')
            message_company2_3 = soup.select('.comp_baseInfo_belong')
            try:
                place = place[0].get_text("|", strip=True)
            except:
                place = None
            try:
                job = job[0].get_text("|", strip=True)
            except:
                job = None
            try:
                company = company[0].get_text("|", strip=True)
            except:
                company = None
            try:
                salery = salery[0].get_text("|", strip=True).replace('|', ' ')  # 上面获取的salery表单第一个为广告 第二个为需要的数据
            except:
                salery = None
            try:
                message_1 = message_1[0].get_text("|", strip=True).replace('|||', ' | ')
            except:
                message_1 = None
            try:
                message_2 = message_2[0].get_text("|", strip=True).replace('|', ' ')
            except:
                message_2 = None
            try:
                message_job1 = message_job1[0].get_text("|", strip=True).replace('|', '')
            except:
                message_job1 = None
            try:
                message_job2 = message_job2[0].get_text("|", strip=True).replace('|', '')
            except:
                message_job2 = None
            try:
                contact = contact[0].get_text("|", strip=True).replace('|', '')
            except:
                contact = None
            try:
                message_company = message_company[0].get_text("|", strip=True).replace('|', '')
            except:
                message_company = None
            try:
                message_company2_1 = message_company2_1[0].get_text("|", strip=True).replace('|', '')
            except:
                message_company2_1 = None
            try:
                message_company2_2 = message_company2_2[0].get_text("|", strip=True).replace('|', '')
            except:
                message_company2_2 = None
            try:
                message_company2_3 = message_company2_3[0].get_text("|", strip=True).replace('|', '')
            except:
                message_company2_3 = None
            # item['job'] = job
            # item['company'] = company
            # item['salery'] = salery
            # item['message_1'] = message_1
            # item['message_2'] = message_2
            # item['message_job1'] = message_job1
            # item['message_job2'] = message_job2
            # item['contact'] = contact
            # item['message_company'] = message_company
            # item['place'] = place
            # item['message_company2_1'] = message_company2_1
            # item['message_company2_2'] = message_company2_2
            # item['message_company2_3'] = message_company2_3
            print('job:{}'.format(job))
            print('company:{}'.format(company))
            print('salary:{}'.format(salery))
            print('message_1:{}'.format(message_1))
            print('message_2:{}'.format(message_2))
            print('message_job1:{}'.format(message_job1))
            print('message_job2:{}'.format(message_job2))
            print('contact:{}'.format(contact))
            print('message_company:{}'.format(message_company))
            print('place:{}'.format(place))
            print('message_company2_1:{}'.format(message_company2_1))
            print('message_company2_2:{}'.format(message_company2_2))
            print('message_company2_3:{}'.format(message_company2_3))
            print("开始写入文件：")
            file.write(str(job) + '\t' + str(company) + '\t' + str(salery) + '\t'
                       + str(message_1) + '\t' + str(message_2) + '\t' + str(place) + '\n')
            file.close()
            # yield item
        except:
            print('爬取出错没有数据')
            return None
