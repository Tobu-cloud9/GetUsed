import requests
import traceback
import re
from bs4 import BeautifulSoup
from .models import Item, Search


class Yahoo:
    def get_data_from_source(self, src):
        soup = BeautifulSoup(src, "html.parser")
        grid = soup.find("ul", attrs={"class": "Products__items"})

        link_list = []
        name_list = []
        price_list = []
        buyout_list = []
        limit_list = []
        image_list = []

        try:
            if grid:
                elems_link = grid.find_all("div", attrs={"class": "Product__image"})
                elems_time = grid.find_all("span", attrs={"class": "Product__time"})
                elems_buyout = grid.find_all("div", attrs={"class": "Product__priceInfo"})

                for elem in elems_link:
                    link = elem.find("a").get("data-auction-id")
                    link = "https://page.auctions.yahoo.co.jp/jp/auction/" + link
                    name = elem.find("a").get("data-auction-title")
                    image = elem.find("a").get("data-auction-img")
                    price = elem.find("a").get("data-auction-price")
                    link_list.append(link)
                    name_list.append(name)
                    image_list.append(image)
                    price_list.append(int(price))

                for elem_t in elems_time:
                    limit = elem_t.text
                    limit_list.append(limit)

                for elem_b in elems_buyout:
                    elem_b.find("span", {"class": "Product__priceValue"}).decompose()
                    buyout = elem_b.find("span", {"class": "Product__priceValue"})
                    if buyout is None:
                        buyout_list.append(0)
                    else:
                        buyout = buyout.text
                        buyout = int(re.sub(r"\D", "", buyout))
                        buyout_list.append(buyout)

            print(link_list)
            return link_list, name_list, price_list, buyout_list, limit_list, image_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None

    def func_limit(self, time):
        if "日" in time:
            time = re.sub(r"\D", "", time)
            ans = int(time) * 10000
        elif "時間" in time:
            time = re.sub(r"\D", "", time)
            ans = int(time) * 100
        elif "分" in time:
            time = re.sub(r"\D", "", time)
            ans = int(time)
        else:
            ans = 0
        return ans

    def scraping(self, search, keyword, min_price, max_price, category, status, quality):

        category_dict = {"none": "", "computer": "&auccat=23336", "books": "&auccat=21006", "contents": "&auccat=22152",
                         "HomeAppliances": "&auccat=23632",
                         "fashion": "&auccat=23000", "beauty": "&auccat=6", "interior": "&auccat=24198",
                         "outdoor": "&auccat=24698", "game": "&auccat=25464", "goods": "&auccat=25464",
                         "food": "&auccat=23976", "car": "&auccat=26318"}
        status_dict = {"指定なし": "/search/search?", "販売中": "/search/search?", "売り切れ": "/closedsearch/closedsearch?"}

        quality_dict = {"指定なし": "", "新品未使用に近い": "&istatus=1%2C3", "目立った傷なし": "&istatus=1%2C3%2C4",
                        "やや傷汚れあり": "&istatus=5%2C1%2C3%2C4",
                        "傷汚れあり": "&istatus=6%2C5%2C1%2C3%2C4", "ジャンクのみ": "&istatus=7"}
        num = 1
        while num < 251:
            url = "https://auctions.yahoo.co.jp" + status_dict[status] + "p=" + keyword + "&aucminprice=" + str(
                min_price) + "&aucmaxprice=" + str(max_price) + category_dict[category] + quality_dict[
                      quality] + "&exflg=1&b=" + str(num) + "&s1=new&o1=d&mode=2"

            response = requests.get(url)
            link, name, price, buyout_price, limit, image = self.get_data_from_source(response.content)

            for link, name, price, buyout_price, limit, image in zip(link, name, price, buyout_price, limit, image):
                Item.objects.bulk_create([
                    Item(item_search=search, item_type='Y', item_category=category, item_status=status, item_link=link,
                         item_name=name, item_price=price, item_buy_price=buyout_price,
                         item_limit=self.func_limit(limit), item_image=image)
                ])
            num += 50
