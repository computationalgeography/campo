import numpy as np
import os
import csv

import lue
import lue.data_model as ldm

from .points import Points
from .areas import Areas
from .propertyset import PropertySet
from .utils import color_message




class Phenomenon(object):
    """ """

    def __init__(self, name):

        self._name = name
        self._nr_objects = 0
        self._property_sets = {}

        self._epsg = None


    def set_epsg(self, epsg):
      """ Setting Coordinate Reference System (CRS) for the spatial domain


      :param epsg: EPSG code
      :type epsg: int
      """
      for p in self._property_sets:
        self._property_sets[p].space_domain.epsg = epsg

      self._epsg = epsg



    def __len__(self):
      return len(self._property_sets)


    def __getattr__(self, property_set_name):

      if property_set_name in self._property_sets:
        return self._property_sets[property_set_name]
      else:
        msg = color_message(f'No property set "{property_set_name}" in phenomenon "{self._name}"')
        raise TypeError(msg)



    def _read_domain(self, filename):

      nr_objects = None
      domain = None
      shape = None

      # simple test if file contains points or field
      with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        content = list(reader)

        nr_objects = len(content)

        if len(content[0]) == 2:
          # point agents
          domain = Points()
          domain.read(filename)

          shape = [(1,)] * nr_objects


        elif len(content[0]) == 6:
          # field agents
          domain = Areas()
          domain.read(filename)
          shape = [(int(domain.row_discr[i]), int(domain.col_discr[i])) for i in range(nr_objects)]


        else:
          raise NotImplementedError


      assert nr_objects is not None
      assert domain is not None
      assert shape is not None

      return nr_objects, domain, shape


    def add_property_set(self, pset_name, filename):
      """ """

      nr_objects, domain, shape  = self._read_domain(filename)
      if nr_objects != 0:
        self._nr_objects = nr_objects

      assert self._nr_objects == nr_objects

      p = PropertySet(pset_name, nr_objects, domain, shape)
      self._property_sets[pset_name] = p

      if self._epsg:
        p.space_domain.epsg = self._epsg






    @property
    def nr_objects(self):
      return self._nr_objects

    @property
    def time_domain(self):
      return self._time_domain

    @property
    def object_ids(self):
      return self._object_ids

    @property
    def name(self):
      return self._name

    @property
    def property_sets(self):
      return self._property_sets

    def __repr__(self, indent=0):
      msg = '{}Phenomenon: {}\n'.format('  ' * indent, self.name)
      msg += '{}Agents: {}'.format('  ' * (indent+1), self.nr_objects)

      if len(self._property_sets) == 0:
        msg += '\n{}Property sets: 0'.format('  ' * (indent+1))
      else:
        for p in self._property_sets:
          msg += '\n'
          msg += self._property_sets[p].__repr__(indent+1)


      return msg
