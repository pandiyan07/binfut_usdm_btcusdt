import logging
from binance.lib.utils import config_logging
from binance.error import ClientError

config_logging(logging, logging.DEBUG)

# Function to place a trailing stop loss order
def TSL_APPLIER(client, input, side, activation_price, trailing_distance):
    try:
        tsl_response = client.new_order(
            symbol=input[0],
            side="SELL" if side == "BUY" else "BUY", 
            type="TRAILING_STOP_MARKET",
            quantity=input[2],
            #activationPrice=activation_price,
            callbackRate= 0.5  # Set the trailing percentage 
        )
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
        tsl_response = None
    return tsl_response


def TSL_ORDER_PLACER(input, position_side, tsl_order_id, tsl, client, entry_price):
    
    if position_side == "BUY":
        activation_price = entry_price + 20  # $20 profit for long
    else:
        activation_price = entry_price - 20  # $20 profit for short
    
    max_tries = 10
    
    for attempt in range(max_tries):
    # Step 5: Place updated TSL
        tsl_order = TSL_APPLIER(client,input,
            side = position_side,
            activation_price = activation_price,
            trailing_distance = tsl,
        )
        
        if tsl_order:
            print("\nTHE TRIALING SL ORDER HAS BEEN PLACED SUCCESSFULLY = \n", tsl_order)
            # Save the TSL order ID for future cancellation
            tsl_order_id = tsl_order['orderId'] if tsl_order else None
            print ('\nTHE TSL ORDER ID IS = ',tsl_order_id)
            break
        else:
            print("\n Attempt ",attempt + 1," has FAILED to place the TSL....!!!!!!!!!!!!!!!!!. = ",tsl_order_id)
        
    return tsl_order_id