

def ENTRY_WORK(last_close, no_of_trade, action, entry_price, max_profit_price):
    no_of_trade += 1
    action = 'ENTER_TRADE'
    entry_price = last_close
    max_profit_price = last_close
    return no_of_trade, action, entry_price,max_profit_price
def EXITING_WORK(action, max_profit_price, current_profit_made):
    action = 'EXIT_TRADE'
    max_profit_price = 0
    current_profit_made = 0
    return action, max_profit_price, current_profit_made



def TRADING_LOGIC(Order_limiter, df, action, status, long_entry_condition, short_entry_condition, pyramid_threshhold, max_profit_price, current_profit_made, entry_price, no_of_trade, max_gap, Initital_trade_lock, long_gap, short_gap, atr_value, position):
    
    last_5ema_value = float(df['ema_5'].iloc[-1])
    last_34ema_value = float(df['ema_34'].iloc[-1])
    last_atr_value = float(df['atr'].iloc[-1])
    current_candle_close = float(df["hl2"].iloc[-1])
    
    trailing_stop_percentage_long = 0.85  # 85% of the maximum profit for long trades                               
    trailing_stop_percentage_short = 0.85  # 85% of the maximum profit for short trades 
    
    if last_5ema_value is not None and last_34ema_value is not None:
        last_close = float(current_candle_close) 
        print('position = ',position)
        
        if position is None:
            if long_entry_condition: 
                no_of_trade, action, entry_price, max_profit_price = ENTRY_WORK(last_close,no_of_trade, action, entry_price,max_profit_price)
                max_gap = last_5ema_value - last_34ema_value
                position = 'LONG'
                status = 'Long trade'
            elif short_entry_condition:
                no_of_trade, action, entry_price, max_profit_price = ENTRY_WORK(last_close,no_of_trade, action, entry_price,max_profit_price)
                max_gap = last_34ema_value - last_5ema_value
                position = 'SHORT'
                status = 'Short trade'
            
            print ('================== >>>  Status, Action = ',status,action)
        
        
        if position == 'LONG':
            current_gap = last_5ema_value - last_34ema_value
            max_gap = max(max_gap, current_gap) 
            if current_gap < max_gap * long_gap: 
                status = 'Exit crossover'
                action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
            
            # Trailing stop loss
            max_profit_price = max(max_profit_price, last_close)
            max_profit_made = round(max_profit_price - entry_price,1)                                            
            TSL = round(max_profit_made * trailing_stop_percentage_long,1)                   
            current_profit_made = round(last_close - entry_price,1)     
            print('current_profit_made = ',current_profit_made)                          
            
            if last_atr_value < atr_value:          # Maximum atr_value on 19 & 20 october is 60 or 61
                if current_profit_made < -15:
                    status = 'SL hit'
                    action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
                if current_profit_made < TSL and current_profit_made > 15:                  
                    status = 'TSL hit'
                    action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
            
            print ('================== >>>  Status, Action = ',status,action)


        elif position == 'SHORT':
            
            # Exit trade if the gap shortens
            current_gap = last_34ema_value - last_5ema_value
            max_gap = max(max_gap, current_gap)
            if current_gap < max_gap * short_gap:
                status = 'Exit crossover'
                action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
                
            # Trailing stop loss
            max_profit_price = min(max_profit_price, last_close)
            max_profit_made = round(entry_price - max_profit_price,1)                                        
            TSL = round(max_profit_made * trailing_stop_percentage_short,1)               
            current_profit_made = round(entry_price - last_close,1)                               
            
            if last_atr_value < atr_value:                      # Maximum atr_value on 19 & 20 october is 60 or 61
                if current_profit_made < -15:
                    status = 'SL hit'
                    action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
                if current_profit_made < TSL and current_profit_made > 15:        
                    status = 'TSL hit'
                    action, max_profit_price, current_profit_made = EXITING_WORK(action, max_profit_price, current_profit_made)
            
            print ('================== >>>  Status, Action = ',status,action)
        
        
        
        
        #   PYRAMIDING order placement with MAXIMUM LEVERAGE
        if current_profit_made > pyramid_threshhold and position is not None:
            if position == 'LONG' and last_close > last_5ema_value and last_close >= max_profit_price and Initital_trade_lock:
                no_of_trade, action, entry_price,max_profit_price = ENTRY_WORK(last_close,no_of_trade, action, entry_price,max_profit_price)
                print(f'-----------------> Entered PYRAMIDING LONG position. ,{current_profit_made}')
                status = 'Long lvg & pyr'
                print ('================== >>>  Pyramiding Status, Action = ',status,action)
                
            elif position == 'SHORT' and last_close < last_5ema_value and last_close <= max_profit_price and Initital_trade_lock:
                no_of_trade, action, entry_price,max_profit_price = ENTRY_WORK(last_close,no_of_trade, action, entry_price,max_profit_price)
                print(f'-----------------> Entered PYRAMIDING SHORT position.,{current_profit_made}')
                status = 'Short lvg & pyr'
                print ('================== >>>  Pyramiding Status, Action = ',status,action)
        
        return Order_limiter, action, status, position, max_profit_price, current_profit_made, entry_price, no_of_trade, max_gap, Initital_trade_lock, long_gap, short_gap, atr_value