import pandas as pd
from src.api.client import get_fyers_client
from src.data.loader import fetch_historical_candles
from src.features.indicators import add_technical_indicators
from src.models.train import train_model
from src.strategy.logic import generate_signals, execute_backtest_strategy
from src.backtest.metrics import calculate_metrics, print_report
from src.config import SYMBOL

def main():
    # 1. Initialize API
    fyers = get_fyers_client()
    
    # 2. Training Pipeline (Nov 2025 - Dec 2025)
    print("Fetching Training Data...")
    raw_train = fetch_historical_candles(fyers, "2025-11-01", "2025-12-31", SYMBOL)
    df_train = add_technical_indicators(raw_train)
    
    # 3. Model Training
    model = train_model(df_train)
    
    # 4. Testing Pipeline (Dec 2025 - Jan 2026)
    print("\nFetching Test Data...")
    raw_test = fetch_historical_candles(fyers, "2025-12-01", "2026-01-08", SYMBOL)
    df_test = add_technical_indicators(raw_test)
    
    # Filter for competition dates (Jan 1 onwards)
    df_competition = df_test[df_test.index >= '2026-01-01'].copy()
    
    if len(df_competition) == 0:
        print("No data found for Jan 1-8.")
        return

    # 5. Signal Generation
    df_scored = generate_signals(model, df_competition)
    
    # 6. Execution & Backtest
    final_val, log, daily_returns = execute_backtest_strategy(df_scored, fyers_client=fyers)
    
    # 7. Evaluation
    metrics = calculate_metrics(df_scored, daily_returns)
    print_report(log, metrics)

if __name__ == "__main__":
    main()