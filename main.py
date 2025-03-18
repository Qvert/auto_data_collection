from datetime import date

from src.parser_cian.ParsingPage import ParsingPage
from src.parser_cian.settings import HEADERS

from src.utils.save_data_csv import save_to_csv


def main():
    scrapped_page = []
    url = 'https://krasnoyarsk.cian.ru/snyat-kvartiru/'
    parsing_page = ParsingPage(url, headers=HEADERS)
    list_dict_to_load_csv = []
    source_site = url.split("//")[1].split('/')[0]
    date_parse = date.today()
    for name, price, addr, link, desc, photo in zip(parsing_page.parse_name(),
                                                    parsing_page.parse_price(),
                                                    parsing_page.parse_address(),
                                                    parsing_page.parse_link(),
                                                    parsing_page.parse_description(),
                                                    parsing_page.parse_photo()):

        dict_to_load_csv = {
            "Name": name,
            "Price": price,
            "Address": addr,
            "Link": link,
            "Description": desc,
            "Photo": photo,
            "Date parse": date_parse,
            "Source": source_site,
        }
        list_dict_to_load_csv.append(dict_to_load_csv)
        save_to_csv(list_dict_to_load_csv, "save_data.csv")


if __name__ == '__main__':
    main()
