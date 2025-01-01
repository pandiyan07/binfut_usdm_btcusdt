from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from pytz import utc
import sys
from binance.um_futures import UMFutures
import pandas as pd
import traceback

from data_fetcher import *
from emailer import *
from trading_journal import *
from indicator_calculation import *
from keeping_webapp_alive import *
from order_closer import *
from order_placer import *
from misc_bin_func import *
from trading_logic import *
from trading_rules import *
from tsl_setter import *


all_orders_status_dict = {}
ids = []
ids_name = []


binance_btcusdt_futures_app = Flask(__name__)
a = 0
action = None
df = pd.DataFrame()
trade_log_df = pd.DataFrame()
my_client = None
ohlc_data = None
logger = logging.getLogger()


pyramid_threshhold = 40
max_profit_price = 0
current_profit_made = 0
entry_price = 0
no_of_trade = 0
max_gap = 0
status = None
position = None
close_position = None
price_precision = None
quantity_precision = None
tsl_order_id = None
bal_amnt = None
Initital_trade_lock = None
market_order_response = None

Order_limiter = 0
sl_response_id = 0
close_side = None

# Load environment variables from .env file
load_dotenv()

# Access the Binance API keys
API_KEY = os.getenv("BINANCE_API_KEY")       
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")

# Sample check to confirm variables loaded correctly
if not API_KEY or not SECRET_KEY:
    raise ValueError("API keys not found. Please set them in the environment or .env file.")

client = UMFutures(API_KEY, SECRET_KEY)

# Initial 1 order with 50 usdt with 4 times leverage
# 10 pyramid orders with 10 usdt with 20 times leverage
input = ("BTCUSDT" ,"MARKET" ,0.002 ,90 ,70 ,'ISOLATED',5)


def ERROR_FLOWCHART(e):
    tb = traceback.extract_tb(e.__traceback__)
    line_number = tb[-1].lineno
    with open("error_log.txt", "w") as f:
        f.write(f"Error in TRADING_ALGO_BOT() function")
        f.write(f"Error occurred on line: {line_number}")
        f.write('\n')
        f.write(f"An error occurred: {e}")
        f.write('\n\n')
        traceback.print_exc(file=f)

def TRADING_ALGO_BOT():
    global Order_limiter, df, my_client, ohlc_data, order_status, status, position, action, Initital_trade_lock, max_profit_price, current_profit_made, max_gap, entry_price, no_of_trade, trade_log_df,market_order_response, quantity_precision, price_precision, tsl_order_id, sl_response_id, close_side, close_position, ids, ids_name, all_orders_status_dict

    try:
        if not df.empty:
            #   TRADE CONDITION CHECKING
            long_entry_condition, short_entry_condition, long_gap, short_gap, atr_value = CONDITION_VERIFIER(df)
            
            Order_limiter, action, status, position, max_profit_price, current_profit_made, entry_price, no_of_trade, max_gap, Initital_trade_lock, long_gap, short_gap, atr_value = TRADING_LOGIC(Order_limiter, df, action, status, long_entry_condition, short_entry_condition, pyramid_threshhold, max_profit_price, current_profit_made, entry_price, no_of_trade, max_gap, Initital_trade_lock, long_gap, short_gap, atr_value, position)
            print ('Order_limiter = ',Order_limiter)
            
            
            #   ORDER PLACEMENT
            if action == 'ENTER_TRADE':
                print('action == ENTER_TRADE')
                if position == 'LONG' or position == 'SHORT':
                    Initital_trade_lock = False     #   Change it to True to enable the PYRAMID ORDER PLACEMENT
                    
                market_order_response, avg_fill_price, all_ord_stat, sl_response_id = OPEN_ORDER_PLACER(input, client, price_precision, quantity_precision, status, position)
                
                if position == "LONG":
                    tsl = input[3]
                elif position == "SHORT":
                    tsl = input[4]
                
                if all_ord_stat == 'FILLED':
                    tsl_order_id = TSL_ORDER_PLACER(input, position, tsl_order_id, tsl, client, avg_fill_price)
                    action = 'POSITION_IS_LIVE'
                    EMAIL_SENDER("ORDER PLACED",position)
                
                ids.append(market_order_response['orderId'])
                ids_name.append('market_order_response_ID')
                ids.append(sl_response_id)
                ids_name.append('sl_response_ID')
                ids.append(tsl_order_id)
                ids_name.append('tsl_order_ID')
            
            
            if action == 'POSITION_IS_LIVE':
                print('action == POSITION_IS_LIVE')
                print ('='*130)
                print ('='*130)
                
                live_position = CHECK_FOR_ACTIVE_POSITIONS(client,input[0])
                if live_position:
                    print('AVAILABLE LIVE POSITIONS TO BE CLOSED ARE = \n',live_position,'\n')
                else:
                    print (live_position,' = NO LIVE POSITIONS TO BE CLOSED CURRENTLY, so setting the action to EXIT_TRADE')
                    action = 'EXIT_TRADE'
                
                print ('\nThe ids =\n',ids,'\nThe ids_name =\n',ids_name,'\n')
                all_orders_status_dict = CHECK_ORDER_STATUS(client, input[0], ids, ids_name)
                print ('='*130)
                print ('='*130)
                
                
            if action == 'EXIT_TRADE':
                print('action == EXIT_TRADE')
                
                if position == 'LONG' or position == 'SHORT':
                    Initital_trade_lock = False
                    close_position = position
                    position = None
                    print ('The close_position variable has been SET TO = ',close_position)
                
                if close_position == 'LONG':
                    close_side = 'SELL'
                elif close_position == 'SHORT':
                    close_side = 'BUY'
                
                if all_orders_status_dict['market_order_response_ID'] == 'FILLED':
                    print ('\n\nSINCE ITS A ',close_position,' POSITION, SO PLACING A ',close_side,' ORDER')
                    all_orders_status_dict = CLOSE_ORDER_PLACER(client, quantity_precision, tsl_order_id, input, sl_response_id, close_side, all_orders_status_dict, ids, ids_name)
                    EMAIL_SENDER("ORDER CLOSED",position)
                    
                    close_position = None
                    status = None
                    action = None
                    market_order_response = None
                    max_profit_price = 0
                    current_profit_made = 0
                    entry_price = 0
                    no_of_trade = 0
                    max_gap = 0
                    
                    all_orders_status_dict = {}
                    ids = []
                    ids_name = []
                else:
                    print ('Market order seems to be NOT FILLED, the MO order status is = ',all_orders_status_dict['market_order_response_ID'])
                
                
                trade_log_df = FETCH_ACCOUNT_TRADES(client,pd)
                
                i = 0
                while True:
                    i+=1
                    print('EXIT THE PROGRAM')
                    time.sleep(3)
                    if i > 10:
                        exit()
                    
            print('\n\nTRADING_ALGO_BOT has finished running, 1 minute over......',action)
        else:
            logger.info('df dataframe is still EMPTY')
    except Exception as e:
        logger.info(f"Error fetching data: {e}")
        #CLOSE_ALL_OPEN_ORDERS(client,input)
        ERROR_FLOWCHART(e)
        EMAIL_SENDER('ERROR',e)
        scheduler.shutdown()
        STOPPING_WEBSOCKET_STREAMING(my_client)
        sys.exit(1)


