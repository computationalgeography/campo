import csv
import numpy


class Points(object):
  def __init__(self, mobile=False):

    self.nr_items = None

    self.space_dimension_constant = None

    self.nr_dimensions = 2

    self.xcoord = None
    self.ycoord = None

    self._mobile = mobile

    self.iter_idx = 0


  @property
  def mobile(self):
    return self._mobile

  @property
  def xcoord(self):
    return self._xcoord

  @xcoord.setter
  def xcoord(self, value):
    self._xcoord = value

  @property
  def ycoord(self):
    return self._ycoord

  @ycoord.setter
  def ycoord(self, value):
    self._ycoord = value


  @property
  def nr_items(self):
    return self._nr_items

  @nr_items.setter
  def nr_items(self, value):
    self._nr_items = value


  def read(self, filename):

    with open(filename, 'r') as csvfile:
      reader = csv.reader(csvfile)
      content = list(reader)

      self.nr_items = len(content)

      #x = numpy.zeros(self.nr_items)
      #y = numpy.zeros(self.nr_items)

      #for idx, item in enumerate(content):
        #x[idx] = item[0]
        #y[idx] = item[1]

      #self.xcoord = x
      #self.ycoord = y

      v = numpy.zeros((self.nr_items,2))
      for idx, item in enumerate(content):
        v[idx,0] = item[0]
        v[idx,1] = item[1]
     # numpy.random.shuffle(v)

      self.xcoord = v[:,0]
      self.ycoord = v[:,1]



  def __iter__(self):
    return self

  def __next__(self):
        if self.iter_idx == self.nr_items:
            self.iter_idx = 0
            raise StopIteration

        values = (self.xcoord[self.iter_idx], self.ycoord[self.iter_idx])
        self.iter_idx += 1

        return values


  def __len__(self):
      return len(self.xcoord)
