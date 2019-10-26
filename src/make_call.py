from twilio.rest import Client
import time

from blink_app import secrets

account_sid = secrets['twilio']['account_sid']
auth_token = secrets['twilio']['auth_token']
from_ = secrets['twilio']['phone_number']
to = secrets['user']['phone_number']
client = Client(account_sid, auth_token)

now = time.time()

while (time.time() < now + 40):
    if (time.time() == (now + 5)):
        call = client.calls.create(
                                url='https://handler.twilio.com/twiml/EHc9c6b7b68c7c960d3c68394101b34d82',
                                to=to,
                                from_=from_
                            )
        print(call.sid)

    if (time.time() == (now + 20)):
        call = client.calls.create(
                                url='https://handler.twilio.com/twiml/EHea73a00f56dfc95bda440cc714a22326',
                                to=to,
                                from_=from_
                            )
        print(call.sid)
