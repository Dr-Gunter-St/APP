import pandas as pd
import psycopg2
import sqlalchemy
import matplotlib.pyplot as plt


from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

# Postgres username, password, and database name
POSTGRES_ADDRESS = 'http://127.0.0.1/'
POSTGRES_PORT = '5432'
POSTGRES_USERNAME = 'postgres'
POSTGRES_DBNAME = 'city_stat'

# A long string that contains the necessary Postgres login information
postgres_str = ('postgresql://{username}:{port}/{dbname}'
                .format(username=POSTGRES_USERNAME,
                        port=POSTGRES_PORT,
                        dbname=POSTGRES_DBNAME))

# Create the connection
# engine = create_engine('postgresql://user:password@localhost:5433/testdb2')

engine = create_engine('postgresql://postgres: @localhost:5432/city_stat')

input = int(input("Enter a number(1=Highway,2=Building,3=Amenity,4=Emergency,5=historic,6=office: "))

tags = ["highway", "building", "amenity","historic", "emergency","office"]


if (tags[input-1]=="highway"):
    df = pd.read_sql_query(
        ''' select tags->'highway', sum(st_length(linestring::geography)) from ways where tags?'highway' group by tags->'highway' order by sum desc;''',
        engine)
    df2 = df.rename(columns={'?column?': 'Highway', 'sum': 'Total Lenght'})
    data = df2.groupby('Highway')
    data.size()
    data_total = (data.sum())/1000
    df2['Lenght (KM)'] = df2['Total Lenght']/1000
    my_plot = data_total.plot(kind='bar',legend=None,title="Highway Length in Krakow", figsize=(15,7))
    my_plot.set_xlabel("Highway Type")
    my_plot.set_ylabel("Length (km)")
    print(df2)
    plt.show()
else:
    df=pd.read_sql_query('''select tags->'{}', sum(st_length(linestring::geography)) from ways where tags?'{}' group by tags->'{}' order by sum desc;'''.format(tags[input-1], tags[input-1],tags[input-1]), engine)
    df2=df.rename(columns={'?column?':'{}'.format(tags[input-1]), 'sum': 'Total Lenght'})
    print(df2)


