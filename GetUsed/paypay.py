from selenium import webdriver
from time import sleep
from selenium.common.exceptions import *
import os
import re
from .models import Item

CHROME_DRIVER = os.path.expanduser('/usr/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument('--lang=ja-JP')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

class PayPay:
    def scraping(self, keyword, min_price, max_price, category, status, quality):

        category_dict = {"none":"", "computer":"categoryIds=2052", "books":"categoryIds=10002",
                         "music":"categoryIds=2516", "movie":"2517", "HomeAppliances":"categoryIds=2506",
                         "fashion":"categoryIds=13257", "beauty":"categoryIds=2501", "interior":"categoryIds=2506",
                         "outdoor":"categoryIds=2513", "game":"categoryIds=2511", "goods":"categoryIds=2511", "food":"categoryIds=2498",
                         "car":"categoryIds=2514"}
        status_dict = {"指定なし":"", "販売中":"&open=1", "売り切れ":"&sold=1"}
        quality_dict = {"指定なし":"", "新品未使用に近い":"&conditions=NEW%2CUSED10", "目立った傷なし":"&conditions=NEW%2CUSED10%2CUSED20", "やや傷汚れあり":"&conditions=NEW%2CUSED10%2CUSED20%2CUSED40", "傷汚れあり":"", "ジャンクのみ":"&conditions=USED60"}

        # option込でChromeを起動
        browser = webdriver.Chrome(options=options)
        # mercari：指定条件を検索したURLにアクセス
        url = 'https://paypayfleamarket.yahoo.co.jp/search/' + keyword + '?' + category_dict[category] + status_dict[status] + quality_dict[quality] + '&minPrice=' + str(min_price) + '&maxPrice=' + str(max_price)
        browser.get(url)
        sleep(3)

        # 外ループ：メルカリの次へボタンが無くなるまで。
        while True:
            no = 0
            link_list = []
            name_list = []
            price_list = []
            image_list = []

            LinkItem = browser.find_elements_by_tag_name("a")
            NameItem = browser.find_elements_by_tag_name("img")
            PriceItem = browser.find_elements_by_tag_name("p")
            ImageItem = browser.find_elements_by_tag_name("img")

            # 内ループ：ページ内のアイテム情報を取得しきるまで。
            for LI in LinkItem:
                link = str(LI.get_attribute("href"))
                if "https://paypayfleamarket.yahoo.co.jp/item/" in link:
                    link_list.append(link)

            for NI in NameItem:
                name = NI.get_attribute ("alt")
                if keyword.upper() in name.upper():
                    name_list.append(name)

            for PI in PriceItem:
                price = PI.text
                if re.match(r'\d', price):
                    price = re.sub(r"\D", "", price)
                    price_list.append(int(price))

            for IM in ImageItem:
                IM = IM.get_attribute("src")
                if IM.startswith("https"):
                    image_list.append(IM)



            for link, name, price, image in zip(link_list, name_list, price_list, image_list):
                no += 1
                if (no > 50): break
                Item.objects.bulk_create([
                    Item(item_type='P', item_category=category, keyword=keyword, item_link=link, item_name=name, item_price=price, item_status=status, item_image=image)
                ])

            if (no > 50): break
            # 「次へ」ボタンを探して、見つかればクリック
            try:
                # 自動でページ遷移すると画面読み込み時の初期処理に割り込まれてボタン押下が出来ないので、execute_scriptで対策する。
                buttonClick = browser.find_element_by_xpath("//mer-button[@data-testid='pagination-next-button']")
                browser.execute_script("arguments[0].click();", buttonClick)
                sleep(3)

            # 「次へ」ボタンが無ければループを抜ける
            except NoSuchElementException:
                break
        # 終了処理(ヘッドレスブラウザを閉じる)
        browser.quit()
