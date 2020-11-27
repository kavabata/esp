

*** ESP8266 ***
Get firmware micropython:
https://micropython.org/download/esp8266/

Put firmware on board:

esptool.py -p /dev/tty.wchusbserial1420 flash_id
esptool.py -p /dev/tty.wchusbserial1420 erase_flash
esptool.py -p /dev/tty.wchusbserial1420 --baud 115200 write_flash --flash_size=detect -fm dio 0 ./bin/<esp>




Ampy file manager:
* Note. fix ampy manager: https://github.com/scientifichackers/ampy/issues/19
/Library/Python/2.7/site-packages/ampy/pyboard.py
```
n = self.serial.inWaiting()
while n > 0:
    self.serial.read(n)
    n = self.serial.inWaiting()
time.sleep(2) # add this line
```

ampy -p /dev/tty.wchusbserial1420 ls




