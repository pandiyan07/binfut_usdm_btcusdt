import logging
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.DEBUG)



def NEW_ODR_PLCR(client,pos_side,input,quantity_precision):
    
    rounded_qty = round(input[2], quantity_precision)
    
    order_response = client.new_order(
        symbol=input[0],
        side=pos_side, 
        type=input[1],
        quantity=rounded_qty
        )
    
    return order_response



def UNWANTED_POSITION_CLOSER(client,input,quantity_precision,live_position,ids):
    
    #   CLOSING THE OPEN POSITIONS
    
    if live_position['positionAmt'] < 0:
        close_side = 'BUY'
    elif live_position['positionAmt'] > 0:
        close_side = 'SELL'
    
    try:
        close_order =  NEW_ODR_PLCR(client,close_side,input,quantity_precision)
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
        close_order = None

    if close_order:
        print('UNWANTED OPEN POSITIONS HAS BEEN CLOSED = \n',close_order)
    else:
        print('UNWANTED OPEN POSITIONS NOT CLOSED = ',close_order)
    
    
    
    
    #   CANCELLING THE OPEN ORDERS
    try:
        all_orders = client.get_all_orders(symbol=live_position['symbol'])
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
    
    if all_orders and ids:
        for id in ids:
            for order in all_orders:    
                if id == order['orderId']:
                    if order['status'] == 'NEW':
                        try:
                            client.cancel_order(symbol=input[0], orderId=id)
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
    else:
        print('UNWANTED_POSITION_CLOSER = ',all_orders,'NO RESPONSE FROM all_orders & ids maplaaaaaaaaaaaaaaaaaaaa = \n\n', ids)
    
    # get the list of unfilled open orders with the 
                        