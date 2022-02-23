import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from functools import partial
from tqdm import tqdm
import os
import datetime


tqdm.pandas()
df = pd.read_csv('PythonPostcodeTest.csv')

geolocator = Nominatim(timeout=10, user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (HTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36')

geocode = RateLimiter(geolocator.geocode, min_delay_seconds = 1, return_value_on_exception = None)

df['location'] = df['PostalCode'].progress_apply(partial(geolocator.geocode, timeout=1000, language='en',country_codes='gb'))

df['point'] = df['location'].apply(lambda loc: tuple(loc.point) if loc else (None, None))

df[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(df['point'].values.tolist(), df.index)

df2 = df[['CompanyId', 'PostalCode', 'Latitude', 'Longitude']]

df2.set_index('CompanyId', inplace=True) #starts index with Name



#Data & Time in Hour & Minute with out colons- "%d%m%Y_%H-%M"
now = datetime.datetime.now()
timestamp = str(now.strftime("%d.%m.%Y"))


##Creates a folder in documents & inserts the file
a = os.path.expanduser(r'~')
b = 'Documents'
c = 'PythonOutput'
d = r'PostCodeLookup' + timestamp + '.xlsx'
folderlocation = os.path.join(a + os.sep, b, c, d)

with pd.ExcelWriter(folderlocation, engine='xlsxwriter') as writer:
    df2.to_excel(writer, sheet_name='sheet1')
