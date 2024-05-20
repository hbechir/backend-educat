from dotenv import load_dotenv
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
load_dotenv()
import os

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')


def send_gift_code(phone_number, code,first_name,provider):
    paragraph = f'Congrats {first_name}!, Your Gift is here... \nuse this code: {code} to redeem your gift at the nearest {provider} store'
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=paragraph,
        from_=TWILIO_NUMBER,  
        # to=phone_number
        # For testing purposes and because of twilio trial account, we will use our own number
        to='+21694950169' # 👈🏽👈🏽👈🏽👈🏽 Bechir's number
    )

    return message.sid
