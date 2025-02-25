from pandas import options
from selenium import webdriver


class ParsingPage:
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver


