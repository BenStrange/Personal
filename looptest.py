import os
import smtplib
import time
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
from bs4 import BeautifulSoup


url = 'https://www.very.co.uk/ghd-platinum-amp-helios-limited-edition-hair-straightener-amp-hair-dryer-in-warm-pewter/1600632697.prd'
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
page = requests.get(url, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')
TITLE = soup.find("meta", property="og:title")
AVAILABILITY = soup.find("meta", property="product:availability")

TITLEFINAL = TITLE["content"]
AVAILABILITYFINAL = AVAILABILITY["content"]

def send_mail():
    username = 'strang3fpv@gmail.com'
    password = 'Delta1345'
    send_from = 'stockinfo@stock.com'
    send_to = 'ben__strange@hotmail.com'
    Cc = ''
    msg = MIMEMultipart()
    messagebody = f"""\
    {TITLEFINAL} is Available
    """
    msg['From'] = send_from
    msg['To'] = send_to
    msg['Cc'] = Cc
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = (f'{TITLEFINAL} is in Stock')
    msg.attach(MIMEText(messagebody, 'html'))
    server = smtplib.SMTP('smtp.gmail.com')
    port = '587'
    smtp = smtplib.SMTP('smtp.gmail.com')
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    smtp.sendmail(send_from, send_to.split(',') + msg['Cc'].split(','), msg.as_string())
    smtp.quit()

while True:
    if 'Out of stock' in AVAILABILITYFINAL:
        now = datetime.datetime.now()
        timestamp = str(now.strftime("%H:%M:%S"))
        print(f"{timestamp} Is out of Stock.")
        time.sleep(5)
        continue
    else:
        now = datetime.datetime.now()
        timestamp = str(now.strftime("%H:%M:%S"))
        print(f"{timestamp} Is in Stock.")
        send_mail()
        break