def SCHEDULED_TASKS():
    global df, bal_amnt
    try:
        logger.info ('SCHEDULED_TASKS   --->   RUNNING  SCHEDULED  PROGRAM')
        ohlc_data = CHOOSY_PICKY_DATA_FETCHER()
        df.drop(df.head(1).index, inplace=True)
        df = pd.concat([df, ohlc_data], ignore_index=True)
        df = INDICATOR_CALCULATOR( df, 13, 5, 34)
        #KEEPING_WEB_APP_ALIVE()
        TRADING_ALGO_BOT()
    except Exception as e:
        logger.info(f"Error fetching data: {e}")
        ERROR_FLOWCHART(e)
        EMAIL_SENDER('ERROR',e)
        scheduler.shutdown()
        STOPPING_WEBSOCKET_STREAMING(my_client)
        sys.exit(1)



scheduler = BackgroundScheduler(timezone=utc)
scheduler.add_job(SCHEDULED_TASKS, 'interval', seconds=30)
scheduler.add_job(DATA_DUMPER, 'cron', hour=12, minute=30, args=[position,trade_log_df,no_of_trade])


@binance_btcusdt_futures_app.route('/')
def HOME_PAGE():
    global a, df, my_client, ohlc_data, position,quantity_precision, price_precision, client, tsl_order_id, input, sl_response_id,close_side,all_orders_status_dict, ids, ids_name,trade_log_df
    if a==0:
        GET_ACCOUNT_BALANCE(client)
        
        
        my_client = WEBSOCKET_STREAMING_DATFET()
        EMAIL_SENDER("START",None)
        df = REST_API_DATFET()
        df = INDICATOR_CALCULATOR(df, 13, 5, 34)
        price_precision = GET_PRICE_PRECISION(client, input)
        quantity_precision = GET_QUANTITY_PRECISION(client, input)
        
        # Set leverage 
        SET_LEVERAGE(client,input[0],input[6])
        live_position = CHECK_FOR_ACTIVE_POSITIONS(client,input[0])
        if live_position:
            print('\n\n\nYES, there are a few positions alive = ',live_position)
            UNWANTED_POSITION_CLOSER(client,input,quantity_precision,live_position,ids)
            #close_order = CLOSE_ORDER_PLACER(client, quantity_precision, tsl_order_id, input, sl_response_id, close_side, all_orders_status_dict, ids, ids_name)
            #print('CLOSE ORDER PLACED FOR THE PRE-EXISTED ORDERS = \n',close_order)
        else:
            print (live_position,' = NO LIVE ORDERS AVAILABLE RIGHT NOW\n\n')
        scheduler.start()
        SCHEDULED_TASKS()
        trade_log_df = FETCH_ACCOUNT_TRADES(client,pd)
        
    
    a+=1
    if position == 'LONG' or position == 'SHORT':
        trading_status = "<h2>ENTERED A POSITION</h2>"
    else:
        trading_status = "<h2>NO LIVE POSITIONS CURRENTLY</h2>"
    
    print ('\nREFRESHED the pageeeeeeeeeeeeeeeee.............\n')      # trade_log_df
    
    if trade_log_df.empty:
        return render_template('btcusdt_binance_futures_dummy_homepage.html', message=trading_status)
    else:
        return render_template('btcusdt_binance_futures_homepage.html', tables=[trade_log_df.to_html(classes='data',index=False)], titles=trade_log_df.columns.values, message=trading_status) 





# Main loop
if __name__ == "__main__":
    try:
        binance_btcusdt_futures_app.run(host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        logger.info('SOME ERROR HAS OCCURED IN THE ================= binance_btcusdt_futures_app')
        scheduler.shutdown()
        STOPPING_WEBSOCKET_STREAMING(my_client)