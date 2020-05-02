import wifi
import oled
import dhtlocal
import pir
import config
import machine


oled.console('Run')
wifi.get_connection()
wifi.send_config()

cnt = 0

def dhtRunEveryTime(timer):
  global cnt
  oled.console(str(cnt))
  dhtlocal.runWhile()
  pir.runWhileLight()
  cnt = cnt + 1

t2 = machine.Timer(2)
t2.init(period=dhtlocal.newtimer(1, 'hour'), mode=t2.PERIODIC, callback=dhtRunEveryTime)

if int(config.get_value('pir')) > 0:
  def pirC(timer):
    pir.runWhilePir()

  t3 = machine.Timer(3)
  t3.init(period=100, mode=t3.PERIODIC, callback=pirC)
  

