import enum

import lue.data_model as ldm

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
