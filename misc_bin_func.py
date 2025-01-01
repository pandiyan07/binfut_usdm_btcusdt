from datetime import datetime, timedelta

import logging
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.DEBUG)

# 1. GET_ACCOUNT_BALANCE function
def GET_ACCOUNT_BALANCE(client):
    try:
        balance_info = client.balance()
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
        balance_info = None
    
    if balance_info:
        for balance in balance_info:
            if balance['asset'] == 'USDT':
                print(f"Remaining USDT Balance: {balance['balance']}")
                return balance['balance']
    else:
        print("ERROR RETRIEVING THE BALANCE = ",balance_info)
    
    


# 2. SET_LEVERAGE function
def SET_LEVERAGE(client,symbol,leverage):
    try:
        client.change_leverage(symbol=symbol, leverage=leverage)
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
    print('\n\n')
    print(f"Leverage set to {leverage}x for {symbol}")
    


# 3. SET_MARGIN_TYPE function
def SET_MARGIN_TYPE(client,symbol,type):
    try:
        client.change_margin_type(symbol=symbol, marginType=type)
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
    print(f"Margin type set to {type} for {symbol}")
    


# 4. GET_PRICE_PRECISION function
def GET_PRICE_PRECISION(client,input):
    try:
        exchange_info = client.exchange_info()  # Get all exchange information
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
        exchange_info = None
    
    if exchange_info:
        # Find the symbol-specific info from the exchange info
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == input[0]:
                price_precision = int(symbol_info['pricePrecision'])
                return price_precision
    else:
        print("ERROR RETRIEVING THE PRICE PRECISION = ",exchange_info)
    
    

# 5. GET_QUANTITY_PRECISION function
def GET_QUANTITY_PRECISION(client,input):
    try:
        exchange_info = client.exchange_info()  # Get all exchange information
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
        exchange_info = None
    
    if exchange_info:
        # Find the symbol-specific info from the exchange info
        for symbol_info in exchange_info['symbols']:
            if symbol_info['symbol'] == input[0]:
                quantity_precision = int(symbol_info['quantityPrecision'])
                return quantity_precision
    else:
        print("ERROR RETRIEVING THE QUANTITY PRECISION = ",exchange_info)
    


# 6. CHECK_POSITIONS function
def CHECK_FOR_ACTIVE_POSITIONS(client,symbol):
    try:
        positions = client.get_position_risk(symbol=symbol)
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
        positions = None
    
    if positions:
        for position in positions:
            if float(position['positionAmt']) != 0:
                #print("\n\n\nThe Open positions are = \n",position)
                return position
    else:
        print("ERROR RETRIEVING THE ACTIVE POSITIONS = ",positions)



def CHECK_ORDER_STATUS(client,symbol,ids, ids_name):
    all_orders_status_dict = {}
    a = 0
    
    if ids:
        #for id in ids:
        print(ids[a])
        print(type(ids[a]))
        try:
            order_status = client.get_orders(symbol=symbol, orderId=ids[a])     # or else use 'orderId=id' 
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
            order_status = None
        
        #print('id = ',id)
        if order_status:
            for os in order_status:
                print(f'THE SPECIFIC ORDER STATUS IS => orderId = {os['orderId']}, type = {os['type']}, Cumulative Margin = {os['cumQuote']}')
                print(f' origQty = {os['origQty']}, stopPrice = {os['stopPrice']}, updateTime = {os['updateTime']}')
        else:
            print(order_status,' a EMPTY LIST RESPONSE from the order_status variable maplaaaaaaaaaaaaaaaaaaaa = \n\n')
        
        try:
            all_orders = client.get_all_orders(symbol=symbol) 
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
            all_orders = None
        
        if all_orders:
            for id in ids:
                for order in all_orders:    
                    if id == order['orderId']:
                        print('\n',ids_name[a],'\nFOR THE ORDER ID = ',id,'THE all_orders ORDER STATUS IS = ',order['status']) 
                        print ('Dictionary items = ',a,ids_name[a],order['status'])
                        all_orders_status_dict.update({ids_name[a]: order['status']})
                        a+=1
        else:
            print(all_orders,'NO RESPONSE FROM all_orders maplaaaaaaaaaaaaaaaaaaaa = \n\n')
        
        print ('\nTHE DICTIONARY IS = \n',all_orders_status_dict)
        return all_orders_status_dict
    else:
        print (a,'\nNO ORDER ID TO CHECK THE STATUS OF THE ORDER = ',ids,'\n\n')
        return None


def FETCH_ORDER_FILL_PRICE(client, symbol, order_id,avg_fill_price, all_ord_stat):
    try:
        all_orders = client.get_all_orders(symbol=symbol)  # Fetch all orders for the symbol
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
        all_orders = None
    
    if all_orders:
        for order in all_orders:
            if order['orderId'] == order_id and order['status'] == 'FILLED':  # Find the specific order
                all_ord_stat = order['status']  
                avg_fill_price = float(order['avgPrice'])
                print('\nTHE ALL ORDER STATUS AND AVERAGE PRICE IS = \n', all_ord_stat, avg_fill_price)
        return avg_fill_price, all_ord_stat
    else:
        print('NO RESPONSE FROM all_orders maplaaaaaaaaaaaaaaaaaaaa = \n',all_orders)
        return None, None


def FETCH_ACCOUNT_TRADES(client,pd):
    try:
        acc_trades = client.get_account_trades(symbol="BTCUSDT")
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
        acc_trades = None
    
    
    
    if acc_trades:
        columns = ['symbol','maker', 'buyer', 'side', 'price', 'commissionAsset', 'qty', 'realizedPnl', 'commission', 'time']
        
        df = pd.DataFrame(acc_trades, columns=columns)
        
        df['time'] = pd.to_datetime(df['time'], unit='ms') + timedelta(hours=5, minutes=30)
        print(df[-20:])
        
        df['realizedPnl'] = pd.to_numeric(df['realizedPnl'])
        df['commission'] = pd.to_numeric(df['commission'])
        df = df[df['realizedPnl'] != 0]
        
        commission_list = df['commission'].tolist()
        realizedPnl_list = df['realizedPnl'].tolist()

        commission_sum = sum(commission_list)
        realizedPnl_sum = sum(realizedPnl_list)
        
        
        print(f"Commission Sum = {commission_sum}")
        print(f"Realized PnL Sum = {realizedPnl_sum}")
        print('Total profit = ',realizedPnl_sum - commission_sum)
        
        #   GET THE LEVERAGE DATA ALSO
        
        print ('\nlength of all the trades = ',len(acc_trades),'\n')
        
    else:
        print('ERROR WHILE FETCHING THE EXECUTED FUTURE TRADES FOR THIS BINANCE ACCOUNT = \n',acc_trades)
    
    return df