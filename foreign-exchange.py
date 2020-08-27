#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 14:39:44 2020

@author: apple
"""

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime as dt
import schedule
import time



def main():
    
    baseurl = "https://www.usd-cny.com/bankofchina.htm"
    #import the site on which you search for information
    
    data = getData(baseurl)
    #get the exchange rate
    
    msg=sendMsg(data)+"https://www.kylc.com/huilv/d-boc-eur.html?datefrom=%s&dateto=%s"%((dt.datetime.now()-dt.timedelta(days=7)).strftime("%Y-%m-%d"),dt.datetime.now().strftime("%Y-%m-%d"))
    #edit the text of the mail
    #exchange rate + the link leads to 7-day line chart
    
    sendData(msg)
    
    
def askurl(url):

    head = {"User-Agent": "Mozilla/5.0 XXXXXXX"}
    #Copy the user-agent from "Request Headers"
    
    request=urllib.request.Request(url=url,headers=head)
    
    try:
        response=urllib.request.urlopen(request)
        html=response.read().decode("gbk")
        
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    
    return html


findLink=re.compile(r'<a href="(.*?)">')
findChange = re.compile(r'<td>(.*)</td>')



'''
Define a function to get the daily exchange rate between RMB and euro
and return the data
'''
def getData(baseurl)  :
    
    html=askurl(baseurl)
    soup = BeautifulSoup(html,"html.parser")
    
    for item in soup.find_all('tr'):
        
        item=str(item)
        Link = re.findall(findLink,item)
        
        if len(Link)>0 and Link[0] == "//www.usd-cny.com/eur-rmb.htm":
            Change=re.findall(findChange,item)
            if len(Change)>0:
                return Change[2]  #selling price
'''
Define a function to write an email everyday to send you the daily exchange rate and the link
'''
    
def sendData(msg):
    mailhost = 'smtp.gmail.com'
    gmail = smtplib.SMTP(mailhost)
    gmail.connect(mailhost,port=587)
    
    account = "YOUR EMAIL ADRESSE"
    password = "YOUR PASSWORD"
    
    gmail.ehlo()
    gmail.starttls()
    gmail.ehlo()
    gmail.login(account, password)
    receiver= "RECEIVER'S EMAIL ADRESSE"

    message = MIMEText(msg,'plain','utf-8')
    subject = "Daily exchange rate"
    message['Subject']=Header(subject,'utf-8')
    
    try:
        gmail.sendmail(account,receiver,message.as_string())
        print("sent")
    except :
        print("failed")
    gmail.quit()
    return True


def sendMsg(data):
    return "today's exchange rate is：%s\n"%data

    
if __name__ == "__main__":
    schedule.every().day.at("11:10").do(main)  #Send email everyday at 11:10
    while True:
        schedule.run_pending()
        time.sleep(1) 
