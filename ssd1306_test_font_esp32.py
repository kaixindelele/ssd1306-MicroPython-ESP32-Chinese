import time
from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块
i2c = I2C(sda=Pin(5), scl=Pin(4))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

# 如果是"GB2312-12.fon"字体的话，有些字体设置，会直接丢失中文部分，即只能显示8*8字体的中文；
oled.font_load("GB2312-12.fon")
for i in range(4):
    oled.fill(0)
    oled.font_set(0x24,i,1,0)
    oled.text("中文显示",0,16,1)
    oled.show()
    time.sleep(1)
    oled.fill(0)
    oled.font_set(0x24,i,1,1)
    oled.text("中文显示",0,16,1)
    oled.show()
    time.sleep(1)
for count in range(10):
    oled.fill(0)
    oled.font_set(0x11,0,1,0)
    oled.text("micro中文迤=%d"%count,0,0,1)
    oled.font_set(0x31,0,1,0)
    oled.text("micro中文迤=%d"%count,0,13,1)
    oled.text("micro中文迤=%d"%count,0,26,1)
    oled.font_set(0x41,0,1,0)
    oled.text("micro中文迤=%d"%count,0,39,1)
    oled.text("micro中文迤=%d"%count,0,51,1)
    oled.show()
for count in range(10):
    oled.fill(0)
    oled.font_set(0x12,0,1,0)
    oled.text("MicRo中文=%d"%count,0,0,1)
    oled.font_set(0x22,0,1,0)
    oled.text("MicRo中文=%d"%count,0,16,1)
    oled.font_set(0x32,0,1,0)
    oled.text("MicRo中文=%d"%count,0,32,1)
    oled.font_set(0x42,0,1,0)
    oled.text("micro中文=%d"%count,0,48,1)
    oled.show()
oled.save_bmp("b.bmp")
for count in range(10):
    oled.fill(0)
    oled.font_set(0x13,0,1,0)
    oled.text("MRo中文=%d"%count,0,0,1)
    oled.font_set(0x33,0,1,0)
    oled.text("MRo中文=%d"%count,0,32,1)
    oled.show()
for count in range(10):
    oled.fill(0)
    oled.font_set(0x14,0,1,0)
    oled.text("MR文=%d"%count,0,0,1)
    oled.font_set(0x34,0,1,0)
    oled.text("Mo中=%d"%count,0,32,1)
    oled.show()
for count in range(65):
    oled.fill(0)
    oled.show_bmp("logo-1.bmp",count*3-64,count*2-64)
    oled.show()
for count in range(65):
    oled.fill(0)
    oled.show_bmp("logo-1.bmp",count*3-64,0)
    oled.show()
for count in range(65):
    oled.fill(0)
    oled.show_bmp("logo-1.bmp",32,count*2-64)
    oled.show()

