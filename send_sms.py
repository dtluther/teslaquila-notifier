from dotenv import dotenv_values
from twilio.rest import Client

config = dotenv_values("twilio.env")

account_sid = config['TWILIO_ACCOUNT_SID']
auth_token = config['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_=config['FROM_NUMBER'],
                     to=config['TO_NUMBER']
                 )

print(message.sid)
