from datetime import date

from src.parser_cian.ParsingPage import ParsingPage
from src.parser_cian.settings import HEADERS_PARSER
from src.utils_.save_data_csv import save_to_csv


class ParsingPages:
    def __init__(self, url, pages=1):
        self.pages = pages
        self.url = url
        self.list_parse_pages = []

    def parsing_pages(self):
        assert self.pages >= 1
        date_parse = date.today()

        for i in range(1, self.pages + 1):
            url_page = self.url[0] + f'{i}' + self.url[1]
            parsing_page = ParsingPage(url_page, HEADERS_PARSER)
            source_site = url_page.split("//")[1].split('/')[0]

            for name, price, address, link, desc, photo, square in zip(parsing_page.parse_name(),
                                                                       parsing_page.parse_price(),
                                                                       parsing_page.parse_address(),
                                                                       parsing_page.parse_link(),
                                                                       parsing_page.parse_description(),
                                                                       parsing_page.parse_photo(),
                                                                       parsing_page.parse_square()):
                self.list_parse_pages.append({
                    "Name": name,
                    "Price": price,
                    "Address": address,
                    "Link": link,
                    "Description": desc,
                    "Photo": photo,
                    "Date parse": date_parse,
                    "Source": source_site,
                    "М^2": square,
                })
        self.save_to_file()


    def save_to_file(self):
        save_to_csv(self.list_parse_pages, "src/utils_/hata.csv")

