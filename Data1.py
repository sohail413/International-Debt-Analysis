import pandas as pd

df = pd.read_csv('IDS_ALLCountries_Data.csv',encoding='latin1')
print(df.info())

print(df.head())

df.drop(['2025','2026','2027','2028','2029','2030','2031','2032'],axis =1,inplace=True)

print(df.nunique)
print(df.value_counts())

print(df.isna().sum())
print(df.duplicated().sum())

df = df.drop_duplicates()
print(df.duplicated().sum())

# analysing numerical columns
print(df.describe())

cols = ['2000','2001','2002','2003','2004','2005','2006','2007',
        '2008','2009','2010','2011','2012','2013','2014','2015',
        '2016','2017','2018','2019','2020','2021','2022','2023','2024']

df[cols]=df[cols].fillna(0,axis=0)

dr_cols = ['Country Name','Country Code','Counterpart-Area Name','Counterpart-Area Code','Series Name','Series Code']

df=df.dropna(subset=dr_cols,how ='all')



id_columns = [
    'Country Name', 'Country Code', 'Counterpart-Area Name', 
    'Counterpart-Area Code', 'Series Name', 'Series Code'
] 

df = pd.melt(
    df,
    id_vars=id_columns,
    var_name='year',
    value_name='value'

)
print(df.head())

df.columns = df.columns.str.lower()

print(df.info())

df['year'] = df['year'].astype(int)

print(df.info())
print(df.head())

from sqlalchemy import create_engine



DB_USER     = "postgres"        # your PostgreSQL username
DB_PASSWORD = "sohail4"   # your PostgreSQL password
DB_HOST     = "localhost"       # or your server IP
DB_PORT     = "5432"            # default PostgreSQL port
DB_NAME     = "International Debt Analysis"

connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_string)
print("connected to sql")

df.to_sql(
    name='debt',          
    con=engine,
    if_exists='replace',    
    index=False,            
    chunksize=5000        
)

df1 = pd.read_csv('IDS_CountryMetaData.csv')

print(df1.info())





