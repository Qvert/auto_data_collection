import requests
from bs4 import BeautifulSoup


class ParsingPage:
    def __init__(self, url, headers):
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
        pass

    def parse_link(self):
        pass

    def parse_phone(self):
        pass

    def parse_name(self):
        pass


