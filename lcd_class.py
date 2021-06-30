'''
实验名称：【我的学习系统】之lcd中文显示（I2C总线）
版本：v1.0
日期：2021.6.5
作者：kaixindelele
'''

import time
from machine import Pin, SPI
from st7789 import ST7789


class LCD_Show:
    def __init__(self, sda_pin=5, scl_pin=4, width=240, height=120):        
        # 初始化SPI，设定好端口
        self.spi = SPI(2, baudrate=40000000, polarity=1, sck=Pin(18), mosi=Pin(23)) 
        # LCD显示屏初始化：240*120分辨率,LCD的SPI地址是0x3c
        self.lcd = ST7789(width=width, height=height, spi=self.spi, rst=Pin(05), dc=Pin(04),cs=None,
             rot=0, bgr=0, external_vcc=False)#横屏初始化
        self.width = width
        self.height = height
        # 导入字库
        self.lcd.font_load("GB2312-32.fon")
        self.font_pixel_list = [8, 12, 16, 24, 32]
#         self.cand_font = [16,17,18,19,20, 21, 32,33,34,35,36,48,49,50,51,52,64,65,66,67,68]
        self.cand_font = [16, 17, 18, 19, 20,
                          32, 33, 34, 35, 36,]

        self.x_occupy = 0
        self.y_occupy = 0
        self.lines = {}
        self.y_space = 4
        self.init_display()

    def init_display(self,):
        self.lcd.font_set(0x13,0,1,0)
        # 字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，
        # 第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
        # 标题        
        # self.lcd.text("我的学习系统", 0,  0, self.lcd.rgb(255, 0, 0))
        for i in range(len(self.cand_font)):
            self.lcd.fill(0)
            self.draw_line(font_size=i,
                           line_index=1)
            text_str = "my study system"
            self.draw_line(text_str=text_str,
                           font_size=i,
                           line_index=2)
            text_str = "font_size"+str(self.cand_font[i])
            self.draw_line(text_str=text_str,
                           font_size=i,
                           line_index=3)
            self.lcd.show()
            time.sleep(2)
#         # 标题和正文的分割线
#         self.lcd.line(0, 40, 240, 40, self.lcd.rgb(255, 255, 255))        
#         # 正文1-3
#         self.lcd.text("手机已使用时间:3H25M",  0, 16)
#         self.lcd.text("本次剩余时间:0H21M",  0, 30)
#         self.lcd.text("一定要好好学习啊!",  0, 44)
#         # lcd执行显示
#         self.lcd.show()
    
    def draw_line(self, text_str="我的学习系统",
                  font_size=1,
                  align=0, line_index=1,
                  color=0,
                  ):
        # 字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，
        # 第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
        
        font = self.cand_font[font_size]
        # font
        font_index = font % 16
        print("font:", font, "font_index:", font_index, "font_size:", font_size)
        self.lines[line_index] = self.font_pixel_list[font_index]
        y_pad = 0
        for i in range(line_index):
            if i in self.lines.keys():
                y_pad += self.lines[i+1] + self.y_space
        
        # 对齐方式：0为居中，1为左对齐，2为右对齐        
        if align==0 and len(text_str) * self.font_pixel_list[font_index] < self.width:            
            x_pad = (self.width - len(text_str) * self.font_pixel_list[font_index])//2
        else:
            x_pad = 0
        self.lcd.font_set(font,0,1,0)
        self.lcd.text(text_str, x_pad,  y_pad, self.lcd.rgb(255, 255, 255))
        
        

def main():
    lcd_show = LCD_Show()


if __name__=="__main__":
    main()
