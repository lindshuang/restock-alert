import sys
import time
import config
from datetime import datetime
from pytz import timezone

import requests
from bs4 import BeautifulSoup
from twilio.rest import Client

def setup_twilio_client():
    account_sid = config.account_sid
    auth_token = config.auth_token
    return Client(account_sid, auth_token)

def send_notif():
    twilio_client = setup_twilio_client()
    twilio_client.messages.create(
        body="Your lululemon product is available for purchase.",
        from_= config.caller,
        to=config.reciever
    )

def get_url():
    url = config.product_url
    page = requests.get(url)
    # print(page.status_code)
    return page.content

def check_item(page_html):
    count = 0;
    soup = BeautifulSoup(page_html, 'html.parser')
    oos = soup.findAll("span", {"class": "sizeTile-3p7Pr"})
    for size in oos:
        # print (size.text)
        if size.text == '6':
            count += 1
    return count == 1

def check_inventory():
    html_from_page = get_url()
    cst = timezone('US/Central')
    curr_time = datetime.now(cst)
    print_curr_time = curr_time.strftime('%H:%M:%S, %Y-%m-%d')
    if check_item(html_from_page):
        print('sending notification to user at' + print_curr_time)
        send_notif()
        sys.exit(1)  #terminate after message sent
    else:
        print("Still out of stock at " + print_curr_time)

while True:
    check_inventory()
    time.sleep(240)  #check every 4 minutes

