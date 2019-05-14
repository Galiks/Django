from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404
from django.template import loader

from .models import Shop


# Create your views here.
def index(request):
    return HttpResponse("Hello! If you're admin, please, log in")


def shops(request):
    shop_list = get_list_or_404(Shop.objects.order_by('-name'))
    template = loader.get_template('shops.html')
    context = {'shop_list': shop_list}
    # return render(request, 'shops.html', context)
    return HttpResponse(template.render(context, request))
