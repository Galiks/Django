import time

from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from django.template import loader

from parsing_methods.ds4Parsing import BS4Parsing
from parsing_methods.request_letyshops_parsing import RequestsLetyShopsParsing
from parsing_methods.requestsParsing import RequestsParsing
from parsing_methods.webDriverParsing import WebDriverParsing
from .models import Shop, Timer


# Create your views here.
def index(request):
    return HttpResponse("Hello! If you're admin, please, log in")


def shops(request):
    shop_list = Shop.objects.order_by('-name')
    template = loader.get_template('shops.html')
    context = {'shop_list': shop_list}
    # return render(request, 'shops.html', context)
    return HttpResponse(template.render(context, request))


def parse(request):
    Shop.objects.all().delete()
    Timer.objects.all().delete()
    methods = [
            # RequestsParsing(),
            # BS4Parsing(),
            # WebDriverParsing(),
            RequestsLetyShopsParsing(),
        ]
    shops = []
    for method in methods:
        try:
            start_time = time.time()
            shops.append(method.parsing())
            timer = Timer(name=method.get_name_class(),
                          time=(time.time() - start_time))
            timer.save()
        except Exception as e:
            continue
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
    context = {'shop_list': shop_list}
    return render(request, 'shops.html', context)
