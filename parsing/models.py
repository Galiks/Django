from django.db import models


# Create your models here.

class Shop(models.Model):
    """Модель для хранения магазинов с сайта"""
    name = models.CharField(max_length=200)
    discount = models.FloatField()
    label = models.CharField(max_length=10)
    url = models.URLField()
    image = models.TextField()

    def __str__(self):
        return self.name + "\n" \
               + self.discount.__str__() + " " + self.label + "\n" \
               + self.image + "\n" \
               + self.url + "\n"


class Timer(models.Model):
    """Модель для хранения времени парсинга сайта"""
    name = models.CharField(max_length=200)
    time = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + "\n" \
               + self.time.__str__() + "\n" \
               + self.date.__str__() + "\n"
