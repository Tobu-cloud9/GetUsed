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
        image_list = []

        try:
            if grid:
                elems = grid.find_all("div", attrs={"class": "item"})

                for elem in elems:
                    link = elem.find("a").get("href")
                    name = elem.find("a").get("title")
                    price = elem.find("p", attrs={"class": "item-box__item-price"}).text
                    price = re.sub(r"\D", "", price)
                    image = elem.find("img").get("src")

                    link_list.append(link)
                    name_list.append(name)
                    price_list.append(int(price))
                    image_list.append(image)

            return link_list, name_list, price_list, image_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None


    def scraping(self, keyword, min_price, max_price, category, status):

        category_dict = {"none":"", "computer":"&category_id=676", "books":"&category_id=733", "music":"&category_id=762",
                         "movie":"&category_id=752","HomeAppliances":"&category_id=10006", "fashion":"&category_id=10001",
                         "beauty":"&category_id=10004", "interior":"&category_id=10009","outdoor":"&category_id=10014",
                         "game":"&category_id=786", "goods":"&category_id=10003", "food":"&category_id=10012", "car":"&category_id=10011"}
        status_dict = {"指定なし":"", "販売中":"&transaction=selling", "売り切れ":"&transaction=soldout"}
        thema = keyword

        num = 1
        while num < 251:
            url = "https://fril.jp/s?query=" + thema + category_dict[category] + "&min=" + str(min_price) + "&max=" + str(max_price) + status_dict[status]

            response = requests.get(url)
            link, name, price, image = self.get_data_from_source(response.content)

            i = 0
            for link_db, name_db, price_db, image_db in zip(link, name, price, image):
                Item.objects.bulk_create([
                    Item(item_type='R', item_category=category, item_status=status, keyword=keyword, item_link=link_db, item_name=name_db, item_price=price_db, item_image=image_db)
                ])
            num += 50