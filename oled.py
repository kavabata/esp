from machine import I2C, Pin
import ssd1306
import config

oled = None
is_oled = int(config.get_value('controller_oled')) > 0
oledcursor = 0

def init():
  if int(is_oled) > 0:
    i2c=I2C(scl=Pin(5),sda=Pin(4))
    i2c.scan()
    oled = ssd1306.SSD1306_I2C(128, 32, i2c)
    oled.fill(0)
    oled.show()



def hello():
  if int(is_oled) > 0:
    oled.fill(0)
    oled.text('HELLO',0,0)
    oled.show()

def showDht(t, h):
  if int(is_oled) > 0:
    print("printDht")
    print(t, h)
    oled.fill(0)

    oled.text('T:',0,0)
    oled.text(str(t),20,0)

    oled.text('H:',0,16)
    oled.text(str(h),20,16)

    oled.show()

def console(t):
  print(str(t))
  if int(is_oled) > 0:
    global oledcursor
    if oledcursor > 30:
      oled.fill(0)
      oledcursor = 0
    oled.text(t, 0, oledcursor)
    oled.show()
    oledcursor = oledcursor + 11
