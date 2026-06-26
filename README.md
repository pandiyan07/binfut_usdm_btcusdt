# 🚀 Binance USD-M Futures BTCUSDT Trading Bot

A robust and fully automated trading bot for **Binance USD-M Futures** perpetual contracts on **BTCUSDT**, built using the official **Binance Futures Connector for Python** (`binance-futures-connector-python`).

The bot implements a comprehensive algorithmic trading strategy based on **EMA crossovers**, **candlestick momentum analysis**, and **ATR-based volatility filtering**. It also includes advanced position management features such as **pyramiding**, **trailing stop-loss**, automated order execution, live monitoring, email notifications, and a web-based dashboard.

Designed as a **Flask web application**, the project can be deployed on cloud platforms such as **Render.com** for continuous **24×7** operation.

---

# ✨ Key Features

## 📈 Live Market Data

* Fetches historical **1-minute BTCUSDT Futures** candlestick data using the Binance REST API.
* Streams real-time market updates using Binance WebSockets.
* Continuously updates trading indicators without restarting the application.

---

## 📊 Technical Indicators

The trading strategy utilizes the following technical indicators:

* **EMA (5)** calculated on **HL2**
* **EMA (34)** calculated on **HL2**
* **ATR (Average True Range)** for volatility filtering

---

## 🧠 Trading Strategy

The strategy combines **trend-following** and **momentum confirmation**.

### ✅ Long Entry

A long position is opened when:

* EMA(5) crosses above EMA(34)
* Bullish candle momentum is confirmed
* ATR satisfies volatility requirements
* Additional candle range and trend filters are met

### 📉 Short Entry

A short position is opened when:

* EMA(5) crosses below EMA(34)
* Bearish candle momentum is confirmed
* ATR satisfies volatility requirements
* Additional candle range and trend filters are met

---

## 💼 Position Management

The bot automatically manages the complete trade lifecycle:

* Market order execution
* Initial Stop-Loss (SL)
* Trailing Stop-Loss (TSL)
* Dynamic exit on EMA crossover reversal
* Automatic position closing
* Optional pyramiding (adding to winning positions)

---

## 🛡️ Risk Management

Built-in risk management features include:

* Isolated Margin Mode
* Configurable leverage
* Exchange precision handling
* ATR-based volatility filtering
* Dynamic Stop-Loss management

---

## 📧 Monitoring & Notifications

The application automatically sends email notifications for:

* 🚀 Bot startup
* 🌐 Public IP address on startup
* 📈 Trade entry
* 📉 Trade exit
* 📊 Daily trading report
* 🚨 Error alerts with log attachments

Additional monitoring includes:

* Live trade logging
* Profit & Loss tracking
* Interactive web dashboard

---

## ⚙️ Automation

The bot operates autonomously using **APScheduler**.

Scheduled tasks include:

* Executing the trading strategy every **30 seconds**
* Generating daily trading reports
* Sending keep-alive requests to prevent Render from sleeping
* Continuously monitoring market conditions

---

## 🚨 Error Handling

Robust exception handling is implemented throughout the application.

Features include:

* Comprehensive logging
* Automatic error detection
* Email notifications with stack traces
* Log file attachments
* Graceful recovery where possible

---

# 📂 Project Structure

```text
binfut_usdm_btcusdt-main/
│
├── main.py                          # Flask application and scheduler
├── data_fetcher.py                  # REST API & WebSocket market data
├── indicator_calculation.py         # EMA and ATR calculations
├── trading_rules.py                 # Trading entry conditions
├── trading_logic.py                 # Core trading state machine
├── order_placer.py                  # Market order execution and SL placement
├── new_order_placer.py              # Generic order placement helper
├── order_closer.py                  # Position closing and order cancellation
├── misc_bin_func.py                 # Utility functions (balance, leverage, precision)
├── emailer.py                       # Email notifications and daily reports
├── tsl_setter.py                    # Trailing Stop-Loss management
├── keeping_webapp_alive.py          # Prevents Render application from sleeping
├── trading_journal.py               # Trade logging and reporting
│
├── templates/
│   ├── btcusdt_binance_futures_homepage.html
│   └── btcusdt_binance_futures_dummy_homepage.html
│
├── requirements.txt
└── todo.txt
```

---

# ⚙️ How It Works

## 1️⃣ Initialization

When the application starts, it performs the following steps:

* Configures leverage and margin type
* Closes unwanted pre-existing positions
* Downloads historical candle data
* Calculates technical indicators
* Starts the Binance WebSocket stream
* Starts the APScheduler background jobs

---

## 2️⃣ Continuous Trading Loop

Every **30 seconds**, the scheduler performs the following operations:

1. Fetches the latest candle data
2. Updates technical indicators
3. Evaluates entry conditions
4. Evaluates exit conditions
5. Places new market orders (if required)
6. Monitors active positions
7. Updates trailing stop-loss orders
8. Executes pyramiding logic
9. Logs completed trades
10. Sends trade notifications

---

## 3️⃣ Web Dashboard

The Flask dashboard provides real-time monitoring by displaying:

* Current trading status
* Active position
* Recent trade history
* Profit & Loss summary

---

## 4️⃣ Notifications

The application automatically sends email notifications for:

* ✅ Startup confirmation
* 🌐 Public IP address
* 📈 Trade entry alerts
* 📉 Trade exit alerts
* 📄 Daily trading report (Excel + HTML)
* 🚨 Error reports with attached log files

---

# ⚙️ Configuration

Key strategy parameters are configured within **`main.py`**.

These include:

* Initial order size (~5 USDT)
* Leverage (5×)
* Margin mode
* EMA periods
* ATR period
* Stop-Loss distance
* Trailing Stop-Loss distance
* Pyramiding configuration
* Strategy thresholds

---

# 🔐 Environment Variables

Create a `.env` file containing the following variables:

```env
BINANCE_API_KEY=YOUR_BINANCE_API_KEY
BINANCE_SECRET_KEY=YOUR_BINANCE_SECRET_KEY
WEB_APP_URL=YOUR_RENDER_APPLICATION_URL
```

---

# 📦 Dependencies

Install the required packages using:

```bash
pip install -r requirements.txt
```

Core dependencies include:

* Flask
* APScheduler
* Pandas
* Pandas TA
* binance-futures-connector
* python-dotenv
* Requests

---

# ☁️ Deployment

The project is designed for cloud deployment and runs seamlessly on platforms such as **Render.com**.

Deployment features include:

* Gunicorn production server
* Automatic keep-alive requests
* Persistent logging
* Background scheduler
* Error monitoring
* Email notifications

---

# ⚠️ Disclaimer

> **This project is intended for educational and research purposes only.**

Trading cryptocurrencies and leveraged derivatives involves significant financial risk. Always perform thorough backtesting and forward testing before deploying this strategy with real funds.

The authors and contributors assume **no responsibility** for any financial losses incurred through the use of this software.

---

# 🚧 Project Status

> **🟢 Actively Developed**

The project follows a modular architecture, making it easy to extend with:

* Additional trading strategies
* New technical indicators
* Enhanced risk management
* Multi-symbol trading
* Database integration
* Telegram / Discord notifications
* Performance analytics
* Machine Learning–based trading models

---

## ⭐ Support the Project

If you find this project useful, consider giving it a **⭐ Star** on GitHub. Contributions, suggestions, and pull requests are always welcome!
