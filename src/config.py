import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("FYERS_CLIENT_ID")
SECRET_KEY = os.getenv("FYERS_SECRET_KEY")
REDIRECT_URI = os.getenv("FYERS_REDIRECT_URI")
ACCESS_TOKEN = os.getenv("FYERS_ACCESS_TOKEN")
SYMBOL = "NSE:IRCON-EQ"