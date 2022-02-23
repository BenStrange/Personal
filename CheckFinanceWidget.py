import requests
from bs4 import BeautifulSoup
import pandas as pd
import xmltodict
import os

url = "https://www.bigmotoringworld.co.uk/sitemap.xml"
res = requests.get(url)
raw = xmltodict.parse(res.text)

data = [r["loc"] for r in raw["urlset"]["url"]]
df = pd.DataFrame(data, columns=["Url"])
df.set_index(["Url"], inplace=False)
string = df[df["Url"].str.contains("/used/cars/audi")]
string1 = string[~string["Url"].str.contains("page")]
pd.set_option('display.max_colwidth', None)

final = string1.Url.to_string(index=False)
final.strip()


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}

page = requests.get("https://www.bigmotoringworld.co.uk/used/cars/hyundai/tucson/gdi-se-nav-blue-drive-98679", headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
search = soup.find_all(class_='finance-widget')
searchstr = str(search)


while True:
    if 'newvehicle' and 'ivendi' in searchstr:
        print("Online")
        break
    else:
        time.sleep(1)
        print("Offline")
        continue