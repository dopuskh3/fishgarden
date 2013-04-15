import serial
import logging
from threading import Thread
from garden import config

log = logging.getLogger(__name__)

class ArduinoSensor(Thread):

  def __init__(self):
    Thread.__init__(self)
    self._sensorValues = dict()
    self._run = True
    self._opened = False

  def _openSerial(self):
    conf = config.getConfig()
    self._serialPort = serial.Serial(conf.arduino['serial_port'], conf.arduino['serial_speed'])
    self._opened = True

  def _update(self, line):
    (name, value) = [ k.strip(' ') for k in line.rstrip('\n').split('=') ]
    try:
      value = int(value.strip(' '))
    except ValueError:
      log.error("Cannot parse line: '%s'" % line)
    self._sensorValues[name] = value

  def run(self):
    if not self._opened:
      self._openSerial()

    while self._run:
      line = self._serialPort.readline()
      self._update(line)

  def stop(self):
    self._run = False

  def get(self, name):
    return self._sensorValues.get(name)

  def getAllValues(self):
    return self._sensorValues
