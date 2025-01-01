import logging
from binance.um_futures import UMFutures
from binance.lib.utils import config_logging
import pandas as pd
from datetime import datetime

import time
import json  # Import json to parse the message
from binance.websocket.um_futures.websocket_client import UMFuturesWebsocketClient

# Configure logging for debugging
config_logging(logging, logging.DEBUG)



def REST_API_DATFET():
    # Initialize the Binance USD-M Futures client
    umfut_rest_api_client = UMFutures()

    # Download the last 40 one-minute candles for BTCUSDT
    candles = umfut_rest_api_client.klines("BTCUSDT", "1m", limit=40)

    # Convert the candle data to a DataFrame
    columns = [
        "timestamp", "open", "high", "low", "close", "volume", 
        "close_time", "quote_asset_volume", "number_of_trades", 
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", 
        "ignore"
    ]
    df = pd.DataFrame(candles, columns=columns)
    df = df[[ "open", "high", "low", "close","close_time"]]

    # Convert timestamp columns to a readable datetime format
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms').dt.strftime('%H:%M:%S')

    return df


# Initialize a variable to store the latest OHLC data
ohlc_data = {}

# Define the message handler
def message_handler(_, message):
    global ohlc_data
    # Parse the message if it's in JSON string format
    data = json.loads(message) if isinstance(message, str) else message
    
    # Extract kline data if present in the message
    if "k" in data:
        kline = data["k"]
        ohlc_data = {
            "open": [kline["o"]],
            "high": [kline["h"]],
            "low": [kline["l"]],
            "close": [kline["c"]]
        }

def WEBSOCKET_STREAMING_DATFET():
    # Initialize the WebSocket client and start receiving kline data
    my_client = UMFuturesWebsocketClient(on_message=message_handler)
    my_client.kline(symbol="btcusdt", id=1, interval="1m")
    return my_client

def CHOOSY_PICKY_DATA_FETCHER():
    global ohlc_data
    entry_time = datetime.utcnow()
    ohlc_data['close_time'] = [entry_time.strftime('%H:%M:%S')]
    ohlc_data = pd.DataFrame(ohlc_data)
    return ohlc_data


def STOPPING_WEBSOCKET_STREAMING(my_client):
    # Stop the WebSocket connection
    logging.debug("closing ws connection")
    my_client.stop()