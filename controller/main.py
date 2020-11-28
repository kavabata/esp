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
    'enable': int(config.get_value('controller_switch')) > 0,
    'from': 0,
    'to': 0,
    'start': 0,
    'deadline': 0,
    'pwm': {}
  }, 
  'switch2': {
    'state': 0,
    'enable': int(config.get_value('controller_switch2')) > 0,
    'from': 0,
    'to': 0,
    'start': 0,
    'deadline': 0,
    'pwm': {}
  }
}



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
    return 'AVAILABE'

  if controller in controllers:
    c = controllers[controller]

    if c['enable'] == 1:
      if state == 'get':
        return c['state']

      start = time.ticks_ms();
      c['from'] = c['state']
      c['to'] = int(state)
      c['start'] = start
      c['deadline'] = start + int(delay)
      return 'SET'

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
      # print('timeleft', timeleft)

      if timeleft <= 0:
        # timeout, set final value!!!
        save_controller_state(cname, c['to'])
      else:
        delay = c['deadline'] - c['start'] + 1
        timespent = delay - timeleft
        diff = c['to'] - c['from'];
        inc = math.ceil(diff * timespent / delay)
        
        # set new state!!!
        save_controller_state(cname, c['from'] + inc)

def save_controller_state(cname, state):
  v = math.floor(state * 1024 / 100)
  c = controllers[cname]
  c['pwm'].duty(v)
  c['state'] = state

  # last state
  if (c['to'] == c['state']):
    graphqlclient.send_controller_value(cname, state)
  
def init():
  wifi.get_connection()
  addr = wifi.ifconfig()
  config.write_conf('ip_address', addr)
  graphqlclient.send_config_value('ip', addr)

  # init controllers
  for cname in controllers:
    if controllers[cname]['enable']:
      pin = int(config.get_value("controller_%s_pin" % (cname)))
      switch = Pin(pin, Pin.OUT)
      controllers[cname]['pwm'] = PWM(switch)
      controllers[cname]['pwm'].freq(1000)
      print("%s controller up" % (cname))

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
    conn.sendall("Controller %s state %s in %sms is %s" % (controller, state, delay, resp))
    conn.close()

    while need_to_update():
      update_controller()

init()
