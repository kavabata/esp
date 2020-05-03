
import config
import time
import wifi
import controller
import machine
import network
try:
  import usocket as socket
except:
  import socket


import gc
gc.collect()

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

    res, message = controller_request(request)
    if res:
      conn.send('HTTP/1.1 200 OK\n')
      conn.send('Content-Type: application/json\n')
      conn.send('Connection: close\n\n')
      conn.sendall('OK')
      
    else:
      conn.send('HTTP/1.1 400 bad request\n')
      conn.send('Content-Type: application/json\n')
      conn.send('Connection: close\n\n')
      conn.sendall(message)
    conn.close()

def controller_request(request):
  request_data = request.split('\r\n')[0].split(' ')
  request_details = request_data[1].split('/')[:4]
  if len(request_details) == 4:
    space, c, a, key = request_details
    if key == config.get_value('key'):
      return controller.fire(c, a)

  return False, 'Wrong request'
