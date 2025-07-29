# Algorithmic Trading With Deep Learning

An end‑to‑end algorithmic trading bot that uses an LSTM neural network to predict future price movements and execute trades automatically via MetaTrader 5, with real‑time Telegram notifications.

---

## Table of Contents

- [Features](#features)  
- [Architecture](#architecture)  
- [Prerequisites](#prerequisites)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Running the Bot](#running-the-bot)  
- [Project Structure](#project-structure)  
- [Environment Variables](#environment-variables)  

---

## Features

- **Data Acquisition**: Fetches live OHLCV data directly from MetaTrader 5.  
- **Data Preprocessing**: Normalizes and sequences data for the LSTM.  
- **LSTM Model**: Two‑layer LSTM (64 units each) with dropout, predicting High/Low/Close.  
- **Automated Trading**: Places buy/sell orders based on prediction confidence and ATR‑based risk management.  
- **Telegram Alerts**: Sends trade signals, retraining notifications, metrics, and errors to your Telegram chat.  
- **Logging & Monitoring**: Console and rotating‐file logging for full audit trail.  

---

## Architecture

1. **DataLoader** (`algo_trader/data/loader.py`)  
   Connects to MT5, downloads and formats historical bars.  

2. **Preprocessor** (`algo_trader/data/preprocess.py`)  
   Scales features/targets and builds look‑back sequences for the LSTM.  

3. **Model**  
   - **Architecture** (`algo_trader/model/architecture.py`): Builds the Keras LSTM.  
   - **Trainer** (`algo_trader/model/trainer.py`): Handles training, checkpointing, and notifications.  
   - **Predictor** (`algo_trader/model/predictor.py`): Runs inference and computes % changes.  

4. **Trading Logic**  
   - **RiskManager** (`algo_trader/trading/risk.py`): Computes ATR for dynamic SL/TP.  
   - **OrderExecutor** (`algo_trader/trading/executor.py`): Sends orders to MT5 when thresholds are met.  
   - **Scheduler** (`algo_trader/trading/scheduler.py`): Main loop for retraining, prediction, trading, and waiting.  

5. **Utilities**  
   - **Config** (`algo_trader/config.py`): Centralizes all `.env` settings.  
   - **Logging** (`algo_trader/utils/logging_setup.py`): Console + rotating‑file logger.  
   - **Telegram** (`algo_trader/utils/telegram.py`): Sends messages & photos.  
   - **Plotting** (`algo_trader/utils/plotting.py`): Generates training and prediction charts.  

---

## Prerequisites

- **Python 3.7+**  
- **MetaTrader 5 terminal** installed & configured  
- A **MetaTrader 5 account** (demo or live) with algorithmic trading enabled  
- **Internet access** for MT5 API and Telegram Bot API  

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YourUser/Algorithmic-Trading-With-Deep-Learning.git
   cd Algorithmic-Trading-With-Deep-Learning
   
2. Install Dependencies:
   pip install -r requirements.txt

## Configuration

1.Copy the example environment file and fill in your details:
  cp .env.example .env
  
2. Open .env in your editor and supply:

  MT5_LOGIN, MT5_PASSWORD, MT5_SERVER — your MetaTrader 5 credentials.
  
  TELEGRAM_TOKEN, TELEGRAM_CHAT_ID — from your Telegram Bot (via BotFather) and chat.
  
  SYMBOL, TIMEFRAME — the instrument and chart timeframe you wish to trade.
  
  LOOK_BACK, PRICE_CHANGE_THRESHOLD, SL_MULTIPLIER, TP_MULTIPLIER, LOT_SIZE, RETRAIN_HOURS — model & trading hyperparameters.
  
  LOG_LEVEL, LOG_FILE — logging verbosity and file.
  
  **Note: Do not commit your real .env file. It’s git‑ignored.**

## Running the Bot

After configuration, simply run:
  python main.py
  
You should see startup logs in the console and in trading.log, and get a “Bot started” message in Telegram. The bot will:

  1.Download historical bars
  
  2.Train (or load) the LSTM model
  
  3.Enter its main loop of:

    Periodic retraining every RETRAIN_HOURS
    
    Predicting the next candle
    
    Placing orders when price‐change ≥ PRICE_CHANGE_THRESHOLD%
    
    Sleeping until the next candle based on TIMEFRAME

Press Ctrl+C to stop; the MT5 connection will shut down cleanly.  

## Environment Variables

| Variable                     | Description                                        |
| ---------------------------- | -------------------------------------------------- |
| **MT5\_LOGIN**               | Your MT5 account number (integer)                  |
| **MT5\_PASSWORD**            | Your MT5 password                                  |
| **MT5\_SERVER**              | Your broker’s MT5 server name                      |
| **TELEGRAM\_TOKEN**          | Your Telegram bot token (string)                   |
| **TELEGRAM\_CHAT\_ID**       | The Telegram chat ID to receive messages (integer) |
| **SYMBOL**                   | Trading symbol (e.g. `EURUSD`)                     |
| **TIMEFRAME**                | Chart timeframe (e.g. `H1`, `M15`)                 |
| **LOOK\_BACK**               | Number of past bars for LSTM sequences             |
| **PRICE\_CHANGE\_THRESHOLD** | Minimum % price change to trigger a trade          |
| **SL\_MULTIPLIER**           | ATR multiplier for Stop Loss                       |
| **TP\_MULTIPLIER**           | ATR multiplier for Take Profit                     |
| **LOT\_SIZE**                | Trade volume in lots                               |
| **RETRAIN\_HOURS**           | Hours between automatic retraining                 |
| **LOG\_LEVEL**               | Logging level (`DEBUG`, `INFO`, `WARNING`, etc.)   |
| **LOG\_FILE**                | Filename for rotating file logs                    |


