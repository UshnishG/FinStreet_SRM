from fyers_apiv3 import fyersModel
from src.config import CLIENT_ID, ACCESS_TOKEN

def get_fyers_client(token=None):
    """Returns an authenticated FyersModel instance."""
    use_token = token if token else ACCESS_TOKEN
    return fyersModel.FyersModel(client_id=CLIENT_ID, token=use_token, log_path="")

def place_order(fyers, symbol, qty, signal):
    """Places an intraday order based on signal (1=Buy, 0=Sell logic handled in strategy)."""
    # Note: Your original script only places BUY orders via API.
    # Logic extracted from test_ircon.py
    if signal == 1:
        data = {
            "symbol": symbol,
            "qty": qty,
            "type": 2,          # Market Order
            "side": 1,          # Buy
            "productType": "INTRADAY",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY"
        }
        print(f"--> API CALL: fyers.place_order({data})")
        # response = fyers.place_order(data) # Uncomment to enable live trading
        # return response