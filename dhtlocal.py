import dht
from machine import Pin
from oled import showDht
import config
from graphqlclient import send_sensor_value

if config.get_value('sensor_dht') == '11':
  sensor = dht.DHT11(Pin(int(config.get_value('sensor_dht_pin')))) # d4 
else:
  sensor = dht.DHT22(Pin(int(config.get_value('sensor_dht_pin')))) # d4 

def sendDht(t, h):
  send_sensor_value("temperature", t)
  send_sensor_value("humidity", h)


def runWhile():
  try:
    sensor.measure()

    t = sensor.temperature()
    h = sensor.humidity()
    sendDht(t, h)
    showDht(t, h)

  except OSError as e:
    print('Failed to read sensor.')


# runWhile();
# def newtimer(x, type):
#   if type == 'minute':
#     return x * 60 * 1000;
#   else if type == 'hour':
#     return x * 60 * 60 * 1000;
#   else if type == 'day':
#     return x * 24 * 60 * 60 * 1000;
#   else:
#     return x