"""
.. module: config
  .. synopsis: this module contains configuration related functions and classes.


Configuration is loaded from a standard yaml file. Here is a sample configuration file:

Configuration reference
~~~~~~~~~~~~~~~~~~~~~~~

The following describe the configuration file and its component.

"""
import yaml

_CONFIG = None

class Config(dict):
  """Configuration object.

  The configuration object stores program global configuration. Main configuration parameters
  are available as object parameters:
  """

  def __init__(self, pdValues):
    self.update(pdValues)

  @classmethod
  def load(cls, poFileObject):
    """Load a configuration file from a file descriptor.

    :param poFileObject: a file descriptor to read configuration from.
    :type poFileObject: File object.
    :returns: A Config instance.
    """
    ldConfig = yaml.load(poFileObject.read())
    if not isinstance(ldConfig, dict):
      raise ValueError("Configuration must be a yaml dictionary.")
    return Config(ldConfig)

  def __getattr__(self, psAttribute):
    try:
      return self[psAttribute]
    except KeyError:
      raise AttributeError("No such configuration value: %s" % psAttribute)

  def __setattr__(self, psAttribute):
    raise ValueError("Config object is read only !")


def getConfig():
  """Gets configuration singleton.

  :raises: ValueError if a configuration as not been loaded yet.
  """
  if _CONFIG is None:
    raise ValueError("Config has not been initialized. Call loadConfig()")
  return _CONFIG

def _setConfig(poConfig):
  """Set configuration singleton.

  .. note::

    This function should be used internally (eg. tests) only.
  """
  global _CONFIG
  _CONFIG = poConfig

def loadConfig(poFileObject):
  """Load configuration singleton from a file object."""
  global _CONFIG
  _CONFIG = Config.load(poFileObject)
  return getConfig()

def loadConfigFromFile(psFilename):
  with open(psFilename) as loFd:
    return loadConfig(loFd)
