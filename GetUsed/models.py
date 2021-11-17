from django.db import models
from accounts.models import CustomUser

class Search(models.Model):
    #user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    keyword = models.CharField(verbose_name='keyword', max_length=40, null=True)
    max_price = models.PositiveIntegerField(verbose_name='max_price', blank=True, null=True)
    min_price = models.PositiveIntegerField(verbose_name='min_price', blank=True, null=True)
    sold_out = models.CharField(verbose_name='sold_out',max_length=20, blank=True, null=True)
    category = models.CharField(verbose_name='category', max_length=20, blank=True, null=True)

class Item(models.Model):
    keyword = models.OneToOneField(Search, related_name='search_item', on_delete=models.CASCADE, null=True)
    item_id = models.PositiveIntegerField(verbose_name='id', blank=True, null=True)
    item_price = models.PositiveIntegerField(verbose_name='price', blank=True, null=True)
    item_date = models.DateField(verbose_name='date', blank=True, null=True)
    item_name = models.CharField(verbose_name='name', max_length=40, blank=True, null=True)
    item_buy_price = models.PositiveIntegerField(verbose_name='buy_price', blank=True, null=True)
    item_limit = models.PositiveIntegerField(verbose_name='time_limit', blank=True, null=True)

    def __str__(self):
        return self.keyword
