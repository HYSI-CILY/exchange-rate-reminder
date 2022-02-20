#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 14:39:44 2020

@author: apple
"""

from datetime import datetime
from dotenv import load_dotenv, main
import os
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

from bs4 import BeautifulSoup
import re
import urllib.request,urllib.error
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime as dt
import schedule
import time


def getLink():
		res = "https://www.kylc.com/huilv/d-boc-eur.html?datefrom=%s&dateto=%s"%((dt.datetime.now()-dt.timedelta(days=7)).strftime("%Y-%m-%d"),dt.datetime.now().strftime("%Y-%m-%d"))
		return res
		
	
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

def getData()  :
		baseurl = "https://www.usd-cny.com/bankofchina.htm"
		
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
		
class InfluxClient:
	def __init__(self,url,token,org,bucket):
		self._url=url
		self._token=token
		self._org=org
		self._bucket=bucket
		self._client=influxdb_client.InfluxDBClient(url,token,org)
		

	def write_data(self,data,write_option):
		write_api = self._client.write_api(write_option)
		p = influxdb_client.Point("exchange_rate").field("rate",data)
		write_api.write(bucket=self._bucket,org=self._org,record=p)
		
	
		
if __name__ == "__main__":
	'''
	get the token, org, bucket from .env
	'''
	load_dotenv()
	token = "cRlyJedIExDykBTfz6VTj6HkpCVcI6swISglr-uPulB5tWOLrMLFmABU6WNoE9UV9U0OegHP86soL4mfNFQY1A=="
	#token = os.getenv('TOKEN')
	print(token)
	#org = os.getenv('ORG')
	org="nan"
	print(org)
	#bucket = os.getenv('BUCKET')
	bucket="nan"
	print(bucket)
	data = getData()
	print(data)
	url = "http://localhost:8086"
	
	client = influxdb_client.InfluxDBClient(url,token,org)
	write_api = client.write_api(SYNCHRONOUS)
	p = Point("exchange_rate").field("rate", data)
	write_api.write(bucket=bucket, org=org, record=p)
	
	print(getLink())
	print("ok send")
	
	query_api = client.query_api()
	query = ' from(bucket:"nan")\
	|> range(start: -3h)\
	|> filter(fn:(r) => r._measurement == "exchange_rate")\
	|> filter(fn:(r) => r._field == "rate" )'
	
	result = query_api.query(org=org,query=query)
	results = []
	for table in result:
		for record in table.records:
			results.append(record.get_value())
	print(results)
	

			
	
	
