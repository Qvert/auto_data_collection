from typing import List

import pandas as pd


def save_to_csv(list_data: List, name_file: str) -> None:
    data_frame = pd.DataFrame(list_data)
    data_frame.to_csv(name_file, index=False)
