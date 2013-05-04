import time
import sys
from garden import config, arduino
from bottle import route, run

class Server(object):
  
  def __init__(self):
    self._channel = arduino.ArduinoChannel(config.getConfig().arduino['sensor_refresh_interval']) 
    self._channel.start()
    self._initRoutes()
    
  def _initRoutes(self):
    route('/sensors')(self.sensors)

  def sensors(self):
    return self._channel.getAllValues()

  

def runServer(psConfigFile):
  config.loadConfigFromFile(psConfigFile)
  server = Server()
  run(host='0.0.0.0', port=8888)

if __name__ == "__main__":
  runServer(sys.argv[1])
