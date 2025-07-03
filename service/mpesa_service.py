# Create M-Pesa service integration
mpesa_service_content = """
import requests
import base64
import json
from datetime import datetime
from config import Config

class MpesaService:
    def __init__(self):
        self.consumer_key = Config.MPESA_CONSUMER_KEY
        self.consumer_secret = Config.MPESA_CONSUMER_SECRET
        self.shortcode = Config.MPESA_SHORTCODE
        self.passkey = Config.MPESA_PASSKEY
        self.auth_url = Config.MPESA_AUTH_URL
        self.b2c_url = Config.MPESA_B2C_URL
        self.stk_push_url = Config.MPESA_STK_PUSH_URL
        self.query_url = Config.MPESA_QUERY_URL
        self.access_token = None
    
    def get_access_token(self):
        \"\"\"Get OAuth access token from M-Pesa API\"\"\"
        try:
            # Create basic auth header
            auth_string = f"{self.consumer_key}:{self.consumer_secret}"
            auth_bytes = auth_string.encode('ascii')
            auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(self.auth_url, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            self.access_token = result['access_token']
            return self.access_token
            
        except Exception as e:
            print(f"Error getting access token: {str(e)}")
            return None
    
    def generate_password(self):
        \"\"\"Generate password for STK push\"\"\"
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_string = f"{self.shortcode}{self.passkey}{timestamp}"
        password_bytes = password_string.encode('ascii')
        password_b64 = base64.b64encode(password_bytes).decode('ascii')
        return password_b64, timestamp
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc, callback_url):
        \"\"\"Initiate STK push payment\"\"\"
        if not self.access_token:
            self.get_access_token()
        
        if not self.access_token:
            return {"error": "Failed to get access token"}
        
        try:
            password, timestamp = self.generate_password()
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.shortcode,
                "PhoneNumber": phone_number,
                "CallBackURL": callback_url,
                "AccountReference": account_reference,
                "TransactionDesc": transaction_desc
            }
            
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"STK Push error: {str(e)}")
            return {"error": str(e)}
    
    def b2c_payment(self, phone_number, amount, occasion, remarks):
        \"\"\"Send B2C payment (Business to Customer)\"\"\"
        if not self.access_token:
            self.get_access_token()
        
        if not self.access_token:
            return {"error": "Failed to get access token"}
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "OriginatorConversationID": f"freelancer_bot_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "InitiatorName": "testapi",
                "SecurityCredential": "your_security_credential_here",  # You'll need to generate this
                "CommandID": "BusinessPayment",
                "Amount": amount,
                "PartyA": self.shortcode,
                "PartyB": phone_number,
                "Remarks": remarks,
                "QueueTimeOutURL": "https://your-domain.com/mpesa/timeout",
                "ResultURL": "https://your-domain.com/mpesa/result",
                "Occasion": occasion
            }
            
            response = requests.post(self.b2c_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"B2C Payment error: {str(e)}")
            return {"error": str(e)}
    
    def query_transaction_status(self, checkout_request_id):
        \"\"\"Query STK push transaction status\"\"\"
        if not self.access_token:
            self.get_access_token()
        
        if not self.access_token:
            return {"error": "Failed to get access token"}
        
        try:
            password, timestamp = self.generate_password()
            
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "BusinessShortCode": self.shortcode,
                "Password": password,
                "Timestamp": timestamp,
                "CheckoutRequestID": checkout_request_id
            }
            
            response = requests.post(self.query_url, json=payload, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Query transaction error: {str(e)}")
            return {"error": str(e)}

# Initialize service
mpesa_service = MpesaService()
"""

with open("freelancers_bot/services/mpesa_service.py", "w") as f:
    f.write(mpesa_service_content)

print("M-Pesa service integration created!")
