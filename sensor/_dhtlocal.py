import dht
from machine import Pin
from oled import showDht
import config
from graphqlclient import send_sensor_value


def sendDht(t, h):
  send_sensor_value("temperature", t)
  send_sensor_value("humidity", h)


def runWhile(t):
  try:
    sensor.measure()
    t = sensor.temperature()
    h = sensor.humidity()
    print('runWhile to read sensor. %s' % t)
    sendDht(t, h)
    # showDht(t, h)

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