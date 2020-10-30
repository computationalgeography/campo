import numpy as np
import uuid

import lue.data_model as ldm



from .points import Points
from .areas import Areas
from .property import Property
from .utils import TimeDiscretization, color_message



class PropertySet(object):

    def __init__(self, name, nr_agents, space_domain, shape):

      self._properties = {}
      self._name = name
      self._nr_agents = nr_agents
      self._space_domain = space_domain
      self._shape = shape
      self._uuid = uuid.uuid4()



    @property
    def uuid(self):
      return self._uuid

    @property
    def space_domain(self):
      return self.space_domain


    @property
    def time_domain(self):
      return self.time_domain

    @property
    def domain(self):
      return self._domain


    @property
    def nr_objects(self):
      return self._nr_agents


    @property
    def name(self):
      return self._name

    @property
    def space_domain(self):
      return self._space_domain

    @property
    def properties(self):
      return self._properties


    @property
    def shapes(self):
      return self._shape

    def __len__(self):
      return len(self._properties)



    def set_space_domain(self, variable, values):
      assert isinstance(variable, str)
      if isinstance(values, Points):

        self._domain = values


      elif isinstance(values, Areas):

        self._domain = values


      else:
        raise NotImplementedError


      for p in self._properties:
        p.pset_domain = self._domain


    def add_property(self, property_name, dtype=np.float64, time_discretisation=TimeDiscretization.dynamic, rank=None, shape=None):

      assert isinstance(property_name, str)
      assert self._lue_dataset_name is not None

      self.time_discretisation = time_discretisation


      # FAME
      self.shapes = None
      if isinstance(self._domain, Points):
        if rank == None:
          self.shapes = [()] * self._phen
        elif rank != None and shape != None:
          self.shapes = [shape] * self._phen
        else:
          raise NotImplementedError
      elif isinstance(self._domain, Areas):
        self.shapes = [(int(self._domain.row_discr[i]), int(self._domain.col_discr[i])) for i in range(len(self._domain.row_discr))]
      else:
        raise NotImplementedError


      p = Property(self._phen, self.shapes, self._uuid, self._domain, self.time_discretisation)
      p.name = property_name

      p._lue_pset_name = self.__name__

      self._properties.add(p)

      # LUE

      nr_timesteps = int(self._lue_dataset.phenomena['framework'].property_sets['fame_time_cell'].time_domain.value[0][1])

      pset = self._lue_dataset.phenomena[self._lue_phenomenon_name].property_sets[self.__name__]

      if isinstance(p.pset_domain, Points):

        if self.time_discretisation == TimeDiscretization.dynamic:
          p_shape = (nr_timesteps,)
          prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=p_shape, value_variability=ldm.ValueVariability.variable)
          prop.value.expand(self.nr_objects())# * nr_timesteps)
        else:
          prop = pset.add_property(property_name, dtype=np.dtype(dtype))
          prop.value.expand(self.nr_objects())

      elif isinstance(p.pset_domain, Areas):

        # all same shape...
        #p_shape = (p.pset_domain.row_discr[0], p.pset_domain.col_discr[0])
        #p_shape = (2,1)
        #prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=p_shape, value_variability=lue.ValueVariability.variable)



        if self.time_discretisation == TimeDiscretization.dynamic:
          prop = pset.add_property(property_name, dtype=np.dtype(dtype), rank=2,
            shape_per_object=ldm.ShapePerObject.different,
            shape_variability=ldm.ShapeVariability.constant)
        else:
          # Same shape
          # prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=shape)

          # Different shape
          prop = pset.add_property(property_name, dtype=np.dtype(dtype), rank=2)#,

        space_discr = pset.fame_discretization

        for idx, item in enumerate(p.pset_domain):
          space_discr.value[idx]= [item[4], item[5]]
          #prop.value.expand(idx, item, nr_timesteps)


        prop.set_space_discretization(
            ldm.SpaceDiscretization.regular_grid,
            space_discr)
        #prop.value.expand(self.nr_objects())

        rank = 2
        if self.time_discretisation == TimeDiscretization.dynamic:
          for idx, item in enumerate(p.pset_domain):
            #prop.value.expand(idx, tuple([nr_timesteps, item[4], item[5]]), self.nr_objects())
            prop.value.expand(idx, tuple([item[4], item[5]]), nr_timesteps)
        else:
          shapes = np.zeros(self.nr_objects() * rank, dtype=ldm.dtype.Count).reshape(self.nr_objects(), rank)

          for idx, item in enumerate(p.pset_domain):
            shapes[idx][0] = item[4]
            shapes[idx][1] = item[5]

          prop.value.expand(self._lue_dataset.phenomena[self._lue_phenomenon_name].object_id[:], shapes)



      else:
        raise NotImplementedError

      ldm.assert_is_valid(self._lue_dataset_name)



    def __getattr__(self, name):
      if name in self._properties:
        return self._properties[name]
      else:
        msg = color_message(f'No property "{name}" in property set "{self._name}"')
        raise TypeError(msg)



    def __setattr__(self, name, value):

      if name.startswith('_', 0, 1):
        self.__dict__[name] = value
      else:
        # We assume the modeller wants to access an existing property
        if name in self._properties:
          self._properties[name].set_values(value)
        else:
          # Create a new property
          p = Property(name, self._uuid, self._space_domain, self._shape, value)
          self._properties[name] = p




    def __repr__(self, indent=0):
      msg = '{}Property set: {}\n'.format('  ' * indent, self.name)
      msg += '{}Type: {}'.format('  ' * (indent+1), self.space_domain)

      if len(self._properties) == 0:
        msg += '\n{}Properties: 0'.format('  ' * (indent+1))
      else:
        for p in self._properties:
          msg += '\n'
          msg += self._properties[p].__repr__(indent+2)

      return msg

