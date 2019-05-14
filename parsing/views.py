from django.http import HttpResponse
from django.shortcuts import get_list_or_404, render
from django.template import loader

from parsing_methods.requestsParsing import RequestsParsing
from .models import Shop


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
    parsing = RequestsParsing()
    shops = parsing.parsing()
    shop_list = []
    for shop in shops:
        for item in shop:
            shop_list.append(item)
    for shop in shop_list:
        new_shop = Shop(name=shop.name, discount=shop.discount, label=shop.label, url=shop.url, image=shop.image)
        new_shop.save()
    context = {'shop_list': shop_list}
    return render(request, 'shops.html', context)
