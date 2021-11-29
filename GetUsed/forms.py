from django.db import models
from django import forms
from .models import Search

class SellChoice(models.TextChoices):
    none = '指定なし', '指定なし'
    sold_out = '売り切れ', '売り切れ'
    sell_now = '販売中', '販売中'

class CategoryChoice(models.TextChoices):
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
        return data["keyword"], data["min_price"], data["max_price"], data["category"]