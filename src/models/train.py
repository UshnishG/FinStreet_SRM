from sklearn.ensemble import RandomForestClassifier

def train_model(df_train):
    """Trains the Random Forest model."""
    features = ['SMA_10', 'SMA_20', 'RSI']
    X_train = df_train[features]
    y_train = df_train['Target']
    
    print("--- [Step 1] Training Random Forest Model ---")
    model = RandomForestClassifier(n_estimators=100, min_samples_split=10, random_state=42)
    model.fit(X_train, y_train)
    print(f"Model Trained on {len(df_train)} rows.")
    return model