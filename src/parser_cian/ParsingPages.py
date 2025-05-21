import time
from datetime import date
import pandas as pd
from tqdm import tqdm
from src.parser_cian.ParsingPage import ParsingPage
from src.parser_cian.settings import HEADERS_PARSER, DATA_PATH, HEADERS
from src.utils_.save_data_csv import save_to_csv


class ParsingPages:
    def __init__(self, base_urls, max_pages=1, delay=1.0):
        self.base_urls = base_urls
        self.max_pages = max(max_pages, 1)
        self.delay = max(delay, 0.5)
        self.data = []
        self.failed_pages = []

    def parse_single_page(self, url):
        """Парсинг одной страницы"""
        try:
            parser = ParsingPage(url, HEADERS)
            source_site = url.split("//")[1].split('/')[0]

            results = []
            for name, price, address, link, desc, photo, square in zip(
                    parser.parse_name(),
                    parser.parse_price(),
                    parser.parse_address(),
                    parser.parse_link(),
                    parser.parse_description(),
                    parser.parse_photo(),
                    parser.parse_square()
            ):
                results.append({
                    "Name": name,
                    "Price": price,
                    "Address": address,
                    "Link": link,
                    "Description": desc,
                    "Photo": photo,
                    "Square (м²)": square,
                    "Date parse": date.today(),
                    "Source": source_site
                })
            return results

        except Exception as e:
            print(f"Ошибка при парсинге {url}: {str(e)}")
            self.failed_pages.append(url)
            return []

    def parse_all_pages(self):
        """Парсинг всех страниц с обработкой прогресса"""
        self.data = []
        self.failed_pages = []

        for page_num in tqdm(range(1, self.max_pages + 1), desc="Парсинг страниц"):
            try:
                page_url = f"{self.base_urls[0]}{page_num}{self.base_urls[1]}"

                # Парсим страницу
                page_data = self.parse_single_page(page_url)
                self.data.extend(page_data)

                # Задержка между запросами
                time.sleep(self.delay)

            except Exception as e:
                print(f"Критическая ошибка на странице {page_num}: {str(e)}")
                self.failed_pages.append(page_num)
        self.save_to_csv_parse()
        return self.data

    def save_to_csv_parse(self, filename=DATA_PATH):
        if not self.data:
            print("Нет данных для сохранения!")
            return False

        df = pd.DataFrame(self.data)
        save_to_csv(df, filename)
        return True
