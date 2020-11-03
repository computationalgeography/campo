import enum

import lue.data_model as ldm


def _color_message(message, colour_start='\033[31m'):
  """ Colourize message using ANSI escape codes """
  colour_end = '\033[0m'
  return f'{colour_start}{message}{colour_end}'

class TimeDomain(enum.Enum):
  """ Enum to indicate time domain of a property set """
  static = 1
  dynamic = 2



class TimeDiscretization(enum.Enum):
  """ Enum to indicate temporal discretisation of a property set """
  static = 1
  dynamic = 2


class TimeUnit(enum.Enum):
  """ Enum to indicate time step unit of a model """

  day = ldm.Unit.day
  month = ldm.Unit.month
  year = ldm.Unit.year
