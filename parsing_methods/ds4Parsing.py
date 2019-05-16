import time
from multiprocessing import Pool

import requests
from bs4 import BeautifulSoup

import parsing_methods.valueForParsing as v
from parsing_methods.parsingAbstractClass import Parsing
from parsing_methods.shop import Shop


class BS4Parsing(Parsing):

    def get_name_class(self):
        return type(self).__name__

    def __init__(self):
        pass

    def parsing(self):
        """Возвращает список элементов"""
        urls = []
        max_page = self.__get_max_page()
        for i in range(1, max_page + 1):
            urls.append(v.url_for_parsing_letyShops + str(i))
        pool = Pool(processes=4)
        result = pool.map(self.parse_elements, urls)
        shops = []
        for items in result:
            for item in items:
                shops.append(item)
        return shops

    def parse_elements(self, url):
        result = []
        soup = BeautifulSoup(self.__get_Html(url), 'lxml')
        shops = soup.find_all('div', class_='b-teaser')
        for shop in shops:
            name = self.__get_name(shop)
            discount = self.__get_discount(shop)
            label = self.__get_label(shop)
            url = self.__get_url(shop)
            image = self.__get_image(shop)
            if name is not None and discount is not None and label is not None and image is not None and url is not None:
                result.append(Shop(name=name, discount=discount, label=label, image=image, url=url))
        return result

    def __get_image(self, shop):
        image = shop.find('div', class_='b-teaser__cover').find('img').get('src')
        return image

    def __get_url(self, shop):
        url = shop.find('a', class_='b-teaser__inner').get('href')
        return v.clear_url_letyShops + url

    def __get_label(self, shop):
        label = shop.find('span', class_='b-shop-teaser__label ')
        if label is None:
            label = shop.find('span', class_='b-shop-teaser__label--red')
            if label is None:
                label = shop.find_all('span', class_='b-shop-teaser__label')[-1]
        else:
            label = label
        return label.text.strip()

    def __get_discount(self, shop):
        discount = shop.find('span', class_='b-shop-teaser__cash')
        if discount is None:
            discount = shop.find('span', class_='b-shop-teaser__new-cash').text.strip()
        else:
            discount = discount.text.strip()
        return discount

    def __get_name(self, shop):
        name = shop.find('div', class_='b-teaser__title').text.strip()
        return name

    def __get_Html(self, url):
        try:
            r = requests.get(url)
            return r.text
        except ConnectionError as e:
            print("Error")

    def __get_max_page(self):
        soup = BeautifulSoup(self.__get_Html(v.letyShops), 'lxml')
        new_pages = []
        pages = soup.find_all('a', class_='b-pagination__link')
        for page in pages:
            new_page = int(page.get('data-page'))
            new_pages.append(new_page)
        return max(new_pages)

    def print_array(self, array: []):
        if len(array) > 0:
            for item in array:
                print(item.__str__())
        else:
            print("Пустой список")


if __name__ == '__main__':
    parser = BS4Parsing()
    parser.parsing()
