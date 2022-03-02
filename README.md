# ssd1306OLED显示屏-MicroPython-ESP32-中文显示-利用GB2312字库（非手动取模）

## 前言：

！！！没有刷固件，是没有load_font()函数的！！！

！！！没有刷固件，是没有load_font()函数的！！！

！！！没有刷固件，是没有load_font()函数的！！！

阿这，为了让这个十几块的OLED显示中文，我可真的是付出了太多。
百度搜不到一个靠谱的教程，昨天晚上搜了一谷歌，终于找到了一个大佬17年的博客，[uPyCraft IDE-micropython支持中文啦！](https://mc.dfrobot.com.cn/thread-26740-1-1.html)

坏消息是：里面也没有一个step by step 的步骤~

好消息是：里面有一个micropython的群号-619558168；

我随即加了群；

好消息是：里面有很多成功显示中文的视频

坏消息是：里面固件文件和python脚本太多，我根本不知道用哪一个，而且没有找到一个保姆级的教程；

然后我问了群里的大佬，大佬告诉我下载这样的一个文件：
`fb增强固件及字库.rar`的文件。

好消息是：我会刷固件

坏消息是：我不知道该怎么把笔记本上的文件，上传字体到ESP32中，以及该怎么在python脚本中导入字库，并且显示出来。

于是接下来就是step by step 的教程了。

## 1. 安装好thonny和基本操作：
参考教程：[安装 Thonny 软件环境开发PI Pico](https://blog.csdn.net/zhuoqingjoking97298/article/details/114064833)

把其中的PI Pico换成ESP32就可以了。

## 2. 刷固件：
官方的固件，直接在官方网站上下载就可以了，但是官方的功能有点少，所以我们以这次可以中文显示的固件为例。

1. 插上USB，确认esp32板子的LED闪烁；
2. 点一下 `stop/restart` 按键，确保得到下面的效果，如果一直是横线，可以将鼠标点到横线下方，摁一下`enter`按键；出现`>>>`字符，说明连接正常。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210605151738611.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaGVkYWRhcQ==,size_16,color_FFFFFF,t_70)
3. 点击`tools`，会进入 `Thonny options`界面，选择`interpreter`，选好设备`ESP32`，选好端口 `COM5`。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210605152100497.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaGVkYWRhcQ==,size_16,color_FFFFFF,t_70)
4. 最后选择要刷的固件，如果你是4M的ESP32，那就选择`esp32_1.15_fb_boost_4M_ULAB.bin`，其他关于flash什么的，默认的就行。每次刷固件，之前存到esp32中的脚本文件都会被清空，这个一定要做好备份！
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210605154510702.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaGVkYWRhcQ==,size_16,color_FFFFFF,t_70)

