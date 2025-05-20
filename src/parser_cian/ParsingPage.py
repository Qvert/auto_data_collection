import time

import requests
import random
from bs4 import BeautifulSoup

from src.parser_cian.settings import HEADERS_PARSER


class ParsingPage:
    def __init__(self, url, headers=None):
        self.url = url
        self.headers = headers
        self.page = requests.get(self.url, headers=self.headers)
        self.parser = BeautifulSoup(self.page.content, 'lxml')

    def parse_price(self):
        list_prices = []
        try:
            block = self.parser.find_all("div", class_="_93444fe79c--container--aWzpE")
            for elements in block:
                price = elements.text
                if price.endswith("мес."):
                    list_prices.append(price)
            return list_prices
        except Exception as _err:
            print(_err)
            return "N/A"

    def parse_address(self):
        list_address = []
        try:
            container_div_address = self.parser.find_all("div", class_="_93444fe79c--labels--L8WyJ")
            for elements in container_div_address:
                list_address.append(elements.text)
            return list_address
        except:
            return "N/A"

    def parse_photo(self):
        list_photo = []
        container_a_link_photo = self.parser.find_all("a", class_="_93444fe79c--link--VtWj6")
        for link in container_a_link_photo:
            time.sleep(random.uniform(1, 6))
            open_link = requests.get(link.get("href"), headers=HEADERS_PARSER)
            print(open_link.status_code)
            parser_photo = BeautifulSoup(open_link.content, 'lxml')
            all_photo = parser_photo.find_all("img", class_='a10a3f92e9--container--KIwW4')
            list_all_to_one_property = []
            for photo in all_photo:
                list_all_to_one_property.append(photo.get("src"))
            list_photo.append(list_all_to_one_property)
        return list_photo

    def parse_link(self):
        list_link = []
        try:
            container_a_link = self.parser.find_all("a", class_="_93444fe79c--link--VtWj6")
            for link in container_a_link:
                list_link.append(link.get("href"))
            return list_link
        except:
            return "N/A"

    def parse_description(self):
        list_description = []
        try:
            container_div_desc = self.parser.find_all("div",
                                                      class_="_93444fe79c--description--SqTNp")
            for elements in container_div_desc:
                list_description.append(elements.text.strip())
            return list_description
        except:
            return "N/A"

    def parse_name(self):
        list_name = []
        try:
            container_div_name = self.parser.find_all("span", class_="_93444fe79c--color_text"
                                                                     "-main-default--HgSpe"
                                                                     " _93444fe79c--lineHeight_28px--KFXmc"
                                                                     " _93444fe79c--fontWeight_bold--BbhnX "
                                                                     "_93444fe79c--fontSize_22px--sFuaL "
                                                                     "_93444fe79c--display_block--KYb25"
                                                                     " _93444fe79c--text--b2YS3 _93444fe79c"
                                                                     "--text_letterSpacing__normal--yhcXb")

            for elements in container_div_name:
                list_name.append(elements.text)
            return list_name
        except:
            return ["N/A"]

    def parse_square(self):
        list_square = []
        try:
            container_span_square = self.parser.find_all("a", class_="_93444fe79c--link--VtWj6")
            for elements in container_span_square:
                if elements.isdigit():
                    list_square.append(elements.text.split(", ")[1])
            print(list_square)
            return list_square
        except:
            return ["N/A"]


