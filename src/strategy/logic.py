import pandas as pd
from src.api.client import place_order
from src.models.inference import predict_probabilities  # <--- Import the new function

def generate_signals(model, df_test, features=['SMA_10', 'SMA_20', 'RSI'], threshold=0.305):
    """
    Generates trading signals based on model confidence.
    """
    # Use the separated inference logic
    probs = predict_probabilities(model, df_test, features)
    
    df_test = df_test.copy()
    df_test['Confidence'] = probs
    df_test['Predicted_Signal'] = (probs > threshold).astype(int)
    
    return df_test

def execute_backtest_strategy(df_competition, fyers_client=None, initial_capital=100000):
    # ... (Rest of the function remains exactly the same)
    capital = initial_capital
    position = 0
    log = []
    daily_returns = []
    
    print("\n--- [Step 3] Executing Strategy Simulation ---")
    
    for index, row in df_competition.iterrows():
        price = row['close']
        signal = row['Predicted_Signal']
        qty = 100
        
        # BUY SIGNAL
        if signal == 1 and position == 0:
            cost = price * qty
            if capital >= cost:
                position = qty
                capital -= cost
                log.append(f"[BUY ] {index.date()} @ {price:.2f}")
                
                if fyers_client:
                    place_order(fyers_client, "NSE:IRCON-EQ", qty, 1)
                    
        # SELL SIGNAL
        elif signal == 0 and position > 0:
            revenue = price * position
            capital += revenue
            position = 0
            log.append(f"[SELL] {index.date()} @ {price:.2f} | Cash: {capital:.2f}")
            
        daily_returns.append(capital + (position * price))
        
    final_value = capital + (position * df_competition.iloc[-1]['close'])
    return final_value, log, daily_returns