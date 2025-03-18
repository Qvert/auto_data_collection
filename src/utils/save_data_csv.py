from typing import List
import csv


def save_to_csv(dict_data: List, name_file: str) -> None:
    with open(name_file, 'w', newline="", encoding="utf-8") as file_write:
        write_to_file = csv.writer(file_write, delimiter=";",
                                   quotechar="|", quoting=csv.QUOTE_MINIMAL)
        write_to_file.writerow(["Name", "Price", "Address", "Link", "Description", "Photo", "Date parse", "Source"])
        for element in dict_data:
            write_to_file.writerow([element["Name"], element["Price"], element["Address"],
                                    element["Link"], element["Description"], element["Photo"], element["Date parse"],
                                    element["Source"]])
