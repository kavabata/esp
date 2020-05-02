import wifi
import oled
import dhtlocal
import pir
import config
import machine
import graphqlclient


oled.console('Run')
wifi.get_connection()
graphqlclient.send_config_value('ip', wifi.ifconfig())

cnt = 0
run_pir = int(config.get_value('sensor_pir')) > 0
run_dht = int(config.get_value('sensor_dht')) > 0

if run_pir:
  pir.init()

def dhtRunEveryTime(timer):
  global cnt
  oled.console(str(cnt))

  if run_pir:
    pir.runWhileLight()

  if run_dht:
    dhtlocal.runWhile()

  cnt = cnt + 1

t2 = machine.Timer(2)
# t2.init(period=dhtlocal.newtimer(1, 'hour'), mode=t2.PERIODIC, callback=dhtRunEveryTime)

if run_pir:
  def pirC(timer):
    pir.runWhilePir()

  t3 = machine.Timer(3)
  t3.init(period=100, mode=t3.PERIODIC, callback=pirC)
  

