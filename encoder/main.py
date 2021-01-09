import config
import wifi
import time
import utime
import graphqlclient
from machine import Pin, ADC, PWM
import math
import neopixel
from urequests import get
from rotary_irq_esp import RotaryIRQ
import gc
gc.collect()

wifi.get_connection()
addr = wifi.ifconfig()
config.write_conf('ip_address', addr)
graphqlclient.send_config_value('ip', addr)

stopCycle = True;

# 5, 4, 0 (d1, d2, d3)
rotary_last_state = 0
rotary_current_state = 0

def set_rotary():
  global rotary
  global rotary_last_state
  global rotary_current_state

  rotary = RotaryIRQ(pin_num_clk=5, 
    pin_num_dt=4,
    min_val=-100, 
    max_val=100,
    value=0,
    reverse=False, 
    range_mode=RotaryIRQ.RANGE_WRAP)

  rotary_last_state = 0
  rotary_current_state = 0


def get_rotary():
  global rotary_last_state
  global controller

  rotary_current_state = rotary.value()
  
  if rotary_last_state != rotary_current_state:
    increment = rotary_current_state - rotary_last_state

    controller['state'] += increment * controller['multiplier']
    if (controller['state'] < controller['min']):
      controller['state'] = controller['min']
    
    elif(controller['state'] > controller['max']):
      controller['state'] = controller['max']
    
    rotary_last_state = rotary_current_state

    return True

  return False

led_cnt = 12
led_pin = 14
led = neopixel.NeoPixel(Pin(led_pin), led_cnt)

def load_led():
  for x in range(0, led_cnt - 1):
    led[x] = (math.floor(255 / (x+1)), 20 * x, 0)
    led.write()
    time.sleep_ms(20)

  for x in range(0, led_cnt):
    led[x] = (0, 0, 0)
    led.write()
    time.sleep_ms(30)

def set_led():
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

button_pin = 0
SHORT_PRESS_TIME = 500
button = Pin(int(button_pin), Pin.IN)
button_last_state = 1
button_current_state = 1
button_pressed_time  = 0
button_released_time = 0

def get_button():
  global button_last_state
  global button_current_state
  global button_pressed_time
  global button_released_time

  button_current_state = button.value()

  if button_current_state != button_last_state:
    if button_last_state == 1: # start press
      button_pressed_time = utime.ticks_ms()
    else: # release
      button_released_time = utime.ticks_ms()

    button_last_state = button_current_state

  if button_pressed_time != 0 and button_released_time != 0:
      duration = button_released_time - button_pressed_time
      button_pressed_time  = 0
      button_released_time = 0
      return duration

  return 0

# global controllers properties
controllers = {}
controller = {}
controllers_current_key = 999

def get_controllers():
  global controllers
  a = graphqlclient.get_controlles()

  for c in range(0, len(a)):
    controllers[a[c]['url']] = {
      'url': a[c]['url'],
      'state': int(a[c]['state']),
      'max': int(a[c]['max']),
      'min': int(a[c]['min']),
      'multiplier': int(a[c]['multiplier'])
    }
  # print(controllers)

def set_next_controller():
  global controller
  global controllers_current_key

  controllers_keys = list(controllers.keys())
  if len(controllers_keys) == 0:
    time.sleep(10)
    get_controllers()
    set_next_controller()
    return False

  controllers_current_key += 1
  if controllers_current_key >= len(controllers_keys):
    controllers_current_key = 0

  controller = controllers[controllers_keys[controllers_current_key]]

  set_rotary()
  set_led()

def set_controller():
  try:
    get(controller['url'].replace('value', str(controller['state']), 1))
  except OSError as e:
    pass

def init():
  global stopCycle
  load_led()

  get_controllers()
  set_next_controller()

  while stopCycle:
    click = get_button()

    if click > SHORT_PRESS_TIME: #stop
      # stopCycle = False 
      get_controllers()
    elif click > 0: #next controller
      get_controllers()
      set_next_controller()

    if get_rotary():
      set_led()
      set_controller()


init()
