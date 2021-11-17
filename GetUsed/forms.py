from django.db import models
from django import forms
from .models import Search

class SellChoice(models.TextChoices):
    none = '指定なし', '指定なし'
    sold_out = '売り切れ', '売り切れ'
    sell_now = '販売中', '販売中'

class CategoryChoice(models.TextChoices):
    none = '指定なし', '指定なし'
    computer = 'コンピュータ', 'コンピュータ'
    books = '本・雑誌', '本・雑誌'
    contents = 'ゲーム・音楽・アニメ映画', 'ゲーム・音楽・アニメ映画'
    HomeAppliances = '家電・AV・カメラ','家電・AV・カメラ'
    fashion = 'ファッション', 'ファッション'
    beauty = '美容・コスメ・香水', '美容・コスメ・香水'
    interior = 'インテリア', 'インテリア'
    outdoor = 'スポーツ・レジャー', 'スポーツ・レジャー'
    goods = 'おもちゃ・グッズ', 'おもちゃ・グッズ'
    food = '食料', '食料'
    car = '自動車・オートバイ', '自動車・オートバイ'

class KeywordForm(forms.Form):
    keyword = forms.CharField(
        label="探したい商品の名前",
        max_length=40,
        required=True,
    )

    min_price = forms.IntegerField(
        initial=0,
        label="探したい商品の下限金額",
        required=True,
    )
    max_price = forms.IntegerField(
        initial=0,
        label="探したい商品の上限金額",
        required=True,
    )

    sold_out = forms.ChoiceField(
        label="商品が売り切れか販売中か",
        choices=SellChoice.choices,
        required=False,
    )

    category = forms.ChoiceField(
        label="商品のカテゴリ",
        choices=CategoryChoice.choices,
        required=False,
    )

    def save(self):
        data = self.cleaned_data
        search = Search(keyword=data["keyword"], min_price=data["min_price"],
                        max_price=data["max_price"], sold_out=data["sold_out"], category=data["category"])
        search.save()


