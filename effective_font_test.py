from ssd1306 import SSD1306_I2C     #从ssd1306模块中导入SSD1306_I2C子模块
import time

i2c = I2C(sda=Pin(5), scl=Pin(4))   #pyBoard I2C初始化：sda--> Y8, scl --> Y6
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c



oled.font_load("GB2312-32.fon")

for i in range(4):
    for j in range(5):
        oled.fill(0)
        oled.font_set(i*16 + 16 +j,0,1,0)
        # 中英文都显示的配置，j值越大字体越大；
        text_str = "MRo中文--"+str(i*10+j)
        
        print("text_str:", text_str)
        
        oled.text(text_str, 0, 17, 1)
        oled.show()
        time.sleep(0.6)
