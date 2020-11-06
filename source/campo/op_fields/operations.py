import os
import numpy
import multiprocessing
import datetime

import pcraster

from ..property import Property



def _spatial_operation(area_property, spatial_operation):


      for item_idx, item in enumerate(area_property.values):

        west = area_property.pset_domain.p1.xcoord[item_idx]
        north = area_property.pset_domain.p1.ycoord[item_idx]

        rows = int(area_property.pset_domain.row_discr[item_idx])
        cols = int(area_property.pset_domain.col_discr[item_idx])


        cellsize = (area_property.pset_domain.p2.xcoord[item_idx] - west ) / cols

        pcraster.setclone(rows, cols, cellsize, west, north)

        raster = pcraster.numpy2pcr( pcraster.Scalar, item,numpy.nan)




def _new_property_from_property(area_property, multiplier):

  # make empty property
  new_prop = Property()

  fame.lue_property.Property(property_set._phen, property_set.shapes, property_set.uuid, property_set._domain, property_set.time_discretization)

  # attach propertyset domain if available
  new_prop.pset_domain = area_property.pset_domain

  # obtain number, datatype and shape of value

  new_prop.shape = area_property.shape
  new_prop.dtype = area_property.dtype

  nr_items = area_property.shape[0]

  # create and attach new value to property
  values = numpy.ones(area_property.shape, area_property.dtype)

  #
  new_prop.values = values



  return new_prop





def _set_current_clone(area_property, item_idx):

    west = area_property.space_domain.p1.xcoord[item_idx]
    north = area_property.space_domain.p1.ycoord[item_idx]

    rows = int(area_property.space_domain.row_discr[item_idx])
    cols = int(area_property.space_domain.col_discr[item_idx])


    cellsize = (area_property.space_domain.p2.xcoord[item_idx] - west ) / cols

    pcraster.setclone(rows, cols, cellsize, west, north)




def _spatial_operation_one_argument(area_property, spatial_operation, pcr_type):


  # generate a property to store the result
  result_prop = _new_property_from_property(area_property, 0.0)



  for item_idx, item in enumerate(area_property.values):


        _set_current_clone(area_property, item_idx)


        arg_raster = pcraster.numpy2pcr(pcr_type, item, numpy.nan)

        result_raster = spatial_operation(arg_raster)
        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values[item_idx] = result_item



  return result_prop





def _spatial_operation_two_arguments(arg1_property, arg2_property, spatial_operation, pcr_type):



  # generate a property to store the result
  result_prop = _new_property_from_property(arg1_property, 0.0)



  for item_idx, item in enumerate(arg1_property.values):

        _set_current_clone(arg1_property, item_idx)


        arg1_raster = pcraster.numpy2pcr(pcr_type, arg1_property.values[item_idx], numpy.nan)
        arg2_raster = pcraster.numpy2pcr(pcr_type, arg2_property.values[item_idx], numpy.nan)


        result_raster = spatial_operation(arg1_raster, arg2_raster)

        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values[item_idx] = result_item



  return result_prop












def slope(area_property):
  """ """
  return _spatial_operation_one_argument(area_property, pcraster.slope, pcraster.Scalar)


def window4total(area_property):
  """ """
  return _spatial_operation_one_argument(area_property, pcraster.window4total, pcraster.Scalar)


def windowtotal(area_property, window_size):
  """ """

  if not isinstance(window_size, Property):
    window_size =_new_property_from_property(area_property, window_size)

  return _spatial_operation_two_arguments(area_property, window_size, pcraster.windowtotal, pcraster.Scalar)


def _pspread(values):
  #(idx, result_prop, start_locations, arg1_raster, frictiondist_raster, friction_raster)

  idx = values[0]
  result_prop = values[1]
  start_locations = values[2]
  raster_values = values[3]
  frictiondist_values = values[4]
  friction_values = values[5]


  _set_current_clone(start_locations, idx)

  arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, raster_values, -999) #numpy.nan)
  frictiondist_raster = pcraster.numpy2pcr(pcraster.Scalar, frictiondist_values, numpy.nan)
  friction_raster = pcraster.numpy2pcr(pcraster.Scalar, friction_values, numpy.nan)
  result_raster = pcraster.spread(arg1_raster, frictiondist_raster, friction_raster)
  result_item = pcraster.pcr2numpy(result_raster, numpy.nan)
  result_prop.values().values[idx] = result_item


def spread(start_locations, frictiondist, friction):
  """ Total friction of the shortest accumulated friction path over a map with friction values from a source cell to cell under consideration

  :param start_locations: starting locations
  :type start_locations:  Property
  :param frictiondist: initial friction
  :type frictiondist: Property
  :param friction: friction per cell
  :type friction: Property
  :returns: a property with total friction values
  :rtype: Property

  For concepts of this operation calculated on each agent see
  https://pcraster.geo.uu.nl/pcraster/4.3.0/documentation/pcraster_manual/sphinx/op_spread.html
  """


  result_prop = Property('emptyspreadname', start_locations.pset_uuid, start_locations.space_domain, start_locations.shapes)

  pool = multiprocessing.Pool(multiprocessing.cpu_count() - 1)

  todo = []
  for idx in start_locations.values().values.keys():
    values = start_locations.values().values[idx]
    _set_current_clone(start_locations, idx)

    frictiondistvalues = frictiondist.values().values[idx]
    frictionvalues = friction.values().values[idx]


    item = (idx, result_prop, start_locations, values, frictiondistvalues, frictionvalues)
    todo.append(item)

  pool.map(_pspread, todo, chunksize=1)

  return result_prop

  for idx in start_locations.values().values.keys():
    values = start_locations.values().values[idx]
    _set_current_clone(start_locations, idx)

    frictiondistvalues = frictiondist.values().values[idx]
    frictionvalues = friction.values().values[idx]

    arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, values, -999) #numpy.nan)
    frictiondist_raster = pcraster.numpy2pcr(pcraster.Scalar, frictiondistvalues, numpy.nan)
    friction_raster = pcraster.numpy2pcr(pcraster.Scalar, frictionvalues, numpy.nan)

    result_raster = pcraster.spread(arg1_raster, frictiondist_raster, friction_raster)
    result_item = pcraster.pcr2numpy(result_raster, numpy.nan)
    result_prop.values().values[idx] = result_item

  return result_prop

