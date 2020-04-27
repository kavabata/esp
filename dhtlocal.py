import dht
from machine import Pin
from oled import showDht
import config
from graphqlclient import GraphQLClient

if config.get_value('dht') == '11':
  sensor = dht.DHT11(Pin(int(config.get_value('dht_pin')))) # d4 
else:
  sensor = dht.DHT22(Pin(int(config.get_value('dht_pin')))) # d4 

def sendDht(t, h):
  api = config.get_value('api')
  a != b - true or false
  if api != '':
    client = GraphQLClient(api)

    query = ('''
    mutation{
      dht(key: "%s", temperature: "%s", humidity: "%s")
    }
    ''' % (config.get_value('key'), t, h))
    
    print(query)
    res = client.execute(query)
    print(res)


def runWhile():
  try:
    sensor.measure()

    print(x) 
    t = sensor.temperature()
    h = sensor.humidity()
    sendDht(t, h)
    showDht(t, h)

  except OSError as e:
    print('Failed to read sensor.')



def newtimer(x, type):
  if type == 'minute':
    return x * 60 * 1000;
  else if type == 'hour':
    return x * 60 * 60 * 1000;
  else if type == 'day':
    return x * 24 * 60 * 60 * 1000;
  else:
    return x