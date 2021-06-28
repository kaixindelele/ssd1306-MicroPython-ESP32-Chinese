'''
实验名称：【我的学习系统】之OLED中文显示（I2C总线）
版本：v1.0
日期：2021.6.5
作者：kaixindelele
'''

from machine import SoftI2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块


class OLED_Show:
    def __init__(self, sda_pin=18, scl_pin=23):        
        # 初始化I2C，设定好端口
        self.i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c
        self.oled = SSD1306_I2C(128, 64, self.i2c, addr=0x3c)
        # 导入字库
        self.oled.font_load("GB2312-32.fon")
        self.init_display()

    def init_display(self,):
        # 标题
        self.oled.text("我的学习系统?", 0,  0)
        # 标题和正文的分割线
        self.oled.line(0, 14, 128, 14, 1)        
        # 正文1-3
        self.oled.text("手机已使用时间:3H25M",  0, 16)
        self.oled.text("本次剩余时间:0H21M",  0, 30)
        self.oled.text("一定要好好学习啊!",  0, 44)
        # OLED执行显示
        self.oled.show()


def main():
    oled_show = OLED_Show()


if __name__=="__main__":
    main()
