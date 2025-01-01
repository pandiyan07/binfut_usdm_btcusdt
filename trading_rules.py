def CONDITION_VERIFIER(df):
    percentage = 0.1
    atr_value = 50

    last_5ema_value = float(df['ema_5'].iloc[-1])
    last_34ema_value = float(df['ema_34'].iloc[-1])
    last_atr_value = float(df['atr'].iloc[-1])
    current_candle_close = float(df["close"].iloc[-1])
    
    current_candle_open = float(df["open"].iloc[-1])
    previous_candle_close = float(df["close"].iloc[-2])
    previous_candle_open = float(df["open"].iloc[-2])
    second_previous_candle_close = float(df["close"].iloc[-3])
    second_previous_candle_open = float(df["open"].iloc[-3])
    
    if last_atr_value < atr_value:
        long_gap = 0.4  
        short_gap = 0.6 
        long_length = 30   
        short_length = 110
    else:
        long_gap = 0.65  
        short_gap = 0.65 
        long_length = 180   
        short_length = 200
    
    # Calculate the open-close differences for current and previous candles
    if current_candle_close > current_candle_open:
        current_candle_open_close_difference = ((current_candle_close - current_candle_open) * percentage) + current_candle_open
        previous_candle_open_close_difference = ((previous_candle_close - previous_candle_open) * percentage) + previous_candle_open
    else:
        current_candle_open_close_difference = current_candle_open - ((current_candle_open - current_candle_close) * percentage)
        previous_candle_open_close_difference = previous_candle_open - ((previous_candle_open - previous_candle_close) * percentage)

    # Long Trading conditions
    l1 = (current_candle_close - second_previous_candle_open) > long_length
    l2 = current_candle_close > last_5ema_value and current_candle_open > last_5ema_value
    l3 = current_candle_open_close_difference > previous_candle_close
    l4 = previous_candle_open_close_difference > second_previous_candle_close
    l5 = last_5ema_value > last_34ema_value
    
    # Short Trading conditions
    s1 = (second_previous_candle_open - current_candle_close) > short_length
    s2 = current_candle_close < last_5ema_value and current_candle_open < last_5ema_value
    s3 = current_candle_open_close_difference < previous_candle_close
    s4 = previous_candle_open_close_difference < second_previous_candle_close
    s5 = last_5ema_value < last_34ema_value
    
    Atr_rule = last_atr_value > atr_value

    long_entry_condition = l1 and l2 and l3 and l4 and l5# and Atr_rule
    short_entry_condition = s1 and s2 and s3 and s4 and s5# and Atr_rule
    
    return long_entry_condition, short_entry_condition, long_gap, short_gap, atr_value