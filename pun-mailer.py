#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 20:55:53 2017

@author: alanspringfield
"""

from multiprocessing import Process
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
from os import environ
import requests
import re
import html
import sys

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException:
            print("An error has occured. This process has crashed.")
    return wrapper
    
def get_pun():
    raw = requests.get("http://www.punoftheday.com/cgi-bin/arandompun.pl").text
    pun = re.search(r"&quot;(.+)&quot;", raw).group(1)
    return html.unescape(pun) + "\n\n© 1996-2017 http://www.punoftheday.com"

@handle_exception
def send_mail():
    user = environ.get("EMAIL")
    password = environ.get("PASSWORD")
    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        target = "atran@aic.ac.nz"
    
    msg = EmailMessage()
    msg.set_content(get_pun())
    msg['Subject'] = "Pun of the Day"
    
    conn = smtplib.SMTP('smtp.gmail.com', 587)
    conn.ehlo()
    conn.starttls()
    conn.login(user, password)
    conn.send_message(msg, user, target)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    send_mail()
#    for i in range(5):
#        Process(target=send_mail).start()