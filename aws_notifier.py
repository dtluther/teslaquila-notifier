import boto3
from twilio.rest import Client
import requests
from time import sleep

ssm = boto3.client('ssm', region_name='us-west-1')

def decrypted_param(name):
    param = ssm.get_parameter(Name=name, WithDecryption=True)
    value = param['Parameter']['Value']
    return value

account_sid = decrypted_param('/twilio/TWILIO_ACCOUNT_SID')
auth_token = decrypted_param('/twilio/TWILIO_AUTH_TOKEN')
from_number = decrypted_param('/twilio/FROM_NUMBER')
to_number = decrypted_param('/twilio/TO_NUMBER')

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
sleep_duration = 10
counts_in_day = seconds_in_day // sleep_duration
counter = counts_in_day - 3
allowed_on_site1 = False
allowed_on_site2 = False

while True:
    if counter >= counts_in_day:
        send_alert_message(from_number, to_number, "Daily update text. Teslaquila notifier is working.")
        counter = 0
        # reset trying after a day and see if it's valid again
        allowed_on_site1 = True
        allowed_on_site2 = True

    print(counter)
    print(f"Can access site1: {site1}" if allowed_on_site1 else f"Denied access on site1: {site1}")
    print(f"Can access site2: {site2}" if allowed_on_site2 else f"Denied access on site2: {site2}")
    resp1, resp2 = None, None # clear the responses
    try:
        if allowed_on_site1:
            resp1 = requests.get(site1) # a 4XX response is falsey
        if allowed_on_site2:
            resp2 = requests.get(site2)
    except requests.ConnectionError as e:
        print("Couldn't connect to one of the sites, trying again")
        sleep(sleep_duration)

    # can't just check for presence because a 4XX response is falsey
    if type(resp1) is requests.models.Response: # we'll have a response if we were allowed_on_siteX is True
        if resp1.status_code == 403:
            print('DENIED')
            allowed_on_site1 = False
            send_alert_message(from_number, to_number, f"Denied from site1: {site1}")
        elif "access denied" not in resp1.text.lower() and "out of stock" not in resp1.text.lower():
            print(f"IN STOCK at {site1}")
            send_alert_message(from_number, to_number, f"Teslaquila IN STOCK! Get it now at {site1}!")
    if type(resp2) is requests.models.Response:
        if resp2.status_code == 403:
            print('DENIED')
            allowed_on_site2 = False
            send_alert_message(from_number, to_number, f"Denied from site2: {site2}")
        elif "access denied" not in resp2.text.lower() and "out of stock" not in resp2.text.lower():
            print(f"IN STOCK at {site2}")
            send_alert_message(from_number, to_number, f"Teslaquila IN STOCK! Get it now at {site2}!")
    else:
        print("NO LUCK YET")
    sleep(sleep_duration)
    counter += 1
