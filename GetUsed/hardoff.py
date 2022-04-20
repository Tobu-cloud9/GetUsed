import requests
import traceback
import re
from bs4 import BeautifulSoup
from .models import Item, Search


class HardOff:
    def get_data_from_source(self, src):
        soup = BeautifulSoup(src, "html.parser")
        link_list = []
        name_list = []
        price_list = []
        image_list = []

        grid = soup.find_all("div", attrs={"class": "itemcolmn_item"})

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

    def scraping(self, search, keyword, min_price, max_price, category, status, quality):

        status_dict = {"指定なし": "", "販売中": "&exso=1", "売り切れ": ""}
        quality_dict = {"指定なし": "", "新品未使用に近い": "&rank=1&rank=2", "目立った傷なし": "&rank=1&rank=2&rank=3",
                        "やや傷汚れあり": "&rank=1&rank=2&rank=3&rank=4", "傷汚れあり": "&rank=1&rank=2&rank=3&rank=4&rank=5",
                        "ジャンクのみ": "&rank=6"}

        num = 1
        while num < 251:
            url = "https://netmall.hardoff  .co.jp/search/?" + "q=" + keyword + "&min=" + str(
                min_price) + "&max=" + str(max_price) + quality_dict[quality]

            response = requests.get(url)
            link, name, price, image = self.get_data_from_source(response.content)

            for link, name, price, image in zip(link, name, price, image):
                Item.objects.bulk_create([
                    Item(item_search=search, item_type='H', item_category=category, item_status=status, item_link=link,
                         item_name=name, item_price=price, item_image=image)
                ])
            num += 50
