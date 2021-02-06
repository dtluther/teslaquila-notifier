from dotenv import dotenv_values
from twilio.rest import Client
import requests
from time import sleep

config = dotenv_values("twilio.env")
account_sid = config['TWILIO_ACCOUNT_SID']
auth_token = config['TWILIO_AUTH_TOKEN']
from_number = config['FROM_NUMBER']
to_number = config['TO_NUMBER']

client = Client(account_sid, auth_token)

site1 = 'https://teslatequila.tesla.com/'
site2 = 'https://shop.tesla.com/product/tesla-tequila?sku=1617866-00-A'

def send_alert_message(src_number, dest_number, body):
    message = client.messages \
                    .create(
                         body=body,
                         from_=src_number,
                         to=dest_number
                     )
    print(message.sid)

seconds_in_day = 86400
sleep_duration = 2
counts_in_day = seconds_in_day // sleep_duration
counter = counts_in_day - 2
while True:
    print(counter)
    try:
        resp1 = requests.get(site1)
        resp2 = requests.get(site2)
    except requests.ConnectionError as e:
        print("Couldn't connect to one of the sites, trying again")
        sleep(3)

    if resp1.text and "out of stock" not in resp1.text.lower() or resp2.text and "out of stock" not in resp2.text.lower():
        print("IN STOCK")
        send_alert_message(from_number, to_number, f"Teslaquila IN STOCK! Get it now at {site1} or {site2}!")
    else:
        print("NO LUCK YET")
    if counter >= counts_in_day:
        send_alert_message(from_number, to_number, f"Daily update text. Teslaquila notifier is working. {site1}")
        counter = 0
    
    sleep(sleep_duration)
    counter += 1




