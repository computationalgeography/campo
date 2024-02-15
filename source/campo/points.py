import csv
import numpy as np


class Points():
    def __init__(self, mobile=False):

        self.nr_items = None

        self.space_dimension_constant = None

        self.nr_dimensions = 2

        self.xcoord = None
        self.ycoord = None

        self._coordinates = None

        self._mobile = mobile

        self.iter_idx = 0

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
    def xcoord(self):
        return self._xcoord

    @xcoord.setter
    def xcoord(self, values):
        new_values = values
        if new_values is not None:
            if isinstance(values, list):
                new_values = np.array(values)

            if new_values.shape != (self.nr_items,):
                msg = f"Number of provided coordinates ({new_values.shape[0]}) does not match number of agents ({self.nr_items})"
                raise RuntimeError(msg)

        self._xcoord = new_values

    @property
    def ycoord(self):
        return self._ycoord

    @ycoord.setter
    def ycoord(self, values):
        new_values = values
        if new_values is not None:
            if isinstance(values, list):
                new_values = np.array(values)

            if new_values.shape != (self.nr_items,):
                msg = f"Number of provided coordinates ({new_values.shape[0]}) does not match number of agents ({self.nr_items})"
                raise RuntimeError(msg)

        self._ycoord = new_values

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

            v = np.empty((self.nr_items, 2))
            for idx, item in enumerate(content):
                v[idx, 0] = item[0]
                v[idx, 1] = item[1]

            self.xcoord = v[:, 0]
            self.ycoord = v[:, 1]

            self._coordinates = np.empty((self.nr_items, 2))

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_idx == self.nr_items:
            self.iter_idx = 0
            raise StopIteration

        values = (self.xcoord[self.iter_idx], self.ycoord[self.iter_idx])
        values = self.xcoord[self.iter_idx], self.ycoord[self.iter_idx]
        self.iter_idx += 1

        return values

    def __len__(self):
        return len(self.xcoord)

    def __repr__(self):
        return 'Point'

    def _get_coordinates(self):

        self._coordinates[:, 0] = self.xcoord
        self._coordinates[:, 1] = self.ycoord
        return self._coordinates

    def _set_coordinates(self, values):
        self._coordinates = values
