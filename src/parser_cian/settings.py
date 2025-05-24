import random
from fake_useragent import UserAgent

ua = UserAgent()
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
]
HEADERS = {"User-Agent": random.choice(USER_AGENTS)}
HEADERS_PARSER = {"User-Agent": ua.random}
URL_PAGE_1 = f'https://krasnoyarsk.cian.ru/cat.php?deal_type=rent&engine_version=2&offer_type=flat&p='
URL_PAGE_2 = f'&region=4827&type=4'

API_KEY = '0585a3a6-e7df-499d-83ea-573e16a5dd16'
PAGES_PARSE = 2
DATA_PATH = "src/utils_/hata.csv"