## 3. Windows10笔记本上传字体到MicroPython设备中：
1. 点击`View`，选择`files`，左侧栏会出现下图，上面是`This computer`，下面是`MicroPython device`，选中要上传的文件，选择`upload`，即可上传到esp32中。
2. 这种方法比什么花里胡哨的 `ampy --port COM5 put GB2312-12.fon`靠谱多了，这个需要先`pip install adafruit-ampy`，然后上传文件，还看不到进度条，上传这种稍微大点的文件不知道啥时候能传完~
![在这里插入图片描述](https://img-blog.csdnimg.cn/20210605160556148.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaGVkYWRhcQ==,size_16,color_FFFFFF,t_70)


## 4. 示例python脚本：
### 4.1. ssd1306.py脚本代码：

```python
# MicroPython SSD1306 OLED driver, I2C and SPI interfaces

from micropython import const
import framebuf


# register definitions
SET_CONTRAST = const(0x81)
SET_ENTIRE_ON = const(0xA4)
SET_NORM_INV = const(0xA6)
SET_DISP = const(0xAE)
SET_MEM_ADDR = const(0x20)
SET_COL_ADDR = const(0x21)
SET_PAGE_ADDR = const(0x22)
SET_DISP_START_LINE = const(0x40)
SET_SEG_REMAP = const(0xA0)
SET_MUX_RATIO = const(0xA8)
SET_COM_OUT_DIR = const(0xC0)
SET_DISP_OFFSET = const(0xD3)
SET_COM_PIN_CFG = const(0xDA)
SET_DISP_CLK_DIV = const(0xD5)
SET_PRECHARGE = const(0xD9)
SET_VCOM_DESEL = const(0xDB)
SET_CHARGE_PUMP = const(0x8D)

# Subclassing FrameBuffer provides support for graphics primitives
# http://docs.micropython.org/en/latest/pyboard/library/framebuf.html
class SSD1306(framebuf.FrameBuffer):
    def __init__(self, width, height, external_vcc):
        self.width = width
        self.height = height
        self.external_vcc = external_vcc
        self.pages = self.height // 8
        self.buffer = bytearray(self.pages * self.width)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_VLSB, self.width)
        self.init_display()

    def init_display(self):
        for cmd in (
            SET_DISP | 0x00,  # off
            # address setting
            SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            SET_DISP_START_LINE | 0x00,
            SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            SET_MUX_RATIO,
            self.height - 1,
            SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            SET_DISP_OFFSET,
            0x00,
            SET_COM_PIN_CFG,
            0x02 if self.width > 2 * self.height else 0x12,
            # timing and driving scheme
            SET_DISP_CLK_DIV,
            0x80,
            SET_PRECHARGE,
            0x22 if self.external_vcc else 0xF1,
            SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            SET_CONTRAST,
            0xFF,  # maximum
            SET_ENTIRE_ON,  # output follows RAM contents
            SET_NORM_INV,  # not inverted
            # charge pump
            SET_CHARGE_PUMP,
            0x10 if self.external_vcc else 0x14,
            SET_DISP | 0x01,
        ):  # on
            self.write_cmd(cmd)
        self.fill(0)
        self.show()

    def poweroff(self):
        self.write_cmd(SET_DISP | 0x00)

    def poweron(self):
        self.write_cmd(SET_DISP | 0x01)

    def contrast(self, contrast):
        self.write_cmd(SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(SET_NORM_INV | (invert & 1))

    def show(self):
        x0 = 0
        x1 = self.width - 1
        if self.width == 64:
            # displays with width of 64 pixels are shifted by 32
            x0 += 32
            x1 += 32
        self.write_cmd(SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)


class SSD1306_I2C(SSD1306):
    def __init__(self, width, height, i2c, addr=0x3C, external_vcc=False):
        self.i2c = i2c
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.temp[0] = 0x80  # Co=1, D/C#=0
        self.temp[1] = cmd
        self.i2c.writeto(self.addr, self.temp)

    def write_data(self, buf):
        self.write_list[1] = buf
        self.i2c.writevto(self.addr, self.write_list)


class SSD1306_SPI(SSD1306):
    def __init__(self, width, height, spi, dc, res, cs, external_vcc=False):
        self.rate = 10 * 1024 * 1024
        dc.init(dc.OUT, value=0)
        res.init(res.OUT, value=0)
        cs.init(cs.OUT, value=1)
        self.spi = spi
        self.dc = dc
        self.res = res
        self.cs = cs
        import time

        self.res(1)
        time.sleep_ms(1)
        self.res(0)
        time.sleep_ms(10)
        self.res(1)
        super().__init__(width, height, external_vcc)

    def write_cmd(self, cmd):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.spi.init(baudrate=self.rate, polarity=0, phase=0)
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(buf)
        self.cs(1)

```

### 4.2. OLED_show.py脚本代码：

```python
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


```

### 4.3. OLED_class.py脚本代码：
```
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
```
这个可以将显示封装成类了，可以针对性的显示一行，选择居中或者左对齐，这样就能轻松定制一个显示界面。

## 5. 显示效果：
图中的`中文`显示非常舒服~
当然还有一些字体大小的设置，没调好，但是这个不重要了~
![在这里插入图片描述](https://img-blog.csdnimg.cn/2021060516133057.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2hlaGVkYWRhcQ==,size_16,color_FFFFFF,t_70)
## 6. 代码和资源
[https://github.com/kaixindelele/ssd1306-MicroPython-ESP32-Chinese/](https://github.com/kaixindelele/ssd1306-MicroPython-ESP32-Chinese/)
欢迎给个star~
