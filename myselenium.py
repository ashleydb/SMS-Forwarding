from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import time
import sys
import smtplib
from email.mime.text import MIMEText

# -------

# parameters for tuning
loop_time_seconds = 30
running = True
message_count = 0

# netgear credentials
url = "http://attwifimanager/index.html"
ng_username = "enter_router_username_here"
ng_password = "enter_router_password_here"

# email settings
subject = "SMS Message Received"
#body = "Here is your new message: "
sender = "me@add_an_email_address_here.com"
recipients = ["someone@add_an_email_address_here.com"]
email_password = "enter_email_password_here"

# -------

# function to send an email (from https://mailtrap.io/blog/python-send-email-gmail/#How-to-send-an-email-with-Python-via-Gmail-SMTP)
def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("[i] Email sent!")

# -------

# starting this script when the device boots, so do a quick pause so WiFi connects
print("[i] SMS Forwarder starting. Wait time (secs):", loop_time_seconds)
time.sleep(loop_time_seconds)

# initialize the browser driver
options = Options()
options.binary_location = "/usr/bin/firefox-esr"
driver = webdriver.Firefox(service =
    Service(executable_path = "/usr/local/bin/geckodriver"),
    options = options)

while running:
    # refresh the page
    driver.get(url)

    if driver.find_element("id", "user_name").is_displayed():
        # find username/email field and send the username itself to the input field
        driver.find_element("id", "user_name").send_keys(ng_username)
        # find password input field and insert password as well
        driver.find_element("id", "session_password").send_keys(ng_password)
        # click login button
        driver.find_element("id", "login_submit").click()
        # wait the ready state to be complete
        WebDriverWait(driver=driver, timeout=10).until(
            lambda x: x.execute_script("return document.readyState === 'complete'")
        )

    # check we are logged in and look for the SMS messages
    if driver.find_element("id", "sms_card").is_displayed():
        # scan for SMS messages
        driver.implicitly_wait(5)
        messages = driver.find_elements("class name", "message_short")
        _msg_count = len(messages)
        _new_msg_count = _msg_count - message_count
        if _msg_count != message_count:
            print("[+] New Messages Found:", _new_msg_count)
        message_count = _msg_count
        #print("[i] Total Messages Found:", message_count)

        if _new_msg_count > 0:
            # iterate over the messages and print them
            new_messages = messages[0:_new_msg_count]
            for message in new_messages:
                print(message.text)
                send_email(subject, message.text, sender, recipients, email_password)

    # wait some secs and loop again
    #print("[i] Wait time (secs):", loop_time_seconds)
    time.sleep(loop_time_seconds)

# something failed, so we're going to end now
driver.close()
sys.exit("[!] Exiting the code with sys.exit()!")
