import requests
from bs4 import BeautifulSoup


class ParsingPage:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.page = requests.get(self.url, headers=self.headers)
        self.parser = BeautifulSoup(self.page.content, 'lxml')

    def parse_price(self):
        try:
            return self.parser.find("div", class_="_93444fe79c--container--aWzpE").text
        except:
            return "N/A"

    def parse_address(self):
        pass

    def parse_photo(self):
        pass

    def parse_link(self):
        pass

    def parse_phone(self):
        pass

    def parse_name(self):
        pass


