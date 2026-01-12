import pandas_ta as ta

def add_technical_indicators(df):
    """Adds SMA_10, SMA_20, RSI, and Target column."""
    df = df.copy()
    df['SMA_10'] = ta.sma(df['close'], length=10)
    df['SMA_20'] = ta.sma(df['close'], length=20)
    df['RSI'] = ta.rsi(df['close'], length=14)
    
    # Create target for training (1 if Next Day Close > Today Close)
    df['Target'] = (df['close'].shift(-1) > df['close']).astype(int)
    
    df.dropna(inplace=True)
    return df