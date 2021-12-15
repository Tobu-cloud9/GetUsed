import requests
import traceback
import re
from bs4 import BeautifulSoup
from .models import Item

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
                    print(elem_b)
                    buyout = elem_b.find("span", {"class":"Product__priceValue"})
                    if buyout is None:
                        buyout_list.append(0)
                    else:
                        buyout = buyout.text
                        buyout = int(re.sub(r"\D", "", buyout))
                        buyout_list.append(buyout)

            print(buyout_list)
            return link_list, name_list, price_list, buyout_list, limit_list, image_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None

    def scraping(self, keyword, min_price, max_price, category, status, quality):

        category_dict = {"none": "", "computer": "23336/", "books": "21006/", "contents": "22152/", "HomeAppliances": "23632/",
                         "fashion": "23000/", "beauty": "6", "interior": "24198/", "outdoor": "24698/", "goods": "25464/",
                         "food": "23976/", "car": "26318/"}
        status_dict = {"指定なし":"/search/search?", "販売中":"/search/search?", "売り切れ":"/closedsearch/closedsearch?"}

        quality_dict = {"指定なし": "", "新品未使用に近い": "istatus=1%2C3", "目立った傷なし": "istatus=1%2C3%2C4",
                        "やや傷汚れあり": "&istatus=5%2C1%2C3%2C4",
                        "傷汚れあり": "&istatus=6%2C5%2C1%2C3%2C4", "ジャンクのみ": "&istatus=7"}
        num = 1
        while num < 251:
            url = "https://auctions.yahoo.co.jp"+ status_dict[status] + "p=" + keyword + "&aucminprice="+ str(min_price) + "&aucmaxprice=" + str(max_price) +  quality_dict[quality] + "&exflg=1&b=" + str(num) + "&s1=new&o1=d&mode=2"

            response = requests.get(url)
            link, name, price, buyout_price, limit, image = self.get_data_from_source(response.content)

            for link, name, price, buyout_price, limit, image in zip(link, name, price, buyout_price, limit, image):
                Item.objects.bulk_create([
                    Item(item_type='Y', item_category=category, item_status=status, keyword=keyword, item_link=link, item_name=name, item_price=price, item_buy_price=buyout_price,
                         item_limit=limit, item_image=image)
                ])
            num += 50


