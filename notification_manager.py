import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

account_sid = os.environ.get("TWILLIO_ACCOUNT_SID")
auth_token = os.environ.get("TWILLIO_AUTH_TOKEN")
from_ = os.environ.get("TWILLIO_FROM_NUMBER")
to = os.environ.get("TWILLIO_TO_NUMBER")


# Class "NotificationManager"
class NotificationManager:
    """
    Class "NotificationManager"
    Instance : client -> Object Client from twilio
    Method : send_text
    """
    
    def __init__(self):
        self.client = Client(account_sid, auth_token)
    
    # Method to send text in your mobile
    def send_text(self, my_text):
        """
        Method to send text in your mobile
        accept:
        my_text -> str
        """
        message = self.client.messages.create(body=my_text, from_=from_, to=to)
        print(message.sid)
