from django import template
register = template.Library()

@register.filter(name="category")
def category(value):
    CATEGORY = {
        'none':'指定なし',
        'computer': 'コンピュータ',
        'books': '本・雑誌',
        'contents': 'ゲーム・音楽・アニメ映画',
        'HomeAppliances': '家電・AV・カメラ',
        'fashion': 'ファッション',
        'beauty':'美容・コスメ・香水',
        'interior': 'インテリア',
        'outdoor':'スポーツ・レジャー',
        'goods': 'おもちゃ・グッズ',
        'food': '食料',
        'car': '自動車・オートバイ',
    }
    return CATEGORY[value]
