from datetime import date

from src.parser_cian.ParsingPage import ParsingPage
from src.parser_cian.settings import HEADERS_PARSER

from src.utils_.save_data_csv import save_to_csv


def main():
    pages = int(input("Введите количество страниц, с которых нужно собрать данные: "))
    assert pages > 1
    list_dict_to_load_csv = []
    for i in range(1, pages):
        if i == 1:
            url_pages = 'https://krasnoyarsk.cian.ru/snyat-kvartiru/'
        else:
            url_pages = (f'https://krasnoyarsk.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p={i}&'
                         'region=4827&type=4')
        parsing_page = ParsingPage(url_pages, headers=HEADERS_PARSER)

        source_site = url_pages.split("//")[1].split('/')[0]
        date_parse = date.today()

        for name, price, address, link, desc, photo in zip(parsing_page.parse_name(),
                                                           parsing_page.parse_price(),
                                                           parsing_page.parse_address(),
                                                           parsing_page.parse_link(),
                                                           parsing_page.parse_description(),
                                                           parsing_page.parse_photo(),
                                                           ):
            list_dict_to_load_csv.append({
                "Name": name,
                "Price": price,
                "Address": address,
                "Link": link,
                "Description": desc,
                "Photo": photo,
                "Date parse": date_parse,
                "Source": source_site,
            })
    save_to_csv(list_dict_to_load_csv, "src/utils_/hata.csv")


if __name__ == '__main__':
    main()
