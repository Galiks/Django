from django.contrib import admin

# Register your models here.

from .models import Shop, Timer

admin.site.register(Shop)
admin.site.register(Timer)