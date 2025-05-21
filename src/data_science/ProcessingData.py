import numpy as np

class ProcessingData:
    def __init__(self, df):
        self.df = df

    def clean_data(self):
        print("\nHandling Missing Data...")
        self.df.replace({'—': np.nan, 'N/A': np.nan, '': np.nan}, inplace=True)
        self.df.dropna(subset=["Price"], inplace=True)
        self.df.reset_index(drop=True, inplace=True)

        print(f"Cleaned Data: {len(self.df)} rows remaining.")
        print(self.df)

    def convert_columns(self):
        print("Converting Columns...")
        try:
            self.df = self.df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            self.df['Price'] = self.df['Price'].str.replace('[$,₽/мес. ]', '', regex=True).replace('', np.nan).astype(float)
            self.df['М^2'] = self.df['М^2'].str.replace('[м^2, м²]', '', regex=True).replace('', np.nan).astype(float)

        except AttributeError:
            print("Данные уже обновлены")
        finally:
            print("Data Cleaning Complete!")


    def save_to_csv_df(self):
        self.df.to_csv("src/utils_/hata.csv", index=False)

