import network
import socket
import ure
import time

CONF_FILE = 'config.dat'

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
  return 0

def write_conf(key, value):
  lines = []
  values = get_values()
  values[key] = value
  for k, v in values.items():
    lines.append("%s;%s\n" % (k, v))
  with open(CONF_FILE, "w") as f:
    f.write(''.join(lines))