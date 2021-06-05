'''
实验名称：【我的学习系统】之OLED中文显示（I2C总线）
版本：v1.0
日期：2021.6.5
作者：kaixindelele
'''

from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块


i2c = I2C(sda=Pin(5), scl=Pin(4))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

oled.font_load("GB2312-12.fon")
oled.fill(0)
help(oled.font_set)


oled.text("我的学习系统", 0,  0)      #写入第1行内容
oled.line(0, 14, 128, 14, 1)
oled.text("手机已使用时间:3H25M",  0, 16)      #写入第2行内容

oled.text("本次剩余时间:0H21M",  0, 30)      #写入第3行内容

oled.text("一定要好好学习啊!",  0, 44)

oled.show()   #OLED执行显示

