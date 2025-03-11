import requests
import undetected_chromedriver as uc
import random

from src.parser_avito.ParsingPage import ParsingPage
from src.parser_avito.settings import HEADERS


def main():
    parsing_page = ParsingPage("https://krasnoyarsk.cian.ru/snyat-kvartiru/",
                               headers=HEADERS)


if __name__ == '__main__':
    main()
