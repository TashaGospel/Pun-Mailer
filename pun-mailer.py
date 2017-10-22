#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 20:55:53 2017

@author: alanspringfield
"""

from multiprocessing import Process, Queue
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv, find_dotenv
from os import environ
import requests
import re
import html
import sys
import queue

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except BaseException:
            print("An error has occured. This process has crashed.")
    return wrapper
    
def get_pun():
    while True:
        try:
            raw = requests.get("http://www.punoftheday.com/cgi-bin/arandompun.pl").text
            pun = re.search(r"&quot;(.+)&quot;", raw).group(1)
            return html.unescape(pun) + "\n\n© 1996-2017 http://www.punoftheday.com"
        except AttributeError:
            pass

def connect_gmail(user, password):
    conn = smtplib.SMTP('smtp.gmail.com', 587)
#    conn.set_debuglevel(1)
    conn.ehlo()
    conn.starttls()
    conn.login(user, password)
    return conn

def take_job(q):
    try:
        q.get_nowait()
        return True
    except queue.Empty:
        return False

#@handle_exception
def send_pun(user, target, q):
    conn = connect_gmail(user, password)
    
    while take_job(q):
        msg = EmailMessage()
        pun = get_pun()
        print(pun)
        msg.set_content(pun)
        msg['Subject'] = "Pun of the Day"
        
        conn.send_message(msg, user, target)
        
    conn.quit()
    
if __name__ == '__main__':
    load_dotenv(find_dotenv())
    user = environ.get("EMAIL")
    password = environ.get("PASSWORD")
    
    target = user
    times = 1
    if len(sys.argv) >= 2:
        target = sys.argv[1]
    if len(sys.argv) >= 3:
        times = int(sys.argv[2])
        
    q = Queue()
    for i in range(times):
        q.put(i)
    
    for i in range(10):
        Process(target=send_pun, args=(user, target, q)).start()