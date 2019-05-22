import csv
import io
import json
import os
import time
from datetime import datetime

import requests
import scrapy
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

import parsing_methods.valueForParsing as v

items = []


def get_max_page():
    soup = BeautifulSoup(get_Html(v.letyShops), 'lxml')
    new_pages = []
    pages = soup.find_all('a', class_='b-pagination__link')
    for page in pages:
        new_page = int(page.get('data-page'))
        new_pages.append(new_page)
    return max(new_pages)


def get_Html(url):
    try:
        r = requests.get(url)
        return r.text
    except ConnectionError as e:
        print("Error")


class MainClassForScrapy():
    """Класс для запуска паука и записи данных в json"""
    file_name = 'E:/Документы/PyCharmProject/Django/files/shops.json'

    items = []

    def __init__(self):
        self.delete_file(self.file_name)
        start_time = time.time()
        process = CrawlerProcess()
        process.crawl(ArcadySpider)
        process.start()
        end_time = time.time()
        self.create_file_with_time(end_time - start_time)
        self.create_json_file(items)

    def get_data_from_json(self):
        with io.open(self.file_name, 'r', encoding='utf8') as file:
            data = json.load(file)
            file.close()
            return data

    def create_json_file(self, shops):
        with io.open(self.file_name, 'a+', encoding='utf8') as file:
            json.dump(shops, file, indent=2, ensure_ascii=False)
            file.close()

    def delete_file(self, file):
        if os.path.exists(file):
            os.remove(file)

    def create_file_with_time(self, timer):
        now_date = datetime.today()
        file_name_for_time = 'E:/Документы/PyCharmProject/Django/files/times_of_scrapy_for_' \
                             + str(now_date).replace(':', '.') + '.csv'
        with open(file_name_for_time, 'w') as file:
            columns = ['name', 'time', 'date']
            writer = csv.DictWriter(file, fieldnames=columns)
            new_time = {'name': 'ArcadySpider',
                        'time': timer,
                        'date': datetime.today(),
                        }
            writer.writerow(new_time)


class ArcadySpider(scrapy.Spider):
    name = "arcady"
    address = "https://letyshops.com/shops?page="
    clear_address = 'https://letyshops.com'
    allowed_domains = ['https://letyshops.com']
    start_urls = []
    max_page = get_max_page()
    for i in range(1, max_page + 1):
        start_urls.append(address + i.__str__())

    rules = (
        Rule(LinkExtractor(allow=('')), callback="parse", follow=False)
    )

    def parse(self, response):
        shops = response.xpath('//div[@class="b-teaser"]')
        for i, shop in enumerate(shops):
            item = {
                'name': self.get_name(shop, i),
                'discount': self.get_discount(shop, i),
                'label': self.get_label(shop, i),
                'image': self.get_image(shop, i),
                'url': self.get_url(shop, i)
            }
            items.append(item)
        return items

    def get_name(self, shop, i):
        index = i + 1
        name = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']//div[@class="b-teaser__title"]//text()').get().strip()
        return name

    def get_url(self, shop, i):
        index = i + 1
        url = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']//a[@class="b-teaser__inner"]/@href').extract()
        return self.clear_address.__str__() + url[0]

    def get_discount(self, shop, i):
        index = i + 1
        discount = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__cash"]/text()').get()
        if discount is None:
            discount = shop.xpath(
                '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__new-cash"]/text()').get()
            print(discount)
            return discount
        return discount

    def get_label(self, shop, i):
        index = i + 1
        label = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__label "]/text()').get()
        if label is None:

            label = shop.xpath(
                '//div[@class="b-teaser"][' + index.__str__() + ']/a//span[@class="b-shop-teaser__label b-shop-teaser__label--red"]/text()')
            return label
        return label

    def get_image(self, shop, i):
        index = i + 1
        image = shop.xpath(
            '//div[@class="b-teaser"][' + index.__str__() + ']//div[@class="b-teaser__cover"]/img/@src').extract()
        return image


if __name__ == '__main__':
    main = MainClassForScrapy()
