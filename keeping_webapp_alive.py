from datetime import datetime
import requests
import os

# URL of your web app
web_app_url = os.getenv("WEB_APP_URL", "https://binance-btcusdt.onrender.com/")

    
def KEEPING_WEB_APP_ALIVE():
    # Send a GET request to the web app URL
    response = requests.get(web_app_url)
    print(f"GET request sent on : {datetime.now()}")
    if response.status_code == 200:
        print("KEEPING_WEB_APP_ALIVE() : Successfully kept the web app alive.")
    else:
        print(f"KEEPING_WEB_APP_ALIVE() : Request returned a non-200 status code: {response.status_code}")
