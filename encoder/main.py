import config
import wifi
import time
import graphqlclient
import esp
from machine import Pin, ADC, PWM
import ure
import sys
import math
import network
import neopixel
try:
  import usocket as socket
except:
  import socket
from rotary_irq_esp import RotaryIRQ
import gc
gc.collect()

# global controllers properties
controllers = {
  'switch': {
    'url': 'http://192.168.1.187/switch/value/1000',
    'state': 15,
    'max': 100,
    'min': 0,
    'multiplier': 5
  }, 
  'switch2': {
    'url': 'http://192.168.1.187/switch2/value/1000',
    'state': 0,
    'max': 100,
    'min': 0,
    'multiplier': 2
  }
}
controller = None

wifi.get_connection()
addr = wifi.ifconfig()
config.write_conf('ip_address', addr)
graphqlclient.send_config_value('ip', addr)

led_cnt = 12
led_pin = 14
led = neopixel.NeoPixel(Pin(led_pin), led_cnt)

# 5, 4, 0 (d1, d2, d3)

rotary_last_state = 0
rotary_current_state = 0

button_pin = 0
SHORT_PRESS_TIME = 500
button = Pin(int(button_pin), Pin.IN)
button_last_state = 1
button_current_state = 1
button_pressed_time  = 0;
button_released_time = 0;

stopCycle = True;

def set_rotary():
  global rotary
  rotary = RotaryIRQ(pin_num_clk=5, 
    pin_num_dt=4,
    min_val=-100, 
    max_val=100,
    value=0,
    reverse=False, 
    range_mode=RotaryIRQ.RANGE_WRAP)


def loadLed():
  for x in range(0, led_cnt):
    led[x] = (2, 5, 1)
    led.write()
    time.sleep_ms(25)

  for x in range(0, led_cnt):
    led[x] = (0, 0, 0)
    led.write()
    time.sleep_ms(25)

def get_rotary():
  global rotary_last_state
  global controller
  global stopCycle

  rotary_current_state = rotary.value()
  
  if rotary_last_state != rotary_current_state:
    increment = rotary_current_state - rotary_last_state

    controller['state'] += increment * controller['multiplier']
    if (controller['state'] < controller['min']):
      controller['state'] = controller['min']
    
    elif(controller['state'] > controller['max']):
      controller['state'] = controller['max']
    
    print(rotary_last_state, rotary_current_state)
    rotary_last_state = rotary_current_state
    
    return True

  return False
  
def set_led():
  global stopCycle
  global controller

  controller_range = controller['max'] - controller['min']
  led_weight = controller_range / led_cnt
  full_led = math.floor(controller['state'] / led_weight)
  last_led = math.floor( (controller['state'] * 255) % math.floor(led_weight * 255) / led_weight)

  for x in range(0, led_cnt):
    if x < full_led:
      led[x] = (0, 255, 0)
    elif (x == full_led):
      led[x] = (1, last_led, 0)
    else:
      led[x] = (1, 0 , 0)
  
  led.write()

def set_url():

      

def init():
  global controller
  loadLed()

  set_rotary()
  controller = controllers['switch']

  while stopCycle:
    if get_rotary():
      set_led()
      set_url()


init()
