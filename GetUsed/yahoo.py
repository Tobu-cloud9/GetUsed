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
        image_list = []

        try:
            if grid:
                elems_link = grid.find_all("li", attrs={"class": "Product"})
                elems_price = grid.find_all("span", attrs={"class": "Product__priceValue u-textRed"})
                elems_buyout_price = grid.find_all("span", attrs={"class": "Product__priceValue"})
                elems_time = grid.find_all("span", attrs={"class": "Product__time"})
                elems_image = grid.find_all("img")

                for elem in elems_link:
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

                for elem_i in elems_image:
                    image = elem_i['src']
                    image_list.append(image)



            return link_list, name_list, price_list, price_buyout_list, limit_list, image_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None

    def scraping(self, keyword, min_price, max_price, category, status):

        category_dict = {"none": "", "computer": "23336/", "books": "21006/", "contents": "22152/", "HomeAppliances": "23632/",
                         "fashion": "23000/", "beauty": "6", "interior": "24198/", "outdoor": "24698/", "goods": "25464/",
                         "food": "23976/", "car": "26318/"}
        status_dict = {"指定なし":"/search/search?", "販売中":"/search/search?", "売り切れ":"/closedsearch/closedsearch?"}

        num = 1
        while num < 251:
            url = "https://auctions.yahoo.co.jp"+ status_dict[status] + "p=" + keyword + "&aucminprice="+ str(min_price) + "&aucmaxprice=" + str(max_price) + "&exflg=1&b=" + str(num) + "&s1=new&o1=d&mode=2"

            response = requests.get(url)
            link, name, price, buyout_price, limit, image = self.get_data_from_source(response.content)

            for link, name, price, buyout_price, limit, image in zip(link, name, price, buyout_price, limit, image):
                Item.objects.bulk_create([
                    Item(item_type='Y', item_category=category, item_status=status, keyword=keyword, item_link=link, item_name=name, item_price=price, item_buy_price=buyout_price ,
                         item_limit=limit, item_image=image)
                ])
            num += 50


