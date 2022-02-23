import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import partial
from tqdm import tqdm
import os
from cryptography.fernet import Fernet
import sys
import psycopg2
tqdm.pandas()


#####Clairty Request to get Postcodes#####
try:
    file = open(os.path.expanduser(r'~\PythonFolder\Python\LocalKeys\key.key'), 'rb')  # Open the file as wb to read bytes
except Exception as EncryptException:
    print(EncryptException)
    sys.exit(1)
else:
    key = file.read()  # The key will be type bytes
    f = Fernet(key)
    #Clarity
    EncryptPass = b"gAAAAABhXHzYeOgtABS17sxIk5hIj271nxdUAbgkVXT9nU7M58zAdUbMUabkl_7p39hUyqSbW9voGdN8Jr_t8g1wVMYuR1Hn2pRAoIccwIc3L55SG_8yDqQ="
    EncryptURL = b'gAAAAABhXVzVi8BSq2J8FvegKI_nSwrkgZKaxu9U0hDR8rwTu39MQXk-8QlI-36MU9hqdZw4xQcfzNex4o2eyNTw18RTFowFOknuMfPYUV9J1RtrQkF1nwTwc5GjU_1jYgXIHTGwpjHPH0UzP1jFesjr9s3ZDc1VOA=='
    EncryptUser = b'gAAAAABhXV3toUXcNXelIiWKE617RwKxOiSq9Cc2xeAKOJ-YkAaNP6kHHGjzJX4Z3MP6CfAQJkr0Vsv3Zq_-B8_J122s53UUag=='
    EncryptDBName = b'gAAAAABhXV37TSE6dSe461Uxrd1WHvM6vJwVFNoRfnAhryAb0aoMx3m07eiwwN3XvnrgcyPV3Anle8h5Y4SNvFi6Sp1h3bjA2g=='
    #Clarity Decrypt
    DecryptedPass= f.decrypt(EncryptPass)
    Password = bytes(DecryptedPass).decode("utf-8")
    DecryptedURL = f.decrypt(EncryptURL)
    URL = bytes(DecryptedURL).decode("utf-8")
    DecryptUser = f.decrypt(EncryptUser)
    User = bytes(DecryptUser).decode("utf-8")
    DecryptDBName = f.decrypt(EncryptDBName)
    DBName = bytes(DecryptDBName).decode("utf-8")

try:
    conn = psycopg2.connect(
        dbname=DBName,
        user=User,
        host=URL,
        password=Password,
        options='-c statement_timeout=300000'
    ) #5 min timout in ms
except Exception as ConnException:
    print(ConnException)
    sys.exit(1)
#Create a new cursor
cur = conn.cursor()

def create_pandas_table(sql_query, database = conn):
    table = pd.read_sql_query(sql_query, database)
    return table

#Utilize the create_pandas_table function to create a Pandas data frame
#Store the data as a variable
clarity_info = create_pandas_table("""\
select
	"CompanyId",
	"PostalCode"
from
	hubspot_companies hc
where
	"CompanyId" not in (
	select
		"CapsuleId"
	from
		dealerships_old
	where
		"IsActive" = 'true'
		and "CapsuleId" is not null
	group by
		1
		)
	and "FieldRegion" <> 'Germany'
	and "PostalCode" <> '' LIMIT 5      
""")

df = pd.DataFrame(clarity_info)
cur.close()
conn.close()

##### Use PostalCode to find Geolocation Data #####
geolocator = Nominatim(timeout=10, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')

geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 1, return_value_on_exception = None)

df['location'] = df['PostalCode'].progress_apply(partial(geolocator.geocode, timeout=1000, language='en',country_codes='gb'))

df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else (None, None))

df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(df['point'].values.tolist(), df.index)

df2 = df[['CompanyId', 'PostalCode', 'Latitude', 'Longitude']]

df2.set_index('CompanyId', inplace=True) #Sets index

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print(df2)
