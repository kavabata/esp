import network
import socket
import ure
import time
import config

wlan_sta = network.WLAN(network.STA_IF)
server_socket = None

def get_connection():
    """return a working WLAN(STA_IF) instance or None"""

    # First check if there already is any connection:
    if wlan_sta.isconnected():
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
        print('\nConnected. Network config: ', wlan_sta.ifconfig())
    else:
        print('\nFailed. Not Connected to: ' + ssid)
    return connected

def ifconfig():
    a = wlan_sta.ifconfig()
    return a[0]
