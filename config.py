import network
import socket
import ure
import time

CONF_FILE = 'config.dat'

# def put_default():
#   confmgr.write_conf('wifi_ssid', 'UKA173')
#   confmgr.write_conf('wifi_password', '0685153051')
#   confmgr.write_conf('key', 'mykeyrele')
#   confmgr.write_conf('api', 'http://192.168.1.149:4000/graphql')

def get_values():
  lines = []
  with open(CONF_FILE) as f:
      lines = f.readlines()
  
  values = {}
  for line in lines:
    key, value = line.strip("\n").split(";")
    values[key] = value
  return values

def get_value(key):
  with open(CONF_FILE) as f:
    lines = f.readlines()
  values = {}
  for line in lines:
    k, value = line.strip("\n").split(";")
    if k == key:
      return value
  return None

def write_conf(key, value):
  lines = []
  values = get_values()
  values[key] = value
  for k, v in values.items():
    lines.append("%s;%s\n" % (k, v))
  with open(CONF_FILE, "w") as f:
    f.write(''.join(lines))