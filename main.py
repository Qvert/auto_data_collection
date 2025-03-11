from src.parser_avito.ParsingPage import ParsingPage
from src.parser_avito.settings import HEADERS


def main():
    scrapped_page = []
    url = 'https://krasnoyarsk.cian.ru/snyat-kvartiru/'
    parsing_page = ParsingPage(url, headers=HEADERS)


if __name__ == '__main__':
    main()
