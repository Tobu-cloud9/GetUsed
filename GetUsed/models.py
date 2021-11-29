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
    ItemType = (
        ('Y', 'ヤフオク'),
        ('M', 'メルカリ'),
        ('P', 'PayPayフリマ'),
        ('R', 'ラクマ'),
        ('H', 'ハードオフ'),
        ('m', 'モバオク'),
        ('E', 'ebay'),
        ('S', 'セカイモン'),
    )

    class Category(models.TextChoices):
        none = 'none', '指定なし'
        computer = 'computer', 'コンピュータ'
        books = 'books', '本・雑誌'
        contents = 'contents', 'ゲーム・音楽・アニメ映画'
        HomeAppliances = 'HomeAppliances', '家電・AV・カメラ'
        fashion = 'fashion', 'ファッション'
        beauty = 'beauty', '美容・コスメ・香水'
        interior = 'interior', 'インテリア'
        outdoor = 'outdoor', 'スポーツ・レジャー'
        goods = 'goods', 'おもちゃ・グッズ'
        food = 'food', '食料'
        car = 'car', '自動車・オートバイ'

    item_type = models.CharField(verbose_name='shop', max_length=1, choices=ItemType, null=True)
    item_category = models.CharField(verbose_name='category', max_length=20, choices=Category.choices, null=True)
    keyword = models.CharField(verbose_name='keyword', max_length=40, null=True)
    item_link = models.CharField(verbose_name='link', max_length=200, blank=True, null=True)
    item_price = models.PositiveIntegerField(verbose_name='price', blank=True, null=True)
    item_date = models.CharField(verbose_name='date', max_length=10, blank=True, null=True)
    item_name = models.CharField(verbose_name='name', max_length=200, blank=True, null=True)
    item_buy_price = models.PositiveIntegerField(verbose_name='buy_price', blank=True, null=True)
    item_limit = models.CharField(verbose_name='time_limit', max_length=5, blank=True, null=True)

    def __str__(self):
        return self.keyword
