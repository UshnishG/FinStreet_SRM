import pandas as pd
import numpy as np

def predict_probabilities(model, df, features=['SMA_10', 'SMA_20', 'RSI']):
    """
    Uses the trained model to infer probabilities for the given data.
    
    Args:
        model: The trained Random Forest model.
        df (pd.DataFrame): Input dataframe containing the feature columns.
        features (list): List of feature names to use for prediction.
        
    Returns:
        np.array: Confidence scores (probabilities) for class 1 (Buy).
    """
    # 1. Validation: Ensure all features exist in the dataframe
    missing_features = [f for f in features if f not in df.columns]
    if missing_features:
        raise ValueError(f"Input data is missing features: {missing_features}")

    # 2. Extract features
    X = df[features]
    
    # 3. Inference: Get probability of Class 1 (Target = 1 / Price Increase)
    # .predict_proba() returns an array like [[prob_0, prob_1], ...]
    try:
        probs = model.predict_proba(X)[:, 1]
        return probs
    except Exception as e:
        print(f"Error during inference: {e}")
        return np.zeros(len(df))