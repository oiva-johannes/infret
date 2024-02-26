import pandas as pd


def read_data(file: str = 'dynamic_datasets/articles_excel.xlsx') -> pd.DataFrame:

    df_ex = pd.read_excel(file)
    return df_ex


def write_data(df, file: str = 'dynamic_datasets/articles_excel.xlsx'):

    df.to_excel(file, index=False)