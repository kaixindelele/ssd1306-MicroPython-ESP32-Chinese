'''
实验名称：OLED显示屏（I2C总线）
版本：v1.0
日期：2019.4
作者：01Studio
'''

from machine import I2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块

i2c = I2C(sda=Pin(5), scl=Pin(4))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

oled.font_load("GB2312-12.fon")
oled.fill(0)

for i in range(4):
#     oled.font_set(0x24, i, 1, 0)
    oled.text("Hello World!", 0,  0)      #写入第1行内容
    oled.text("MicroPython",  0, 20)      #写入第2行内容
    oled.text("By 01Studio",  0, 30)      #写入第3行内容
    oled.text("中文",  0, 40)

    oled.show()   #OLED执行显示

