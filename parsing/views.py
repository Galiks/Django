import logging
import time

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from parsing_methods.ds4Parsing import BS4Parsing
from parsing_methods.request_letyshops_parsing import RequestsLetyShopsParsing
from parsing_methods.requestsParsing import RequestsParsing
from parsing_methods.scrapyParsing.scrapyParsing.spiders.arcady_spider import MainClassForScrapy
from parsing_methods.webDriverParsing import WebDriverParsing
from .models import Shop, Timer

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return HttpResponse("Hello! If you're admin, please, log in")


def shops(request):
    shop_list = get_shops_from_DB()
    template = loader.get_template('shops.html')
    context = {'shop_list': shop_list}
    # return render(request, 'shops.html', context)
    return HttpResponse(template.render(context, request))


def get_shops_from_DB():
    return Shop.objects.order_by('-name')


def parse(request):
    global method
    Shop.objects.all().delete()
    Timer.objects.all().delete()
    # methods = [
    #     RequestsParsing(),
    #     BS4Parsing(),
    #     WebDriverParsing(),
    #     RequestsLetyShopsParsing(),
    # ]
    # shops = []
    # for method in methods:
    #     try:
    #         start_time = time.time()
    #         shops.append(method.parsing())
    #         timer = Timer(name=method.get_name_class(),
    #                       time=(time.time() - start_time))
    #         timer.save()
    #     except Exception as e:
    #         logger.error("Ошибка при проходе методов : " + e.__str__())
    try:
        start_time = time.time()
        spider = MainClassForScrapy()
        timer = Timer(name=method.get_name_class(),
                      time=(time.time() - start_time))
        timer.save()
        save_shops_in_DB_for_scrapy(spider)
    except Exception as e:
        logger.error("Ошибка при запуске Scrapy: " + e.__str__())
    # save_shops_in_DB(shops)
    context = get_shops_from_DB()
    return render(request, 'shops.html', context)


def save_shops_in_DB_for_scrapy(spider):
    shops_list = spider.get_data_from_json()
    for shop in shops_list:
        new_shop = Shop(name=shop["name"],
                        discount=shop["discount"],
                        label=shop["label"],
                        image=shop["image"],
                        url=shop["url"])
        new_shop.save()


def save_shops_in_DB(shops):
    shop_list = []
    for shop in shops:
        for item in shop:
            shop_list.append(item)
    for shop in shop_list:
        try:
            new_shop = Shop(name=shop.name, discount=shop.discount, label=shop.label, url=shop.url, image=shop.image)
            new_shop.save()
        except AttributeError as e:
            continue


def save_shops_in_excel():
    pass
