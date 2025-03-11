import requests


class ParsingPage:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers
        self.page = requests.get(self.url, headers=self.headers)




