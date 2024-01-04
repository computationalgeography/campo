import copy
import numpy


from ..points import Points
from ..areas import Areas
from ..property import Property

import campo.config as cc


def uniform(lower, upper):
    """ Returns for each object values drawn from a uniform distribution. Can be applied to fields and objects.

    :param lower: lower boundary
    :type lower:  Property
    :param upper: upper boundary
    :type upper: Property
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

    if isinstance(lower.space_domain, Points):
        shape = 1
    elif isinstance(lower.space_domain, Areas):
        shape = (int(lower.space_domain.row_discr[0]), int(lower.space_domain.col_discr[0]))
    else:
        raise NotImplementedError

    for idx in range(lower.nr_objects):
        values = None
        if isinstance(lower.space_domain, Points):
            lower_value = lower.values()[idx][0]
            upper_value = upper.values()[idx][0]
            values = cc.rng.uniform(low=lower_value, high=upper_value, size=shape)
        elif isinstance(lower.space_domain, Areas):
            lower_value = lower.values()[idx]
            upper_value = upper.values()[idx]
            values = cc.rng.uniform(low=lower_value, high=upper_value, size=shape)
        else:
            raise NotImplementedError

        tmp_prop.values()[idx] = values

    return tmp_prop


def normal(mean, stddev):
    """ Returns for each object values drawn from a normal distribution. Can be applied to fields and objects

    :param mean: Mean value
    :type mean:  Property
    :param stddev: Standard deviation
    :type stddev: Property
    :returns: a property with normal distributed values
    :rtype: Property
    """

    if not isinstance(mean, Property):
        raise ValueError

    if not isinstance(stddev, Property):
        raise ValueError

    if mean.pset_uuid != stddev.pset_uuid:
        msg = 'Property "{}" and property "{}" are not from the same PropertySet '.format(mean.name, stddev.name)
        raise ValueError(msg)

    tmp_prop = Property('emptynormalname', mean.pset_uuid, mean.space_domain, mean.shapes)

    if isinstance(mean.space_domain, Points):
        shape = 1
    elif isinstance(mean.space_domain, Areas):
        shape = (int(mean.space_domain.row_discr[0]), int(mean.space_domain.col_discr[0]))
    else:
        raise NotImplementedError

    for idx in range(mean.nr_objects):
        values = None
        if isinstance(mean.space_domain, Points):
            mean_value = mean.values()[idx][0]
            stddev_value = stddev.values()[idx][0]
            values = cc.rng.normal(loc=mean_value, scale=stddev_value, size=shape)
        elif isinstance(mean.space_domain, Areas):
            mean_value = mean.values()[idx]
            stddev_value = stddev.values()[idx]
            values = cc.rng.normal(loc=mean_value, scale=stddev_value, size=shape)
        else:
            raise NotImplementedError

        tmp_prop.values()[idx] = values

    return tmp_prop



def random_integers(lower, upper):
    """ Returns for each object random_integers values. Can be applied to fields and objects

    :param lower: lower boundary
    :type lower:  Property
    :param upper: upper boundary
    :type upper: Property
    :returns: a property with random integers values from lower (inclusive) to upper (exclusive)
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

    if isinstance(lower.space_domain, Points):
        shape = 1
    elif isinstance(lower.space_domain, Areas):
        shape = (int(lower.space_domain.row_discr[0]), int(lower.space_domain.col_discr[0]))
    else:
        raise NotImplementedError

    for idx in range(lower.nr_objects):
        values = None
        if isinstance(lower.space_domain, Points):
            lower_value = lower.values()[idx][0]
            upper_value = upper.values()[idx][0]
            values = cc.rng.integers(low=lower_value, high=upper_value, size=shape)
        elif isinstance(lower.space_domain, Areas):
            lower_value = lower.values()[idx]
            upper_value = upper.values()[idx]
            values = cc.rng.integers(low=lower_value, high=upper_value, size=shape)
        else:
            raise NotImplementedError

        tmp_prop.values()[idx] = values

    return tmp_prop

