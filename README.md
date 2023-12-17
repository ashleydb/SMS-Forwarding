# SMS-Forwarding

For scraping SMS messages sent to Netgear Nighthawk mobile routers and forwarding them as emails.

---
See myselenium.py for the final code.

These are some of the steps needed for setup:

## Browser and Driver Setup
We're using an OrangePi 3-LTS with Ubuntu 3.x.
This comes with Firefox as a "snap". That means it is located at:
  /usr/bin/firefox-esr

Get the Firefox WebDriver from:
  https://github.com/mozilla/geckodriver/releases
Get the linux-aarch64 version.

Extract it, then make it executable:
  sudo chmod +x geckodriver

Move the file to a folder within the $PATH, e.g.
  sudo mv geckodriver /usr/local/bin

## Email Sending Setup
For sending emails via GMail I needed an App Password from Google, which itself requires 2-Step Verification to be setup on the account.

## Credentials Setup
Be sure to update the script to add usernames, passwords, and email addresses at the top.

## Run Script on Boot
How to run the script at startup:
Applications --> Settings Manager --> System --> Session and Startup
Click + and add a job with a path to the script, e.g.
  Name: SMS Forwarder
  Description: Forwarding SMS messages from Netgear router to an email address
  Command: python3 /home/orangepi/Documents/SMS-Scraping/myselenium.py
  Trigger: On Login

## Restarting the OrangePi
Getting the device to reboot every day at 1:01am (1am, with a 70 sec sleep) using cron:

0 1 * * * sleep 70 && reboot

(This is how to configure the timing in cron: https://crontab.guru/every-day-at-1am)
