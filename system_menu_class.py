'''
实验名称：【我的学习系统】之OLED中文显示（I2C总线）
版本：v1.0
日期：2021.6.5
作者：kaixindelele
'''

from machine import SoftI2C,Pin         #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块
import time


class OLED_Show:
    def __init__(self, sda_pin=18, scl_pin=23, width=128, height=64):        
        # 初始化I2C，设定好端口
        self.i2c = SoftI2C(sda=Pin(sda_pin), scl=Pin(scl_pin))
        #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c
        self.oled = SSD1306_I2C(width, height, self.i2c, addr=0x3c)
        self.width = width
        self.height = height
        # 导入字库
        self.oled.font_load("GB2312-32.fon")
        self.font_pixel_list = [8, 12, 16, 24, 32]
        self.cand_font = [16, 17, 18, 19, 20,
                          32, 33, 34, 35, 36,]
        self.x_occupy = 0
        self.y_occupy = 0
        self.lines = {}
        self.y_space = 4
        self.menu_pointer = 0
        self.last_pointer_list = [0, 1, 2]

    def main_menu(self,):
        title_str = '功能主菜单'
        for new_p in range(7):
            self.oled.fill(0)
            self.draw_title(title_str)
            self.draw_menu(new_p)
            self.oled.show()
            self.menu_pointer += 1
            time.sleep(1)
        for new_p in range(7):
            new_p = 6-new_p
            self.oled.fill(0)
            self.draw_title(title_str)
            self.draw_menu(new_p)
            self.oled.show()
            self.menu_pointer += 1
            time.sleep(1)


    def draw_menu(self, new_p):
        cand_list = ['选项1', '选项2', '选项3',
                     '选项4', '选项5', '选项6',
                     '选项7',
                    ]
        if new_p in self.last_pointer_list:
            self.menu_pointer = new_p
        elif new_p > max(self.last_pointer_list):
            self.last_pointer_list = self.last_pointer_list[1:]
            self.last_pointer_list.append(new_p)
            self.menu_pointer = new_p
        elif new_p < min(self.last_pointer_list):
            self.last_pointer_list = [new_p+i for i in range(3)]
            self.menu_pointer = new_p
        else:
            print("else!")
        print("self.menu_pointer", self.menu_pointer)
        print("self.last_pointer_list", self.last_pointer_list)
        
        # 显示当前的三行选项
        for i in range(len(self.last_pointer_list)):
            pre_str = ' ' + str(self.last_pointer_list[i]+1)+'.'
            if self.last_pointer_list[i] == self.menu_pointer:
                pre_str = '>' + str(self.last_pointer_list[i]+1)+'.'
            
            self.draw_line(cand_list[self.last_pointer_list[i]],
                           line_index=i,
                           pre_str=pre_str)
   
    def init_display(self,):
        self.oled.fill(0)
        for i in range(len(self.cand_font)):
            self.oled.fill(0)
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
            # OLED执行显示
            self.oled.show()
            time.sleep(1)

    def draw_title(self, title_str='主菜单', font_size=1):
        # 字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，
        # 第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
        title_font = [17, 18, 33, 34]
        font = title_font[font_size]
        font_pixel = self.font_pixel_list[title_font[font_size] % 16]
        # 对齐方式：0为居中，1为左对齐，2为右对齐        
        if len(title_str) * font_pixel < self.width:            
            x_pad = (self.width - len(title_str) * font_pixel)//2
        else:
            x_pad = 0
        self.oled.font_set(font,0,1,0)
        self.oled.text(title_str, x_pad,  0)
        
    def draw_line(self, text_str="你的系统",
                  
                  font_size=1,
                  align=1, line_index=1,
                  color=0,
                  pre_str='>'
                  ):
        # 字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，
        # 第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
        
        font = self.cand_font[font_size]
        # font
        font_index = font % 16
        print("font:", font, "font_index:", font_index, "font_size:", font_size)
        self.lines[line_index] = self.font_pixel_list[font_index]
        y_pad = 16
        for i in range(line_index):
            if i in self.lines.keys():
                y_pad += self.lines[i+1] + self.y_space
        
        # 对齐方式：0为居中，1为左对齐，2为右对齐        
        if align==0 and len(text_str) * self.font_pixel_list[font_index] < self.width:            
            x_pad = (self.width - len(text_str) * self.font_pixel_list[font_index])//2
        else:
            x_pad = 0
        self.oled.font_set(font,0,1,0)
        text_str = pre_str + text_str
        self.oled.text(text_str, x_pad,  y_pad)


def main():
    oled_show = OLED_Show()
    oled_show.main_menu()


if __name__=="__main__":
    main()





