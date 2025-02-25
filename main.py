
import undetected_chromedriver as uc
from src.parser_avito.setings import options, service

def main():
    driver = uc.Chrome(options=options, service=service, headless=True, use_subprocess=False)


if __name__ == '__main__':
    main()
