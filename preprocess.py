import pandas as pd


def preprocess_data(df):
    df = df[df["CountryCode"] == 'USA']

    df = df.dropna(subset=["RegionName"])
    df = df.sort_values("Date")
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df['RegionCode'] = df['RegionCode'].str[-2:]

    return df
