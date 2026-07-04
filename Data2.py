import pandas as pd
df = pd.read_csv('IDS_CountryMetaData.csv',encoding = 'latin1')

print(df.head())
print(df.info())

df.columns = df.columns.str.lower()
print(df.columns)

print(df.isna().sum().sort_values(ascending=False))

df.drop(['vital registration complete','national accounts reference year','other groups','special notes','latest agricultural census'],axis = 1, inplace =True)

print(df.isna().sum())

print(df.columns.nunique())