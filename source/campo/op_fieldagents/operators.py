import copy

from ..property import Property


def _PropOp(arg1, op):

    if not isinstance(arg1, Property):
        msg = 'Property expected'
        raise TypeError(msg)

    tmp_prop = copy.deepcopy(arg1)

    for idx in range(0, tmp_prop.nr_objects):
        tmp_prop.values()[idx] = op(arg1.values()[idx])

    return tmp_prop


def _PropOpB(arg1, arg2, op, cast_type=None):

    if isinstance(arg2, Property):
        if arg1.pset_uuid != arg2.pset_uuid:
            msg = 'Property "{}" and "{}" are not part of the same PropertySet '.format(arg2.name, arg1.name)
            raise TypeError(msg)

    tmp_prop = copy.deepcopy(arg1)

    argument2 = None

    if isinstance(arg2, (int, float)):
        argument2 = numpy.full(tmp_prop.nr_objects, arg2)
    else:
        argument2 = arg2.values()

    for idx in range(0, tmp_prop.nr_objects):
        value = op(tmp_prop.values()[idx], argument2[idx])
        if cast_type == None:
            tmp_prop.values()[idx] = value
        else:
            tmp_prop.values()[idx] = value.astype(numpy.dtype(cast_type))

    return tmp_prop


def _AOpProp(number, arg2, op):
    tmp_prop = copy.deepcopy(arg2)

    argument1 = None

    if isinstance(number, (int, float)):
        argument1 = numpy.full(tmp_prop.nr_objects, number)

    for idx, i in enumerate(arg2.values()):
        tmp_prop.values()[idx] = op(argument1[idx], arg2.values()[idx])

    return tmp_prop


def log(property):
    """ Calculates the absolute value for each object the property values.

    :param property:
    :type property: Property
    :returns: a property with the absolute values
    :rtype: Property
    """
    return _PropOp(property, numpy.log)


def abs(property):
    """ Calculates the absolute value for each object the property values.

    :param property:
    :type property: Property
    :returns: a property with the absolute values
    :rtype: Property
    """
    return _PropOp(property, numpy.absolute)


def exp(property):
    """ Calculates the exponential for each object the property values.

    :param property:
    :type property: Property
    :returns: a property with the exponential values
    :rtype: Property
    """
    return _PropOp(property, numpy.exp)


def mul(self, other):
    """ Multiplication, equivalent to the * operator.

    The * operator multiplies for each object the property values of two properties.
    The properties must be from the same property set, or one argument can be a number.


    :param arg1: multiplier
    :type arg1: Property or number
    :param arg2: multiplicand
    :type arg2: Property or number
    :returns: a property with the product
    :rtype: Property
    """
    return _PropOpB(self, other, numpy.multiply)


def rmul(self, number):
    return mul(self, number)


def sub(self, other):
    """ Subtraction, equivalent to the - operator.

    The - operator subtracts for each object the property values of two properties.
    The properties must be from the same property set, or one argument can be a number.


    :param arg1: minuend
    :type arg1: Property or number
    :param arg2: subtrahend
    :type arg2: Property or number
    :returns: a property with the difference
    :rtype: Property
    """
    return _PropOpB(self, other, numpy.subtract)


def rsub(self, number):
    return _AOpProp(number, self, numpy.subtract)


def add(self, other):
    """ Addition, equivalent to the + operator.

    The + operator adds for each object the property values of two properties.
    The properties must be from the same property set, or one argument can be a number.


    :param arg1: summand
    :type arg1: Property or number
    :param arg2: summand
    :type arg2: Property or number
    :returns: a property with summed values
    :rtype: Property
    """

    return _PropOpB(self, other, numpy.add)


def radd(self, number):

    return add(self, number)


def divide(self, other):
    """ Division, equivalent to the / operator.

    The / operator divides for each object the property values of two properties.
    The properties must be from the same property set, or one argument can be a number.


    :param arg1: dividend
    :type arg1: Property or number
    :param arg2: divisor
    :type arg2: Property or number
    :returns: a property with the quotient
    :rtype: Property
    """
    return _PropOpB(self, other, numpy.divide)


def rdivide(self, number):

    return _AOpProp(number, self, numpy.divide)


def power(self, other):
    """ First property raised to the power of the second property. Equivalent to ‘**’.

    :param arg:
    :type arg: Property
    :returns: a property with the base raised to the power exponent
    :rtype: Property
    """
    return _PropOpB(self, other, numpy.power)


def rpower(self, number):

    return _AOpProp(number, self, numpy.power)


def neg(self):
    return -1 * self


def not_equal(self, other):
    """ Equivalent to the != operator.
    """
    return _PropOpB(self, other, numpy.not_equal, numpy.uint8)


def equal(self, other):
    """ Equivalent to the == operator.
    """
    return _PropOpB(self, other, numpy.equal, numpy.uint8)


def greater(self, other):
    """ Equivalent to the > operator.
    """
    return _PropOpB(self, other, numpy.greater, numpy.uint8)


def greater_equal(self, other):
    """ Equivalent to the >= operator.
    """
    return _PropOpB(self, other, numpy.greater_equal, numpy.uint8)


def less(self, other):
    """ Equivalent to the < operator.
    """
    return _PropOpB(self, other, numpy.less, numpy.uint8)


def less_equal(self, other):
    """ Equivalent to the <= operator.
    """
    return _PropOpB(self, other, numpy.less_equal, numpy.uint8)


def logical_and(self, other):
    return _PropOpB(self, other, numpy.logical_and, numpy.uint8)


def _bool(self):
    raise NotImplementedError

Property.__add__= add
Property.__radd__ = radd
Property.__sub__ = sub
Property.__rsub__ = rsub
Property.__mul__ = mul
Property.__rmul__ = rmul
Property.__truediv__  = divide
Property.__rtruediv__ = rdivide
Property.__pow__ = power
Property.__rpow__ = rpower

Property.__neg__ = neg

Property.__ne__ = not_equal
Property.__eq__ = equal
Property.__gt__ = greater
Property.__ge__ = greater_equal
Property.__lt__ = less
Property.__le__ = less_equal

Property.__bool__ = _bool