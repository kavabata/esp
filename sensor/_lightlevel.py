from machine import Pin, ADC
import config
from graphqlclient import send_sensor_value

light = None;

def init():
  if int(config.get_value('sensor_lightlevel')) > 0: 
    light = ADC(config.get_value('sensor_lightlevel_pin'))

def run(t):
  send_sensor_value("lightlevel", light.read())

