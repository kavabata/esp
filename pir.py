from machine import Pin, ADC
import time
import oled
import config
from graphqlclient import GraphQLClient

light = ADC(0)
cnt = 0
pirState = 0
ldr = None

def init():
  if int(config.get_value('pir')) > 0: 
    ldr = Pin(int(config.get_value('pir_pin')), Pin.IN) #13 d5

def sendApi(state):
  client = GraphQLClient(api)

  query = ('''
  mutation{
    pir(key: "%s", state: "%s")
  }
  ''' % (confmgr.get_value('key'), state))

  print(query)
  
  res = client.execute(query)

def runWhilePir():
  newState = ldr.value()
  global pirState

  if pirState != newState:
    pirState = newState
    sendApi(newState)


def runWhileLight():
  client = GraphQLClient(confmgr.get_value('api'))

  query = ('''
  mutation{
    light(key: "%s", level: "%s")
  }
  ''' % (confmgr.get_value('key'), light.read()))
  
  res = client.execute(query)

init()