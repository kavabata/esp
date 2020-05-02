import network
import socket
import ure
import time
import oled
import config
from graphqlclient import send_config_value

wlan_sta = network.WLAN(network.STA_IF)

server_socket = None

def get_connection():
    """return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    if wlan_sta.isconnected():
        # oled.console('wifi connected [1]')
        return wlan_sta
    
    try:
      do_connect(config.get_value('wifi_ssid'), config.get_value('wifi_password'))

    except OSError as e:
      print("exception", str(e))


def do_connect(ssid, password):
    wlan_sta.active(True)
    if wlan_sta.isconnected():
        return None
    print('Trying to connect to %s...' % ssid)
    wlan_sta.connect(ssid, password)
    for retry in range(100):
        connected = wlan_sta.isconnected()
        if connected:
            break
        time.sleep(0.1)
        print('.', end='')
    if connected:
        oled.console('wifi connected [2]')
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        oled.console('wifi fail')
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

def send_config():
    a = wlan_sta.ifconfig()
    print (a[0])
    send_config_value('ip', a[0])

