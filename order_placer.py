from datetime import datetime
from misc_bin_func import *
from new_order_placer import *
import time


def FALLBACK_PLACE_STOP_LOSS(client, input, side, entry_price, sl_distance):
    stop_loss_price = entry_price - sl_distance if side == "BUY" else entry_price + sl_distance
    try:
        sl_response = client.new_order(
            symbol=input[0],
            side="SELL" if side == "BUY" else "BUY",
            type="STOP_MARKET",
            quantity=input[2],
            stopPrice=stop_loss_price, # Stop loss price
            reduceOnly=True
        )
        print("\nSTOP LOSS PLACED AT = ",stop_loss_price)
        return sl_response
    except ClientError as error:
        print ('='*100)
        logging.error(
            "Found an error ===> STATUS = '{}', ERROR CODE = '{}', ERROR MESSAGE = '{}'".format(
                error.status_code, error.error_code, error.error_message
            )
        )
        print ('='*100)
        print(error)
        print ('='*100)
        return None
    

def OPEN_ORDER_PLACER(input, client, price_precision, quantity_precision, status, position):
    avg_fill_price = None
    all_ord_stat = None
    try:
        price = float(client.mark_price(symbol=input[0])['markPrice'])
    except ClientError as error:
        print ('='*100)
        logging.error(
            "Found an error ===> STATUS = '{}', ERROR CODE = '{}', ERROR MESSAGE = '{}'".format(
                error.status_code, error.error_code, error.error_message
            )
        )
        print ('='*100)
        print(error)
        print ('='*100)
        price = None
    
    if price:
        price = round(price, price_precision)
    else:
        print('THE MARK PRICE CANNOT BE FETCHED = ',price)
    
    
    
    
    if position == 'LONG':
        position_side = 'BUY'
    elif position == 'SHORT':
        position_side = 'SELL'

    try:
        market_order_response = NEW_ODR_PLCR(client,position_side,input,quantity_precision)
    except ClientError as error:
        print ('='*100)
        logging.error(
            "Found an error ===> STATUS = '{}', ERROR CODE = '{}', ERROR MESSAGE = '{}'".format(
                error.status_code, error.error_code, error.error_message
            )
        )
        print ('='*100)
        print(error)
        print ('='*100)
        market_order_response = None
    
    if market_order_response:
        order_id = market_order_response['orderId']
        
        print ('\n\n\n')
        print('MARKET ORDER PLACED SUCCESSFULLY =\n',market_order_response)
        
        max_tries = 10
        
        for attempt in range(max_tries):
            avg_fill_price, all_ord_stat = FETCH_ORDER_FILL_PRICE(client, input[0], order_id,avg_fill_price, all_ord_stat)
            
            
            if avg_fill_price and all_ord_stat == 'FILLED':
                sl_response = FALLBACK_PLACE_STOP_LOSS(client, input, position_side, avg_fill_price, sl_distance=50)
                print ('\nTHE FALLBACK STOP LOSS HAS BEEN PLACED = \n',sl_response)
                sl_response_id = sl_response['orderId']
                break
            else:
                print(f"Attempt {attempt + 1} failed to retrieve the fill price. = ",avg_fill_price,all_ord_stat)
            
            if attempt == max_tries - 1:
                print("\nMax retries reached. Failed to retrieve the fill price.\nOrder may still be pending without being cancelled.\n\n")
            
            time.sleep(5)
    else:
        print("ERROR in placing the MARKET ORDER = ",market_order_response)
    
    return market_order_response, avg_fill_price, all_ord_stat, sl_response_id