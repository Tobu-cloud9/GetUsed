from django.db import models
from accounts.models import CustomUser

class Search(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user', on_delete=models.CASCADE)
    keyword = models.CharField(verbose_name='keyword', max_length=40, null=True)
    max_price = models.PositiveIntegerField(verbose_name='max_price', blank=True, null=True)
    min_price = models.PositiveIntegerField(verbose_name='min_price', blank=True, null=True)
    status = models.CharField(verbose_name='status',max_length=20, blank=True, null=True)
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

    class SellChoice(models.TextChoices):
        none = '指定なし', '指定なし'
        sold_out = '売り切れ', '売り切れ'
        sell_now = '販売中', '販売中'

    class Category(models.TextChoices):
        none = 'none', '指定なし'
        computer = 'computer', 'コンピュータ'
        books = 'books', '本・雑誌'
        game = 'game', 'ゲーム'
        music = "music", "音楽・CD"
        movie = "movie", "映画・ビデオ"
        HomeAppliances = 'HomeAppliances', '家電・AV・カメラ'
        fashion = 'fashion', 'ファッション'
        beauty = 'beauty', '美容・コスメ・香水'
        interior = 'interior', 'インテリア'
        outdoor = 'outdoor', 'スポーツ・レジャー'
        goods = 'goods', 'おもちゃ・グッズ'
        food = 'food', '食料'
        car = 'car', '自動車・オートバイ'

    item_type = models.CharField(verbose_name='shop', max_length=1, choices=ItemType, null=True)
    item_category = models.CharField(verbose_name='category', max_length=20, choices=Category.choices, null=True, default="指定なし")
    keyword = models.CharField(verbose_name='keyword', max_length=40, null=True)
    item_link = models.CharField(verbose_name='link', max_length=200, blank=True, null=True)
    item_price = models.PositiveIntegerField(verbose_name='price', blank=True, null=True)
    item_date = models.CharField(verbose_name='date', max_length=10, blank=True, null=True)
    item_name = models.CharField(verbose_name='name', max_length=200, blank=True, null=True)
    item_buy_price = models.PositiveIntegerField(verbose_name='buy_price', blank=True, null=True, default=0)
    item_limit = models.CharField(verbose_name='time_limit', max_length=10, blank=True, null=True, default="なし")
    item_status = models.CharField(verbose_name='status', max_length=10, choices=SellChoice.choices, null=True, default="指定なし　")
    item_image = models.CharField(verbose_name='image', max_length=500, blank=True, null=True)

    def __str__(self):
        return self.keyword
