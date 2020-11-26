import config
import wifi
import time
import graphqlclient
from machine import Pin, ADC, PWM
import ure
import sys
import math
import network
try:
  import usocket as socket
except:
  import socket

import gc
gc.collect()

# global controllers properties
controllers = {
  'switch': {
    'state': 0,
    'enable': 1,
    'from': 0,
    'to': 0,
    'start': 0,
    'deadline': 0,
    'pwm': {}
  }, 
  'switch2': {
    'state': 0,
    'enable': 1,
    'from': 0,
    'to': 0,
    'start': 0,
    'deadline': 0,
    'pwm': {}
  }
}

if int(config.get_value('controller_switch')) > 0:
  switch = Pin(int(config.get_value('controller_switch_pin')), Pin.OUT)
  controllers['switch']['pwm'] = PWM(switch)
  controllers['switch']['pwm'].freq(300)
  print('PWM 1')
  
if int(config.get_value('controller_switch2')) > 0:
  switch2 = Pin(int(config.get_value('controller_switch2_pin')), Pin.OUT)
  controllers['switch2']['pwm'] = PWM(switch2)
  controllers['switch2']['pwm'].freq(1000)
  print('PWM 2')



def parse_request(r):
  request = ure.compile("[\r\n]").split(r)[0]
  urllist = ure.compile('\s').split(request)

  if len(urllist) > 1:
    url = urllist[1]
  else:
    url = '/test'

  cmdlist = url.split("/")

  controller = 'test'
  state = 0
  delay = 0

  if len(cmdlist) == 4:
    [n, controller, state, delay] = cmdlist

  if len(cmdlist) == 3:
    [n, controller, state] = cmdlist

  if len(cmdlist) == 2:
    [n, controller] = cmdlist

  return [controller, state, delay]

def set_controller(controller, state, delay):
  if controller == 'test':
    return 'Test Work'

  if controller in controllers:
    print(controllers[controller])
    if controllers[controller]['enable'] == 1:
      start = time.ticks_ms();
      controllers[controller]['from'] = controllers[controller]['state']
      controllers[controller]['to'] = int(state)
      controllers[controller]['start'] = start
      controllers[controller]['deadline'] = start + int(delay)
      return 'OK'
  else:
    return 'Not found Controller %s' % controller

def need_to_update():
  for cname in controllers:
    c = controllers[cname]
    if c['to'] != c['state']:
      return True
  return False

def update_controller():
  for cname in controllers:
    c = controllers[cname]
    if c['to'] != c['state']:
      timeleft = c['deadline'] - time.ticks_ms()
      print('timeleft', timeleft)

      if timeleft < 0:
        # timeout, set final value!!!
        save_controller_state(cname, c['to'])
      else:
        delay = c['deadline'] - c['start'] + 1
        timespent = delay - timeleft
        diff = c['to'] - c['from'];
        inc = math.ceil(diff * timespent / delay)
        
        # set new state!!!
        save_controller_state(cname, c['from'] + inc)

def save_controller_state(controller, state):
  v = math.floor(state * 1024 / 100)
  controllers[controller]['pwm'].duty(v)
  controllers[controller]['state'] = state
  graphqlclient.send_controller_value(controller, state)
  
def init():
  wifi.get_connection()
  addr = wifi.ifconfig()
  config.set_value('ip_address', addr)
  graphqlclient.send_config_value('ip', addr)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((addr, 80))
  s.listen(5)
  print('listening on: ', addr)

  while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)

    print('Got a connection from %s' % str(addr))
    print('Content = %s' % request)

    [controller, state, delay] = parse_request(request)
    resp = set_controller(controller, state, delay)

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Connection: close\n\n')
    conn.sendall(controller)
    conn.close()

    while need_to_update():
      update_controller()

init()
