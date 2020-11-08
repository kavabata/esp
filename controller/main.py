import wifi
# import oled
import dhtlocal
# import pir
import config
import machine
import graphqlclient
# import lightlevel
import switch
import time
import network
try:
  import usocket as socket
except:
  import socket

import gc
gc.collect()

wifi.get_connection()
graphqlclient.send_config_value('ip', wifi.ifconfig())


def init():
  addr = config.get_value('ip_address')
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

    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: application/json\n')
    conn.send('Connection: close\n\n')
    
    conn.sendall(request)
    conn.close()

  init()

# graphqlclient.update_config()

# if int(config.get_value('sensor_dht')) > 0:
#   print('temperature_delay')
#   print('run dht cron')
#   t0 = machine.Timer(0)
#   t0.init(period=int(config.get_value('temperature_delay')), mode=t0.PERIODIC, callback=dhtlocal.runWhile)

# if int(config.get_value('sensor_lightlevel')) > 0:
#   lightlevel.init()
#   t1 = machine.Timer(1)
#   t1.init(period=config.get_value('sensor_lightlevel_delay'), mode=t1.PERIODIC, callback=lightlevel.run)
  
# if int(config.get_value('sensor_pir')) > 0:
#   pir.init()

# time.sleep(10)

# switch.init()

