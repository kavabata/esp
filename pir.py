from machine import Pin, ADC
import time
import oled
import config
from graphqlclient import send_sensor_value

cnt = 0
pirState = 0
ldr = None

def init():
  if int(config.get_value('sensor_pir')) > 0: 
    ldr = Pin(int(config.get_value('sensor_pir_pin')), Pin.IN) #13 d5
    ldr.irq(trigger=Pin.IRQ_RISING, handler=runWhilePir)

def sendApi(state):
  send_sensor_value("pir", state)

def runWhilePir():
  newState = ldr.value()
  global pirState

  if pirState != newState:
    pirState = newState
    sendApi(newState)
