import wifi
import oled
import dhtlocal
import pir
import config
import machine
import graphqlclient
import lightlevel
import switch


# oled.console('Run')
wifi.get_connection()
# graphqlclient.send_config_value('ip', wifi.ifconfig())
# graphqlclient.update_config()

# config.get_value('temperature_delay')

# if int(config.get_value('sensor_dht')) > 0:
#   t0 = machine.Timer(0)
#   t0.init(period=int(config.get_value('temperature_delay')), mode=t2.PERIODIC, callback=dhtlocal.runWhile)

# if int(config.get_value('sensor_lightlevel')) > 0:
#   lightlevel.init()
#   t1 = machine.Timer(1)
#   t1.init(period=config.get_value('sensor_lightlevel_delay'), mode=t3.PERIODIC, callback=lightlevel.run)
  
# if int(config.get_value('sensor_pir')) > 0:
#   pir.init()

# switch.init()

