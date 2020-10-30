import csv
import numpy

from .points import Points


class Areas(object):

  def __init__(self, mobile=False):

    self.iter_idx = 0

    self.nr_items = None
    self.space_discretisation_constant = None
    self.space_origin_constant = None

    # start with a plain unoptimised array for the row and columns
    self.space_discretisations = None

    # 2D coordinate for the upper left (?) corner
    # Use lue_points here for bounding box?
    self.space_origins = None

    # upper left
    self.p1 = None
    # lower right
    self.p2 = None
    #
    self.row_discr = None
    self.col_discr = None


    self._mobile = mobile


    self._epsg = None


  @property
  def epsg(self):
      return self._epsg

  @epsg.setter
  def epsg(self, epsg):
      assert isinstance(epsg, int)
      self._epsg = epsg

  @property
  def mobile(self):
    return self._mobile


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

      self.p1 = Points()
      self.p2 = Points()


      x1 = numpy.zeros(self.nr_items)
      y1 = numpy.zeros(self.nr_items)

      x2 = numpy.zeros(self.nr_items)
      y2 = numpy.zeros(self.nr_items)

      xdiscr = numpy.zeros(self.nr_items)
      ydiscr = numpy.zeros(self.nr_items)

      for idx, item in enumerate(content):
        x1[idx] = item[0]
        y1[idx] = item[1]
        x2[idx] = item[2]
        y2[idx] = item[3]
        xdiscr[idx] = item[4]
        ydiscr[idx] = item[5]

      self.p1.xcoord = x1
      self.p1.ycoord = y1

      self.p2.xcoord = x2
      self.p2.ycoord = y2


      self.row_discr = xdiscr
      self.col_discr = ydiscr


  def __iter__(self):
        return self

  def __next__(self):
        if self.iter_idx == self.nr_items:
            self.iter_idx = 0
            raise StopIteration

        values = (self.p1.xcoord[self.iter_idx],
                  self.p1.ycoord[self.iter_idx],
                  self.p2.xcoord[self.iter_idx],
                  self.p2.ycoord[self.iter_idx],
                  self.row_discr[self.iter_idx],
                  self.col_discr[self.iter_idx],
                  )
        self.iter_idx += 1

        return values


  def __repr__(self):
    return 'Area'

  def _extent(self, index):
        values = (self.p1.xcoord[index],
                  self.p1.ycoord[index],
                  self.p2.xcoord[index],
                  self.p2.ycoord[index],
                  int(self.row_discr[index]),
                  int(self.col_discr[index]),
                  )

        return values
