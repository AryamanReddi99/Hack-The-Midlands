from twilio.rest import Client
import time

from blink_app import secrets, config

account_sid = secrets['twilio']['account_sid']
auth_token = secrets['twilio']['auth_token']
from_ = secrets['twilio']['phone_number']
to = config['user']['phone_number']
client = Client(account_sid, auth_token)
x = 0

while (x < 20):
    if (x == 1):
        print('First threshold reached')
        call = client.calls.create(
                                url='https://handler.twilio.com/twiml/EHf78588c67173c8830e80c1845f1ffe87',
                                to=to,
                                from_=from_
                            )

    if (x == 10):
        print('Second threshold reached')
        call = client.calls.create(
                                url='https://handler.twilio.com/twiml/EH7513cf20a7590d433e34dcc02bfa8788',
                                to=to,
                                from_=from_
                            )
    x += 1
    time.sleep(2)
