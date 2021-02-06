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
# using // 2 because we are sleeping at the end of this
counter = seconds_in_day // 2 - 2
while True:
    print(counter)
    try:
        resp1 = requests.get(site1)
        resp2 = requests.get(site2)
    except requests.ConnectionError as e:
        print("Couldn't connect to one of the sites, trying again")
        sleep(3)

    if "out of stock" not in resp1.text.lower() or  "out of stock" not in resp2.text.lower():
        print("IN STOCK")
        send_alert_message(from_number, to_number, f"Teslaquila IN STOCK! Get it now at {site1} or {site2}!")
    else:
        print("NO LUCK YET")
    if counter >= seconds_in_day // 2:
        send_alert_message(from_number, to_number, f"Daily update text. Teslaquila notifier is working. {site1}")
        counter = 0
    
    sleep(2)
    counter += 1




