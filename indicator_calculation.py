import pandas_ta as ta

def ATR_CALCULATOR(df,length):
    return ta.atr(df['high'].astype(float), df['low'].astype(float), df['close'].astype(float), length=length)            

def EMA_CALCULATOR(df, length):
    df['hl2'] = (df['high'].astype(float) + df['low'].astype(float)) / 2
    return ta.ema(df['hl2'], length=length)

def INDICATOR_CALCULATOR( df, atr_len, small_ema_len, large_ema_len):
    df['ema_5'] = EMA_CALCULATOR(df, small_ema_len)
    df['ema_34'] = EMA_CALCULATOR(df, large_ema_len)
    df['atr'] = ATR_CALCULATOR(df, atr_len)
    return df