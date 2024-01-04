import numbers
import os
import numpy as np

from .values import Values



class Property(object):
    def __init__(self, name, pset_uuid, pset_domain, shape, initial_value = np.nan):

        self._name = name
        self._pset_uuid = pset_uuid
        self._pset_domain = pset_domain

        self._nr_agents = self._pset_domain.nr_items
        self._shape = shape

        self._is_dynamic = False

        self._values = Values(self._nr_agents, self._shape, initial_value)


    @property
    def is_dynamic(self):
        return self._is_dynamic

    @is_dynamic.setter
    def is_dynamic(self, value):
        self._is_dynamic = value


    def values(self):
        return self._values

    @property
    def nr_objects(self):
        return self._nr_agents

    @property
    def pset_uuid(self):
        return self._pset_uuid

    @property
    def space_domain(self):
        return self._pset_domain


    @property
    def name(self):
        return self._name

    @property
    def shapes(self):
        return self._shape

    def set_values(self, values):
        self._values = Values(self._nr_agents, self._shape, values)


    def __repr__(self, indent=0):
        msg = '{}Property: {}'.format('  ' * indent, self.name)

        return msg

