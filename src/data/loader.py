import pandas as pd
from src.config import SYMBOL

def fetch_historical_candles(fyers, start_date, end_date, symbol=SYMBOL):
    """Fetches historical data from Fyers API."""
    data_req = {
        "symbol": symbol,
        "resolution": "D",
        "date_format": "1",
        "range_from": start_date,
        "range_to": end_date,
        "cont_flag": "1"
    }
    
    print(f"Fetching data for {symbol} ({start_date} to {end_date})...")
    response = fyers.history(data_req)
    
    if 'candles' not in response:
        raise ValueError(f"Error fetching data: {response}")
        
    cols = ['epoch', 'open', 'high', 'low', 'close', 'volume']
    df = pd.DataFrame(response['candles'], columns=cols)
    df['date'] = pd.to_datetime(df['epoch'], unit='s')
    df.set_index('date', inplace=True)
    return df