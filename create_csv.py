import pandas as pd

df = pd.read_csv('https://github.com/OxCGRT/USA-covid-policy/raw/master/data/OxCGRT_US_latest.csv', dtype={
                 'E4_Notes': str, 'H6_Facial Coverings': float}, usecols=["CountryCode", "RegionName", "RegionCode", "Date", 'ConfirmedCases', 'H6_Facial Coverings'])

df = df[df["CountryCode"] == 'USA']
df = df.dropna(subset=["RegionName"])
df = df.sort_values("Date")
df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
df['H6_Facial Coverings'] = pd.to_numeric(df['H6_Facial Coverings'])
df['RegionCode'] = df['RegionCode'].str[-2:]

df.to_csv('assets/usa.csv')
