import numpy as np
from collections import OrderedDict

from . import property


class Values(object):

    def __init__(self, nr_objects, shapes, values):

        self.iter_idx = 0
        self.nr_objects = nr_objects

        self.values = OrderedDict()

        if isinstance(values, (int, float)):
            self._init_numbers(shapes, values)
        elif isinstance(values, np.ndarray):
            self._init_array(shapes, values)
        elif isinstance(values, property.Property):
            self._init_prop(shapes, values)
        else:
            msg = f"Setting values with '{type(values).__name__}' is not implemented. Use NumPy arrays instead."
            raise NotImplementedError(msg)

    def _init_array(self, shapes, values):

        dim = len(shapes[0])

        if values.ndim == 2:
            msg = f"Array of shape ({values.shape[0]}, {values.shape[1]}) cannot be assigned to one agent, use shape (1, {values.shape[0]}, {values.shape[1]})"
            raise ValueError(msg)

        if len(shapes) != values.shape[0]:
            msg = f"Number of provided values ({values.shape[0]}) does not match number of agents ({len(shapes)})"
            raise ValueError(msg)

        for idx, shape in enumerate(shapes):
            if dim == 1:
                self.values[idx] = np.array([values[idx]])
            elif dim == 2:
                if shape != values[idx].shape:
                    msg = f"The provided shape {values[idx].shape} does not match the expected shape {shape}"
                    raise ValueError(msg)
                self.values[idx] = values[idx]
            else:
                raise NotImplementedError

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
            self.iter_idx = 0
            raise StopIteration

        values = self.values[self.iter_idx]
        self.iter_idx += 1

        return values
