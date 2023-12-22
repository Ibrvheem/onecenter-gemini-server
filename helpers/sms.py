import os

import africastalking

class SMS:
    def __init__(self):
        SMS_USERNAME="mypal"
        SMS_API_KEY="08fc39e0dd7a60614ac4e8d2357238ac4c16748a53dc4980664bc173f05dcb08"
        # Set your app credentials
        self.username = SMS_USERNAME
        self.api_key = SMS_API_KEY
        
        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)
        
        # Get the SMS service
        self.sms = africastalking.SMS
    
    def send(self, recipient, message):
        # Set your shortCode or senderId
        # sender = os.environ.get("SMS_ID")
        try:
            # print(recipient, message, sender)
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, [recipient])
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))
    
    def send_bulk(self, recipients, message):
        # Set your shortCode or senderId
        # sender = os.environ.get("SMS_ID")
        try:
            # Thats it, hit send and we'll take care of the rest.
            response = self.sms.send(message, recipients)
            print (response)
        except Exception as e:
            print ('Encountered an error while sending: %s' % str(e))

def send_ai_message(history):
    recipients = ["+2348158962698", "+2348076196276"]
    sms = SMS()
    if len(history) > 2:
        for recipient in recipients:
            sms.send(recipient, history[-2].content[:160])