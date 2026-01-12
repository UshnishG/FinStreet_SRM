import pandas as pd

def calculate_metrics(df, daily_returns, initial_capital=100000):
    """Calculates ROI, Sharpe Ratio, and Model Accuracy."""
    
    # 1. Profit & ROI
    final_value = daily_returns[-1]
    total_profit = final_value - initial_capital
    returns_pct = (total_profit / initial_capital) * 100
    
    # 2. Sharpe Ratio
    returns_series = pd.Series(daily_returns).pct_change().dropna()
    sharpe_ratio = 0
    if len(returns_series) > 1 and returns_series.std() > 0:
        sharpe_ratio = (returns_series.mean() / returns_series.std()) * (252**0.5)
        
    # 3. Model Accuracy
    df['Actual_Target'] = (df['close'].shift(-1) > df['close']).astype(int)
    matches = df['Predicted_Signal'] == df['Actual_Target']
    accuracy = matches.mean() * 100
    
    return {
        "net_profit": total_profit,
        "return_pct": returns_pct,
        "sharpe_ratio": sharpe_ratio,
        "model_accuracy": accuracy
    }

def print_report(log, metrics):
    print("\n" + "="*40)
    print(f"FINAL REPORT")
    print("="*40)
    for l in log:
        print(l)
    print("-" * 40)
    print(f"Model Accuracy: {metrics['model_accuracy']:.2f}%")
    print(f"Net Profit:     ₹{metrics['net_profit']:.2f}")
    print(f"Total Return:   {metrics['return_pct']:.2f}%")
    print(f"Sharpe Ratio:   {metrics['sharpe_ratio']:.2f}")
    print("="*40)