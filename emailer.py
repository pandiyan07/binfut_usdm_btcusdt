from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from datetime import datetime
from email import encoders
import pandas as pd
import smtplib
import time
import traceback
import logging
import os

# Configure the logging
log_file = "binfut_trading_bot.log"  # Define the log file name
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),  # Log to a file
        logging.StreamHandler()  # Log to the console (terminal)
    ]
)

# Create a logger instance
logger = logging.getLogger()
# Get the absolute path of the log file
log_file_path = os.path.abspath(log_file)

error_file = 'error_log.txt'
error_file_path = os.path.abspath(error_file)



# Function to send an email with a text file attachment
def EMAIL_SENDER(status,argument):
    # Create the email object
    msg = MIMEMultipart()
    current_time = datetime.now()
    
    if status == 'ORDER PLACED':
        subject = f"OPENED A ORDER"
        body = f"{argument} open order placed at = {current_time.strftime('%Y-%m-%d')} at  {current_time.strftime('%H:%M:%S')}" 
        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))
    
    if status == 'ORDER CLOSED':
        subject = f"CLOSED A ORDER"
        body = f"{argument} close order placed at = {current_time.strftime('%Y-%m-%d')} at  {current_time.strftime('%H:%M:%S')}" 
        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))
        
    if status == 'ERROR':
        subject = "ERROR WHILE RUNNING THE RENDER TRADING BOT"
        body = f"This Error popped up on {current_time.strftime('%Y-%m-%d')} at {current_time.strftime('%H:%M:%S')} = <br> {argument}"
        body2 = f"Please find the attached trading bot log file located at = {log_file_path}"
        # Attach the body text
        msg.attach(MIMEText(f"{body} <br><br> {body2}", 'plain'))
        
        # Attach the log files
        with open(log_file_path, "rb") as attachment1:
            part1 = MIMEBase('application', 'octet-stream')
            part1.set_payload((attachment1).read())
            encoders.encode_base64(part1)
            part1.add_header('Content-Disposition', f"attachment1; filename= {os.path.basename(log_file_path)}")
            msg.attach(part1)
        with open(error_file_path, "rb") as attachment2:
            part2 = MIMEBase('application', 'octet-stream')
            part2.set_payload(attachment2.read())
            encoders.encode_base64(part2)
            part2.add_header('Content-Disposition', f"attachment2; filename= {os.path.basename(error_file_path)}")
            msg.attach(part2)
    
    if status == 'START':
        import requests

        def get_public_ip():
            try:
                response = requests.get('https://api.ipify.org?format=json')
                response.raise_for_status()  # Check if request was successful
                ip = response.json().get('ip')
                return ip
            except requests.RequestException as e:
                print(f"Error fetching IP address: {e}")
                return None

        # Usage
        my_ip = get_public_ip()
        if my_ip:
            print("Your public current IP address is = ", my_ip)
        else:
            print("Could not retrieve my current IP address = ", my_ip)
        
        subject = "TRADING PYTHON BOT IN RENDER HAS STARTED RUNNING"
        body = f"{my_ip} = Program has started running on {current_time.strftime('%Y-%m-%d')} at  {current_time.strftime('%H:%M:%S')}" 
        # Attach the body text
        msg.attach(MIMEText(body, 'plain'))
    
    if status == 'DUMP':
        subject = "PANDIYAN'S DAILY RENDER TRADING REPORT"
        body = "Please find the attached trading report for today's session as well as the table below."
        trade_log_df = argument
        # Convert DataFrame to HTML and attach it in the body
        html_table = trade_log_df.to_html(index=False)  # Convert DataFrame to HTML format (without index)
        body_with_table = f"{body} <br><br> {html_table}"
        # Attach the HTML-formatted DataFrame in the email body
        msg.attach(MIMEText(body_with_table, 'html'))

        # Create a text file (or use an existing file)
        excel_file = "daily_report.xlsx"
        trade_log_df.to_excel(excel_file, index=False)  # Save DataFrame as CSV

        # Open the file to attach
        with open(excel_file, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename= {excel_file}")
            msg.attach(part)
    
    
    sender_email = "becool.pandiyan@gmail.com"
    sender_password = "bymthsinqckstzod" 
    receiver_email = [sender_email] #["nithyananth3377@gmail.com", sender_email] 

    msg['From'] = sender_email
    msg['To'] = ", ".join(receiver_email)
    msg['Subject'] = subject
    
    # Connect to the Gmail SMTP server and send the email
    
    server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server
    server.starttls()
    server.login(sender_email, sender_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_email, text)
    logger.info(f"EMAIL SENT = to {receiver_email} at {current_time}, with the email's subject as follows =")
    logger.info(subject)
    server.quit()



def DATA_DUMPER(position_side,trade_log_df,no_of_trade):
    try:
        if position_side == None:
            EMAIL_SENDER("DUMP",trade_log_df)
            trade_log_df = pd.DataFrame()
            no_of_trade = 0
        logger.info(f'{position_side} Since the TODAYS TRADING REPORT EMAIL has been sent, exiting the DATA_DUMPER() function')
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        line_number = tb[-1].lineno
        with open("error_log.txt", "w") as f:
            f.write(f"Error in DATA_DUMPER() function")
            f.write(f"Error occurred on line: {line_number}")
            f.write('\n')
            f.write(f"An error occurred: {e}")
            f.write('\n\n')
            traceback.print_exc(file=f)
        EMAIL_SENDER('ERROR',e)



if __name__ == "__main__":
    logger.warning(f'\n\nThis is just a support file which has some extra code.\n Run the main file = main.py')
