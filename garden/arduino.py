import time
import re
import serial
import logging
from threading import Thread, Lock
from garden import config

log = logging.getLogger(__name__)


class ArduinoSensorHelper(object):
  SENSOR_COMMAND = "sensors"
  
  @classmethod
  def parseSensorLine(cls, line):
    sensor_values = dict()
    if re.match("sensors=.+", line):
      sensors = line.split('=')[1]
      for sensor_part in sensors.split(','):
        (name, value) = sensor_part.split(':')
        sensor_values[name] = int(value)
    return sensor_values


class ArduinoChannel(Thread):

  def __init__(self, update_interval):
    Thread.__init__(self)
    self._sensorValues = dict()
    self._run = True
    self._opened = False
    self._update_interval = update_interval
    self._lock = Lock()

  def _openSerial(self):
    conf = config.getConfig()
    self._serialPort = serial.Serial(conf.arduino['serial_port'], conf.arduino['serial_speed'])
    self._opened = True

  def _fetchSensorsValues(self):
    with self._lock:
      log.info("Fetching sensors values...")
      self._serialPort.write(ArduinoSensorHelper.SENSOR_COMMAND)
      resp = self._serialPort.readline()
      self._sensorValues = ArduinoSensorHelper.parseSensorLine(resp)
      self._sensorValues['update_time'] = time.time()
      log.info("Stored: %s " % resp)

  def run(self):
    if not self._opened:
      self._openSerial()
    while self._run is not False:
      self._fetchSensorsValues()
      time.sleep(self._update_interval)

  def stop(self):
    self._run = False

  def get(self, name):
    if not self._sensorValues:
      self._fetchSensorsValues()
    return self._sensorValues.get(name)

  def getAllValues(self):
    return self._sensorValues
