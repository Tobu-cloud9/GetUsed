# メルカリ上で動的レンダリングされた商品情報を取得し、すべてのページから商品名、価格、タイトルを取得する。
import webbrowser

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



class Merukari:
    def scraping(self, keyword, min_price, max_price, category, status, quality):

        category_dict = {"none":"", "computer":"7", "books":"5", "music":"75", "movie":"74",
                         "HomeAppliances":"7", "fashion":"1&2", "beauty":"6", "interior":"4",
                         "outdoor":"8", "game":"76", "goods":"1328", "food":"10&1027", "car":"1318"}

        status_dict = {"指定なし":"on_sale,sold_out", "販売中":"on_sale", "売り切れ":"sold_out"}

        quality_dict = {"指定なし": "", "新品未使用に近い": "&item_condition_id=1,2", "目立った傷なし": "&item_condition_id=1,2,3", "やや傷汚れあり": "&item_condition_id=1,2,3,4",
                        "傷汚れあり": "&item_condition_id=1,2,3,4,5", "ジャンクのみ": "&item_condition_id=6"}
        # option込でChromeを起動
        browser = webdriver.Chrome(options=options)
        # mercari：指定条件を検索したURLにアクセス
        url = 'https://jp.mercari.com/search?keyword=' + keyword + '&price_min=' + str(min_price) + '&price_max=' + str(max_price) + '&category_id=' + category_dict[category] + "&status=" + status_dict[status] + quality_dict[quality]
        browser.get(url)
        sleep(3)

        # 外ループ：メルカリの次へボタンが無くなるまで。
        while True:
            no = 0
            link_list = []
            name_list = []
            price_list = []
            image_list = []
            sell_status_list = []
            LinkItems = browser.find_elements_by_tag_name("a")
            sellItems = browser.find_elements_by_tag_name("mer-item-thumbnail")


            # 内ループ：ページ内のアイテム情報を取得しきるまで。
            for LI in LinkItems:
                link = str(LI.get_attribute("href"))
                if "/item/m" in link:
                    link_list.append(link)

            for sI in sellItems:
                name = sI.get_attribute("item-name")
                price = sI.get_attribute("price")
                image = sI.get_attribute("src")
                sold_out = sI.get_attribute('sticker')
                #########未実装
                sell_status = "None"
                try:
                    if len(sold_out) > 0:
                        sell_status = "売り切れ"
                except:
                    sell_status = "販売中"
                ###################
                name_list.append(str(name))
                price_list.append(price)
                image_list.append(image)
                sell_status_list.append(sell_status)

            for link, name, price, image in zip(link_list, name_list, price_list, image_list):
                no += 1
                if (no > 50): break
                Item.objects.bulk_create([
                    Item(item_type='M', item_category=category, keyword=keyword, item_link=link, item_name=name, item_price=price, item_status=status, item_image=image)
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

