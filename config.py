# Create config.py
config_content = """
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///freelancers_bot.db'
    
    # M-Pesa Configuration
    MPESA_CONSUMER_KEY = os.environ.get('MPESA_CONSUMER_KEY') or 'moEMNSeSDDFclE64XGTk2A0O0XGTFSZGonifdphRj8VHnYPg'
    MPESA_CONSUMER_SECRET = os.environ.get('MPESA_CONSUMER_SECRET') or 'cGoUmLHcuMUCfaubt66qPK3mUKOkfE7bQe1WdVvyLVNToLT1ou6DOaHblq4pyKKt'
    MPESA_SHORTCODE = os.environ.get('MPESA_SHORTCODE') or '174379'
    MPESA_PASSKEY = os.environ.get('MPESA_PASSKEY') or 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
    MPESA_ENVIRONMENT = os.environ.get('MPESA_ENVIRONMENT') or 'sandbox'
    
    # M-Pesa URLs
    MPESA_BASE_URL = 'https://sandbox.safaricom.co.ke' if MPESA_ENVIRONMENT == 'sandbox' else 'https://api.safaricom.co.ke'
    MPESA_AUTH_URL = f'{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials'
    MPESA_B2C_URL = f'{MPESA_BASE_URL}/mpesa/b2c/v3/paymentrequest'
    MPESA_STK_PUSH_URL = f'{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest'
    MPESA_QUERY_URL = f'{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query'
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # Application Settings
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
"""

with open("freelancers_bot/config.py", "w") as f:
    f.write(config_content)

print("Configuration file created!")
