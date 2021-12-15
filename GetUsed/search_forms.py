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

class QualityChoice(models.TextChoices):
    none = '指定なし', '指定なし'
    rankA = '新品未使用に近い', '新品未使用に近い'
    rankB = '目立った傷なし', '目立った傷なし'
    rankC = 'やや傷汚れあり', 'やや傷汚れあり'
    rankD = '傷汚れあり', '傷汚れあり'
    rankJ = 'ジャンクのみ', 'ジャンクのみ'

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

    status = forms.ChoiceField(
        label="商品が売り切れか販売中か",
        choices=SellChoice.choices,
        required=False,
    )

    category = forms.ChoiceField(
        label="商品のカテゴリ",
        choices=CategoryChoice.choices,
        required=False,
    )

    quality = forms.ChoiceField(
        label = "商品の品質",
        choices=QualityChoice.choices,
        required=False,
    )

    def save(self, user_id):
        data = self.cleaned_data
        search = Search(user=user_id, keyword=data["keyword"], min_price=data["min_price"],
                        max_price=data["max_price"], status=data["status"], category=data["category"], quality=data["quality"])
        search.save()
        return data["keyword"], data["min_price"], data["max_price"], data["category"], data["status"], data["quality"]