# 📈 AI-Powered Algorithmic Trading Bot (NSE: IRCON)

This repository contains a modular algorithmic trading pipeline designed for the **Fyers APIv3**. It automates the entire trading workflow—from fetching historical market data and engineering technical features to training a Machine Learning model (Random Forest) and generating actionable Buy/Sell signals.

The system is currently configured for **NSE:IRCON-EQ** but can be easily adapted for other symbols.

## 📂 Project Structure

The project is organized into modular components for scalability and maintainability:

```text
├── .env                       # API Credentials
├── requirements.txt           # Python dependencies
├── main.py                    # Orchestrator: Runs the full pipeline
└── src/
    ├── api/                   # FYERS API Integration (Auth & Execution)
    ├── data/                  # Data Loading & Preprocessing
    ├── features/              # Feature Engineering Pipeline
    ├── models/                # Model Training & Inference Logic
    ├── strategy/              # Signal Generation & Trade Logic
    └── backtest/              # Performance Evaluation Metrics

```

---

## 🚀 Key Features

### 1. FYERS API Integration

**Location:** `src/api/`

* **Authentication:** Securely handles client credentials and access tokens using environment variables.
* **Data Fetching:** Retrieves historical OHLCV (Open, High, Low, Close, Volume) data efficiently.
* **Trade Execution:** Contains wrappers to place Intraday Buy/Sell orders directly to the exchange.

### 2. Data Loading & Preprocessing

**Location:** `src/data/loader.py`

* Connects to the Fyers History API to fetch raw candlestick data.
* Cleans and formats timestamps.
* Handles missing data and ensures the DataFrame is indexed by date.

### 3. Feature Engineering Pipeline

**Location:** `src/features/indicators.py`

* Uses `pandas_ta` to generate technical indicators:
* **SMA_10 & SMA_20:** Simple Moving Averages for trend detection.
* **RSI (14):** Relative Strength Index for momentum.


* Creates the **Target Variable**: A binary label (1 if the *next day's* close is higher than today's, else 0).

### 4. Model Training & Inference

**Location:** `src/models/`

* **Training (`train.py`):** Uses a **Random Forest Classifier** (`n_estimators=100`) to learn patterns from historical data.
* **Inference (`inference.py`):** A dedicated module that accepts live data and returns raw probability scores (Confidence) for the "Buy" class.

### 5. Trading Strategy

**Location:** `src/strategy/logic.py`

* **Signal Logic:** Converts model probabilities into trade signals.
* **Threshold:** Custom optimized threshold (Default: `> 0.305` or 30.5% confidence).


* **Execution Rules:**
* **Buy:** If Signal is 1 and no position exists.
* **Sell:** If Signal is 0 and a position exists (or at EOD for intraday).



### 6. Performance Evaluation

**Location:** `src/backtest/metrics.py`

* Simulates the strategy over a test dataset (e.g., Jan 1 - Jan 8).
* Calculates key financial metrics:
* **Net Profit (₹)**
* **ROI (%)**
* **Sharpe Ratio** (Risk-adjusted return)
* **Model Accuracy (%)**



---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ircon-trading-bot.git
cd ircon-trading-bot

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Configure Environment Variables

Create a file named `.env` in the root directory and add your Fyers credentials. **Do not share this file.**

```ini
FYERS_CLIENT_ID="Your_Client_ID-100"
FYERS_SECRET_KEY="Your_Secret_Key"
FYERS_REDIRECT_URI="https://www.google.com"
FYERS_ACCESS_TOKEN="Your_Generated_Access_Token"

```

---

## 🖥️ Usage

### Generate Access Token (First Time Only)

If you don't have a valid token, you can generate one using the helper in `src/api/auth.py` or by running a script that utilizes the `generate_auth_code` function.

### Run the Pipeline

Execute the main script to fetch data, train the model, and simulate the strategy:

```bash
python main.py

```

### Output Example

```text
========================================
FINAL REPORT
========================================
[BUY ] 2026-01-01 @ 177.98
[SELL] 2026-01-02 @ 179.22 | Cash: 100124.00
----------------------------------------
Model Accuracy: 66.67%
Net Profit:     ₹124.00
Total Return:   0.12%
Sharpe Ratio:   7.10
========================================

```

---

## ⚙️ Customization

* **Change Dates:** Open `main.py` and modify the date strings in `fetch_historical_candles`.
* **Tune Strategy:** Open `src/strategy/logic.py` to change the `threshold` (default 0.305).
* **Add Indicators:** Edit `src/features/indicators.py` to add MACD, Bollinger Bands, etc.

---

## ⚠️ Disclaimer


*This software is for educational purposes only. Do not trade with real money unless you fully understand the risks. The authors are not responsible for any financial losses incurred.*

