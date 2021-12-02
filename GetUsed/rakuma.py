import requests
import traceback
import re
from bs4 import BeautifulSoup
from .models import Item

class Rakuma:

    def get_data_from_source(self, src):
        soup = BeautifulSoup(src, "html.parser")
        grid = soup.find("div", attrs={"class": "content"})

        link_list = []
        name_list = []
        price_list = []

        try:
            if grid:
                elems = grid.find_all("div", attrs={"class": "item"})

                for elem in elems:
                    link = elem.find("a").get("href")
                    name = elem.find("a").get("title")
                    price = elem.find("p", attrs={"class": "item-box__item-price"}).text
                    price = re.sub(r"\D", "", price)

                    link_list.append(link)
                    name_list.append(name)
                    price_list.append(int(price))

            return link_list, name_list, price_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None


    def scraping(self, keyword, min_price, max_price, category, status):

        status_dict = {"指定なし":"", "販売中":"&transaction=selling", "売り切れ":"&transaction=soldout"}
        thema = keyword

        num = 1
        while num < 251:
            url = "https://fril.jp/s?query=" + thema + "&min=" + str(min_price) + "&max=" + str(max_price)

            response = requests.get(url)
            link, name, price = self.get_data_from_source(response.content)

            i = 0
            for link_db, name_db, price_db in zip(link, name, price):
                Item.objects.bulk_create([
                    Item(item_type='R', item_category=category, item_status=status, keyword=keyword, item_link=link_db, item_name=name_db, item_price=price_db)
                ])
            num += 50