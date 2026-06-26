# Binance USD-M Futures BTCUSDT Trading Bot

A robust, automated trading bot for **Binance USD-M Futures** perpetual contracts on **BTCUSDT**, built with the `binance-futures-connector-python` library. The bot implements a complete trading strategy using EMA crossovers combined with candle pattern filters and ATR-based rules, along with position management, pyramiding, trailing stop-losses, and comprehensive monitoring.

Deployed as a Flask web application (suitable for platforms like Render.com), it runs scheduled tasks, maintains a live dashboard, sends email notifications, and includes robust error handling and logging.

## Key Features

- **Real-time & Historical Data**: Fetches 1-minute klines via REST API and streams live updates via WebSocket.
- **Technical Indicators**:
  - EMA 5 and EMA 34 (on HL2).
  - ATR (Average True Range) for volatility filtering.
- **Trading Strategy**:
  - **Long Entry**: EMA5 > EMA34 + specific candle momentum and range conditions.
  - **Short Entry**: EMA34 > EMA5 + corresponding short conditions.
  - Additional ATR-based gap thresholds and length filters.
- **Position Management**:
  - Market order entry.
  - Initial Stop-Loss + Trailing Stop-Loss (TSL).
  - Dynamic exit on crossover reversal or TSL/SL hits.
  - Optional pyramiding (adding to winning positions).
- **Risk Controls**:
  - Isolated margin.
  - Configurable leverage.
  - Precision handling for price and quantity.
- **Monitoring & Alerts**:
  - Email notifications for order open/close, errors, daily reports, and startup (with public IP).
  - Real-time trade logging and profit tracking.
  - Web dashboard showing recent trades.
- **Automation**:
  - Background scheduler (APScheduler) runs core logic every 30 seconds.
  - Daily report dumping.
  - Web app keep-alive mechanism.
- **Error Resilience**: Comprehensive try/except blocks, logging, and error email alerts.

## Project Structure
binfut_usdm_btcusdt-main.zip
Read through all the content in this attached zip file of a small github repository and give me a detailed description summary of what the code does, which will be used to fill this repository's readme file.
Output Rules - Give me the description in a markdown file syntax and not as a plain text (I need the final summary content in copy pastable markdown syntax )


Thought for 10s
# Binance USD-M Futures BTCUSDT Trading Bot

A robust, automated trading bot for **Binance USD-M Futures** perpetual contracts on **BTCUSDT**, built with the `binance-futures-connector-python` library. The bot implements a complete trading strategy using EMA crossovers combined with candle pattern filters and ATR-based rules, along with position management, pyramiding, trailing stop-losses, and comprehensive monitoring.

Deployed as a Flask web application (suitable for platforms like Render.com), it runs scheduled tasks, maintains a live dashboard, sends email notifications, and includes robust error handling and logging.

## Key Features

- **Real-time & Historical Data**: Fetches 1-minute klines via REST API and streams live updates via WebSocket.
- **Technical Indicators**:
  - EMA 5 and EMA 34 (on HL2).
  - ATR (Average True Range) for volatility filtering.
- **Trading Strategy**:
  - **Long Entry**: EMA5 > EMA34 + specific candle momentum and range conditions.
  - **Short Entry**: EMA34 > EMA5 + corresponding short conditions.
  - Additional ATR-based gap thresholds and length filters.
- **Position Management**:
  - Market order entry.
  - Initial Stop-Loss + Trailing Stop-Loss (TSL).
  - Dynamic exit on crossover reversal or TSL/SL hits.
  - Optional pyramiding (adding to winning positions).
- **Risk Controls**:
  - Isolated margin.
  - Configurable leverage.
  - Precision handling for price and quantity.
- **Monitoring & Alerts**:
  - Email notifications for order open/close, errors, daily reports, and startup (with public IP).
  - Real-time trade logging and profit tracking.
  - Web dashboard showing recent trades.
- **Automation**:
  - Background scheduler (APScheduler) runs core logic every 30 seconds.
  - Daily report dumping.
  - Web app keep-alive mechanism.
- **Error Resilience**: Comprehensive try/except blocks, logging, and error email alerts.

## Project Structure
binfut_usdm_btcusdt-main/
├── main.py                          # Flask app, scheduler, main orchestration
├── data_fetcher.py                  # REST + WebSocket data fetching
├── indicator_calculation.py         # EMA & ATR calculations
├── trading_rules.py                 # Entry condition logic
├── trading_logic.py                 # Core trading state machine
├── order_placer.py                  # Market order + fallback SL placement
├── new_order_placer.py              # Generic order placement helper
├── order_closer.py                  # Position closing and order cancellation
├── misc_bin_func.py                 # Utilities (balance, leverage, precision, etc.)
├── emailer.py                       # Email notifications & daily reports
├── tsl_setter.py                    # Trailing Stop-Loss order handling
├── keeping_webapp_alive.py          # Ping to prevent Render sleep
├── trading_journal.py               # Trade logging (partial)
├── templates/                       # Flask HTML templates
│   ├── btcusdt_binance_futures_homepage.html
│   └── btcusdt_binance_futures_dummy_homepage.html
├── requirements.txt
└── todo.txt


## How It Works

1. **Initialization** (on first load):
   - Sets leverage and margin type.
   - Closes any unwanted pre-existing positions.
   - Fetches initial candle data and calculates indicators.
   - Starts WebSocket stream and APScheduler.

2. **Main Loop** (every 30 seconds):
   - Updates latest candle data.
   - Recalculates indicators.
   - Evaluates entry/exit conditions.
   - Manages active positions (entry, pyramiding, TSL monitoring, exits).
   - Logs trades and sends email alerts.

3. **Web Interface**:
   - Accessible at the deployed URL.
   - Displays recent executed trades in a table.
   - Shows current position status.

4. **Notifications**:
   - Startup confirmation with public IP.
   - Order open/close alerts.
   - Error reports with log attachments.
   - Daily trading summary (Excel + HTML table).

## Configuration

Key parameters (in `main.py`):
- Initial order: ~5 USDT at 5x leverage (isolated).
- Pyramiding logic (currently partially disabled via lock).
- TSL and SL distances.
- EMA lengths, ATR length, and various filter thresholds.

Environment variables required:
- `BINANCE_API_KEY`
- `BINANCE_SECRET_KEY`
- `WEB_APP_URL` (for keep-alive)

## Dependencies

See `requirements.txt`:
- Flask, APScheduler, pandas, pandas_ta, binance-futures-connector, python-dotenv, etc.

## Deployment

Designed for headless deployment (e.g., Render.com):
- Uses Gunicorn in production.
- Includes keep-alive pings.
- Persistent logging and error tracking.

## Disclaimer

This is a **trading bot** involving real financial risk. Use at your own risk. Thoroughly backtest the strategy and start with small amounts in testnet mode before using real capital. The authors/maintainers are not responsible for any losses.

---

**Status**: Actively developed with modular architecture for easy extension of strategies, risk rules, or notification channels.
