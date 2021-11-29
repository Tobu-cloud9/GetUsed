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
        price_buyout_list = []
        limit_list = []

        try:
            if grid:
                elems = grid.find_all("li", attrs={"class": "Product"})
                elems_price = grid.find_all("span", attrs={"class": "Product__priceValue u-textRed"})
                elems_buyout_price = grid.find_all("span", attrs={"class": "Product__priceValue"})
                elems_time = grid.find_all("span", attrs={"class": "Product__time"})

                for elem in elems:
                    link = elem.find("a").get("data-auction-id")
                    link = "https://page.auctions.yahoo.co.jp/jp/auction/" + link
                    name = elem.find("a").get("data-auction-title")
                    link_list.append(link)
                    name_list.append(name)

                for elem_p in elems_price:
                    price = elem_p.text
                    price = re.sub(r'\D', "", price)
                    price_list.append(price)

                for elem_b in elems_buyout_price:
                    buyout_price = elem_b.text
                    buyout_price = re.sub(r'\D', "", buyout_price)
                    buyout_price = int(buyout_price)
                    price_buyout_list.append(buyout_price)

                for elem_t in elems_time:
                    limit = elem_t.text
                    limit_list.append(limit)
                    print(limit)

            return link_list, name_list, price_list, price_buyout_list, limit_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None

    def scraping(self, keyword, min_price, max_price, category, status):

        status_dict = {"指定なし":"/search/search?", "販売中":"/search/search?", "売り切れ":"/closedsearch/closedsearch?"}
        thema = keyword


        num = 1
        while num < 251:
            url = "https://auctions.yahoo.co.jp"+ status_dict[status] + "p=" + thema + "&aucminprice="+ str(min_price) + "&aucmaxprice=" + str(max_price) + "&exflg=1&b=" + str(num) + "&n=50&s1=new&o1=d"

            response = requests.get(url)
            link, name, price, buyout_price, limit = self.get_data_from_source(response.content)

            i = 0
            for link_db, name_db, price_db, bp_db, limit_db in zip(link, name, price, buyout_price, limit):
                Item.objects.bulk_create([
                    Item(item_type='Y', item_category=category, item_status=status, keyword=keyword, item_link=link_db, item_name=name_db, item_price=price_db, item_buy_price=bp_db,
                         item_limit=limit_db)
                ])
            num += 50


