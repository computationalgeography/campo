import numpy as np
from collections import OrderedDict

import campo.property as Property


class Values(object):

  def __init__(self, nr_objects, shapes, values):

    self.iter_idx = 0
    self.nr_objects = nr_objects

    self.values = OrderedDict()

    if isinstance(values, (int, float)):
      self._init_numbers(shapes, values)

    elif isinstance(values, np.ndarray):
      self._init_array(shapes, values)

    elif isinstance(values, Property):
      self._init_prop(shapes, values)
    else:
      raise NotImplementedError


  def _init_array(self, shapes, values):

    for idx, shape in enumerate(shapes):
      self.values[idx] = values[idx]


  def _init_numbers(self, shapes, values):

    dim = len(shapes[0])


    for idx, shape in enumerate(shapes):
      tmp = None
      if dim == 0:
        tmp = np.array(values)
      elif dim == 1 or dim == 2:
        tmp = np.full(shape, values)
      else:
        raise NotImplementedError

      self.values[idx] = tmp


  def _init_prop(self, shapes, values):

    for idx, shape in enumerate(shapes):
      self.values[idx] = values.values().values[idx]





  def __setitem__(self, index, value):

    if index < 0 or index > self.nr_objects:
      raise IndexError

    self.values[index] = value


  def __getitem__(self, index):
    return self.values[index]


  def __iter__(self):
        return self

  def __next__(self):
        if self.iter_idx == self.nr_objects:
            raise StopIteration

        values = self.values[self.iter_idx]
        self.iter_idx += 1

        return values
