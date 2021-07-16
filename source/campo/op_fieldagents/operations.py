import copy
import numpy


from ..points import Points
from ..areas import Areas
from ..property import Property




def uniform(lower, upper, seed=0):
  """ Returns for each object values drawn from a uniform distribution. Can be applied to fields and objects.

  :param lower: lower boundary
  :type lower:  Property
  :param upper: upper boundary
  :type upper: Property
  :param seed: random seed (default 0)
  :type seed: int
  :returns: a property with uniform distributed values
  :rtype: Property

  """

  if not isinstance(lower, Property):
    raise ValueError

  if not isinstance(upper, Property):
    raise ValueError

  if lower.pset_uuid != upper.pset_uuid:
      msg = 'Property "{}" and property "{}" are not from the same PropertySet '.format(lower.name, upper.name)
      raise ValueError(msg)

  tmp_prop = Property('emptyuniformname', lower.pset_uuid, lower.space_domain, lower.shapes)


  for idx in range(lower.nr_objects):
    values = None
    if isinstance(lower.space_domain, Points):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower.values()[idx], upper.values()[idx])
    elif isinstance(lower.space_domain, Areas):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.uniform(lower.values()[idx], upper.values()[idx], (int(lower.space_domain.row_discr[idx]), int(lower.space_domain.col_discr[idx])))
    else:
      raise NotImplementedError

    tmp_prop.values()[idx] = values

  return tmp_prop


def normal(lower, upper, seed=0):
  """ Returns for each object values drawn from a normal distribution. Can be applied to fields and objects

  :param lower: lower boundary
  :type lower:  Property
  :param upper: upper boundary
  :type upper: Property
  :param seed: random seed (default 0)
  :type seed: int
  :returns: a property with normal distributed values
  :rtype: Property

  """

  if not isinstance(lower, Property):
    raise ValueError

  if not isinstance(upper, Property):
    raise ValueError

  if lower.pset_uuid != upper.pset_uuid:
      msg = 'Property "{}" and property "{}" are not from the same PropertySet '.format(lower.name, upper.name)
      raise ValueError(msg)

  tmp_prop = Property('emptynormalname', lower.pset_uuid, lower.space_domain, lower.shapes)


  for idx in range(lower.nr_objects):
    values = None
    if isinstance(lower.space_domain, Points):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.normal(lower.values()[idx], upper.values()[idx])
    elif isinstance(lower.space_domain, Areas):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.normal(lower.values()[idx], upper.values()[idx], (int(lower.space_domain.row_discr[idx]), int(lower.space_domain.col_discr[idx])))
    else:
      raise NotImplementedError

    tmp_prop.values()[idx] = values

  return tmp_prop



def random_integers(lower, upper, seed=0):
  """ Returns for each object random_integers values. Can be applied to fields and objects

  :param lower: lower boundary
  :type lower:  Property
  :param upper: upper boundary
  :type upper: Property
  :param seed: random seed (default 0)
  :type seed: int
  :returns: a property with random integers values
  :rtype: Property

  """

  if not isinstance(lower, Property):
    raise ValueError

  if not isinstance(upper, Property):
    raise ValueError

  if lower.pset_uuid != upper.pset_uuid:
      msg = 'Property "{}" and property "{}" are not from the same PropertySet '.format(lower.name, upper.name)
      raise ValueError(msg)

  tmp_prop = Property('emptynormalname', lower.pset_uuid, lower.space_domain, lower.shapes)


  for idx in range(lower.nr_objects):
    values = None
    if isinstance(lower.space_domain, Points):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.random_integers(lower.values()[idx], upper.values()[idx])
    elif isinstance(lower.space_domain, Areas):
      if seed != 0:
        numpy.random.seed(seed + idx)
      values = numpy.random.random_integers(lower.values()[idx], upper.values()[idx], (int(lower.space_domain.row_discr[idx]), int(lower.space_domain.col_discr[idx])))
    else:
      raise NotImplementedError

    tmp_prop.values()[idx] = values

  return tmp_prop

