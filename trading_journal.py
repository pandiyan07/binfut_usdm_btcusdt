from datetime import datetime
import pandas as pd

def TRADE_LOGGER(close_order, open_trades, status,bal_amnt):
    
    transact_time_ms = close_order['transactTime']
    transact_time_seconds = transact_time_ms / 1000
    transact_time_readable = datetime.utcfromtimestamp(transact_time_seconds)
    formatted_time = transact_time_readable.strftime('%Y-%m-%d %H:%M:%S')
    print(f"Transaction Time: {formatted_time} UTC")
    
    exit_status = status
    exit_time = formatted_time
    
    log_entries = []
    
    for trade in open_trades:
        log_entry = {
            'T no': trade['trade_number'],
            'quantity': trade['quantity'],
            'position': trade['position'],
            'Entry price': trade['entry_price'],
            'Entry time' : trade['entry_time'],
            'Exit time' : exit_time,
            'Exit status': exit_status,
            'Balance amount': bal_amnt
        }
        log_entries.append(log_entry)
    log_entry_df = pd.DataFrame(log_entries)
    trade_log_df = pd.concat([trade_log_df, log_entry_df], ignore_index=True)
    
    return trade_log_df