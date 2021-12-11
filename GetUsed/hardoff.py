import requests
import traceback
import re
from bs4 import BeautifulSoup
from .models import Item

class HardOff:
    def get_data_from_source(self, src):
        soup = BeautifulSoup(src, "html.parser")
        link_list = []
        name_list = []
        price_list = []
        image_list = []

        grid = soup.find_all("div", attrs={"class":"itemcolmn_item"})

        try:
            for elem in grid:
                link_list.append(elem.find("a").get("href"))
                name_list.append(elem.find("img").get("alt"))
                price = elem.find("span", attrs={"class": "font-en item-price-en"}).text
                price = re.sub(r"\D", "", price)
                price_list.append(int(price))
                image_list.append(elem.find("img").get("src"))

            return link_list, name_list, price_list, image_list

        except Exception as e:

            print("Exception\n" + traceback.format_exc())

            return None

    def scraping(self, keyword, min_price, max_price, category, status):

        status_dict = {"指定なし":"", "販売中":"&exso=1", "売り切れ":""}

        num = 1
        while num < 251:
            url = "https://netmall.hardoff.co.jp/search/?" + "q=" + keyword + "&min="+ str(min_price) + "&max=" + str(max_price)

            response = requests.get(url)
            link, name, price, image = self.get_data_from_source(response.content)

            for link, name, price, image in zip(link, name, price, image):
                Item.objects.bulk_create([
                    Item(item_type='H', item_category=category, item_status=status, keyword=keyword, item_link=link, item_name=name, item_price=price, item_image=image)
                ])
            num += 50

