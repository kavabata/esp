import config
import wifi
import dht
import graphqlclient
from machine import Pin, ADC
import time
import gc
gc.collect()

# I'm simple sensor with:
#   PIR - ?GPIO0;
#   DHT - ?GPIO2;
#   Light Level Sensor (LL) - ?ADO

# - my nickname is? it should be uniq
# config.write_conf('key', 'esp-sensor-1')


wifi.get_connection()
addr = wifi.ifconfig()
graphqlclient.send_config_value('ip', addr)
config.write_conf('ip_address', addr)


IS_DHT = int(config.get_value('sensor_dht')) > 0
DHT_T = ""
DHT_H = ""

if IS_DHT:
  if config.get_value('sensor_dht') == '11':
    sensor = dht.DHT11(Pin(int(config.get_value('sensor_dht_pin'))))
  else:
    sensor = dht.DHT22(Pin(int(config.get_value('sensor_dht_pin'))))


IS_LL = int(config.get_value('sensor_lightlevel')) > 0
LL = None
LLV = 0

if IS_LL:
  LL = ADC(config.get_value('sensor_lightlevel_pin'))



IS_PIR = int(config.get_value('sensor_pir')) > 0
PIR_S = 0
PIR = None

if IS_PIR:
  PIR = Pin(int(config.get_value('sensor_pir_pin')), Pin.IN) #13 d5
  newState = PIR.value()


while True:
  if IS_DHT:
    try:
      sensor.measure()
      t = sensor.temperature()
      h = sensor.humidity()
      if DHT_H != h:
        DHT_H = h
        graphqlclient.send_sensor_value("humidity", DHT_H)
        
      if DHT_T != t:
        DHT_T = t
        graphqlclient.send_sensor_value("temperature", DHT_T)

    except OSError as e:
      print('Failed to read DHT or send.')
      pass

  if IS_LL:
    try:
      l = LL.read()
      l = round(100 * l/1024)
      if l != LLV:
        LLV = l
        graphqlclient.send_sensor_value("lightlevel", LLV)

    except OSError as e:
      print('Failed to read LLV or send.')
      pass

  if IS_PIR:
    try:
      s = PIR.value()
      if PIR_S != s:
        PIR_S = s
        graphqlclient.send_sensor_value("pir", PIR_S)

    except OSError as e:
      print('Failed to read PIR or send.')
