from concurrent import futures
import copy
import numpy
import multiprocessing


from ..property import Property

import pcraster

def _spatial_operation(area_property, spatial_operation):


      for item_idx, item in enumerate(area_property.values):

        west = area_property.pset_domain.p1.xcoord[item_idx]
        north = area_property.pset_domain.p1.ycoord[item_idx]

        rows = int(area_property.pset_domain.row_discr[item_idx])
        cols = int(area_property.pset_domain.col_discr[item_idx])


        cellsize = (area_property.pset_domain.p2.xcoord[item_idx] - west ) / cols

        pcraster.setclone(rows, cols, cellsize, west, north)

        raster = pcraster.numpy2pcr( pcraster.Scalar, item.astype("float32"), numpy.nan)




def _new_property_from_property(area_property, multiplier):

  # make empty property

  new_prop = Property("_new_property_from_property_name", area_property._pset_uuid, area_property._pset_domain, area_property._shape)

  # attach propertyset domain if available
  #new_prop.pset_domain = area_property.pset_domain

  # obtain number, datatype and shape of value

  #new_prop.shape = area_property.shape
  #new_prop.dtype = area_property.dtype

  nr_items = area_property._shape[0]

  # create and attach new value to property
  dtype = area_property.values()[0].dtype
  values = numpy.ones(area_property._shape[0], dtype)#, area_property.dtype)

  new_prop.values().values = copy.deepcopy(area_property.values().values)

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

  for item_idx, item in enumerate(arg1_property.values()):

        _set_current_clone(arg1_property, item_idx)

        arg1_raster = pcraster.numpy2pcr(pcr_type, arg1_property.values()[item_idx], numpy.nan)
        arg2_raster = pcraster.numpy2pcr(pcr_type, arg2_property.values()[item_idx], numpy.nan)

        result_raster = spatial_operation(arg1_raster, arg2_raster)
        result_item = pcraster.pcr2numpy(result_raster, numpy.nan)

        result_prop.values()[item_idx] = result_item

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
#(idx, start_locationsvalues, frictiondistvalues, frictionvalues, clone)
  idx = values[0]
  start_locations_values = values[1]
  frictiondist_values = values[2]
  friction_values = values[3]
  clone = values[4]

  pcraster.setclone(clone[0], clone[1], clone[2], clone[3], clone[4])

  arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, start_locations_values, -999) #numpy.nan)
  frictiondist_raster = pcraster.numpy2pcr(pcraster.Scalar, frictiondist_values.astype("float32"), numpy.nan)
  friction_raster = pcraster.numpy2pcr(pcraster.Scalar, friction_values.astype("float32"), numpy.nan)
  result_raster = pcraster.spread(arg1_raster, frictiondist_raster, friction_raster)

  return idx, pcraster.pcr2numpy(result_raster, numpy.nan)


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
  https://pcraster.geo.uu.nl/pcraster/latest/documentation/pcraster_manual/sphinx/op_spread.html
  """


  result_prop = Property('emptyspreadname', start_locations.pset_uuid, start_locations.space_domain, start_locations.shapes)

  todo = []
  for idx in start_locations.values().values.keys():
    start_locations_values = start_locations.values().values[idx]
    frictiondist_values = frictiondist.values().values[idx]
    friction_values = friction.values().values[idx]

    west = start_locations.space_domain.p1.xcoord[idx]
    north = start_locations.space_domain.p1.ycoord[idx]
    rows = int(start_locations.space_domain.row_discr[idx])
    cols = int(start_locations.space_domain.col_discr[idx])
    cellsize = (start_locations.space_domain.p2.xcoord[idx] - west ) / cols

    clone = (rows, cols, cellsize, west, north)

    item = (idx, start_locations_values, frictiondist_values, friction_values, clone)
    todo.append(item)

  cpus = multiprocessing.cpu_count()
  tasks = len(todo)
  chunks = max(1, tasks // cpus)

  with futures.ProcessPoolExecutor(max_workers=cpus) as ex:
    results = ex.map(_pspread, todo, chunksize=chunks)

  for result in results:
    result_prop.values().values[result[0]] = result[1]

  return result_prop


  # sequential
  for idx in start_locations.values().values.keys():
    values = start_locations.values().values[idx]
    _set_current_clone(start_locations, idx)

    frictiondistvalues = frictiondist.values().values[idx]
    frictionvalues = friction.values().values[idx]

    arg1_raster = pcraster.numpy2pcr(pcraster.Nominal, values, -99999) #numpy.nan)
    frictiondist_raster = pcraster.numpy2pcr(pcraster.Scalar, frictiondistvalues.astype("float32"), numpy.nan)
    friction_raster = pcraster.numpy2pcr(pcraster.Scalar, frictionvalues.astype("float32"), numpy.nan)

    result_raster = pcraster.spread(arg1_raster, frictiondist_raster, friction_raster)
    result_item = pcraster.pcr2numpy(result_raster, numpy.nan)
    result_prop.values().values[idx] = result_item

  return result_prop

