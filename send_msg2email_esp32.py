# -*- coding: utf-8 -*-
import umail
import time
import machine
from machine import Pin
import network
try:
  import usocket as socket
except:
  import socket
import esp
esp.osdebug(None)
import gc
gc.collect()

led = machine.Pin(2,machine.Pin.OUT)
io19 = Pin(19, Pin.IN) 
sent_flag = 0

#下面五个参数使用时修改成自己的，本例程中邮箱使用微软Hotmail邮箱，其他邮箱未经测试
wifi_ssid = "huining3F-03"					#本地wifi的ssid名称
wifi_password = '66666666'      #本地wifi的密码

myusername = 'reg520@hotmail.com'  #发送端邮箱地址
mypassword = 'gadgasdfdadgasg'           #发送端邮箱授权码！
target_email = '1976792544@qq.com'		#接收端邮箱地址

SMTP_SERVER   = 'smtp.office365.com'  #hotmail的smtp服务器地址
SMTP_SERVER_PORT   = 587                   #hotmail的smtp服务器端口

#连接本地wifi
def connect_wifi():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	if not wlan.isconnected(): 
		print("scaning......")       
		all_ssid=str(wlan.scan())
		if all_ssid.count(wifi_ssid)>0:
			print('connecting to:', wifi_ssid)   	
		else:
			print("not found AP")
		try:
			wlan.connect(wifi_ssid, wifi_password)
			time.sleep(3)
		except Exception as e:
			raise e
		if wlan.isconnected():
			pass  
		else:
			print("connect wlan fail!!!")
			while not wlan.isconnected():
				print("reconnect......")
				wlan.connect(wifi_ssid, wifi_password)
				if wlan.isconnected():
					pass  
				else:
					time.sleep(10)
	print('network config:', wlan.ifconfig())

def callback(p):
	global sent_flag
	if(io19.value()==1):
		time.sleep_ms(300)
		if(io19.value()==1):
			print("door open")
			led.value(1)
			sent_flag = 1

connect_wifi()
io19.irq(trigger=Pin.IRQ_RISING, handler=callback)
while(True):
	if(sent_flag == 1):
		try:
			smtp = umail.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
			smtp.login(myusername, mypassword)
			smtp.to(target_email)
			smtp.write("From: Devices<"+myusername+">\r\n")  #windows服务器不能单独识别\n  所以加上\r
			smtp.write("To: You<"+target_email+">\r\n")      #如果出现报错可以尝试把\r\n换成\n
			smtp.write("Subject: WARNING!!!\r\n\n")
			smtp.write("有内鬼终止交易.\r\n")
			smtp.send()
			smtp.quit()
			print("Email was sent successfully!")
			led.value(0)
			sent_flag = 0
		except Exception as e:
			print("ERROR!!!")
			raise e
	time.sleep_ms(10)
