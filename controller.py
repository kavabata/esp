from machine import Pin
import config
import graphqlclient

switch = None
switch2 = None
switch3 = None

if int(config.get_value('controller_switch')) > 0:
  switch = Pin(int(config.get_value('controller_switch_pin')), Pin.OUT)
  switch.value(0)

if int(config.get_value('controller_switch2')) > 0:
  switch2 = Pin(int(config.get_value('controller_switch2_pin')), Pin.OUT)
  switch.value(0)

if int(config.get_value('controller_switch3')) > 0:
  switch2 = Pin(int(config.get_value('controller_switch3_pin')), Pin.OUT)
  switch.value(0)

def fire(controller, action):
  print('Lets fire %s with %s' % (controller, action))

  if controller == 'switch':
    switch.value(int(action))
    graphqlclient.send_controller_value(controller, action)
    return True, 'OK'

  if controller == 'switch2':
    switch2.value(int(action))
    graphqlclient.send_controller_value(controller, action)
    return True, 'OK'

  return False, 'Wrong Eval "%s"' % controller
