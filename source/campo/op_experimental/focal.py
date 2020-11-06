import copy
import numpy
import math
import sys
import multiprocessing
import datetime

from osgeo import gdal
from osgeo import ogr
from osgeo import osr

import pcraster


from ..property import Property
from ..points import Points
from ..areas import Areas
from ..utils import _color_message


def agents_average(prop):
  """returns average value of property values """
  if not isinstance(prop, Property):
    raise NotImplementedError

  if not isinstance(prop.space_domain, Points):
    raise NotImplementedError

  tmp_prop = copy.deepcopy(prop)
  nr_objects = tmp_prop.nr_objects

  tmp = numpy.zeros(nr_objects)

  for i in range(0, nr_objects):
    tmp[i] = tmp_prop.values()[i]

  tmp_values = numpy.average(tmp)

  for i in range(0, nr_objects):
    tmp_prop.values()[i] = tmp_values

  return tmp_prop

def get_others(start_prop, dest_prop, buffer_size):
  # re-use the previous approach to obtain the neighbours within a buffer
  values = numpy.zeros((len(start_prop.space_domain),len(dest_prop.space_domain)), dtype=numpy.int8)

  spatial_ref = osr.SpatialReference()
  spatial_ref.ImportFromEPSG(28992)

  memdriver = ogr.GetDriverByName('MEMORY')
  ds = memdriver.CreateDataSource('tmp.gpkg')

  # Destination layer
  lyr_dest = ds.CreateLayer('uid', geom_type=ogr.wkbPoint, srs=spatial_ref)
  field = ogr.FieldDefn('uid', ogr.OFTInteger)
  lyr_dest.CreateField(field)


  # Plain storing of object order (id)
  for idx, p in enumerate(dest_prop.space_domain):
    point = ogr.Geometry(ogr.wkbPoint)

    point.AddPoint(p[0], p[1])
    feat = ogr.Feature(lyr_dest.GetLayerDefn())
    feat.SetGeometry(point)

    feat.SetField('uid', idx)

    lyr_dest.CreateFeature(feat)


  lyr_dest = None
  lyr_dest = ds.GetLayer('uid')


  for idx, p in enumerate(start_prop.space_domain):

    lyr_shop = ds.CreateLayer('destination_locations', geom_type=ogr.wkbPoint, srs=spatial_ref)
    # just a round buffer
    lyr_dist = ds.CreateLayer('source_buffer', geom_type=ogr.wkbPolygon, srs=spatial_ref)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(p[0], p[1])
    poly = point.Buffer(float(buffer_size.values()[idx]))
    feat = ogr.Feature(lyr_dist.GetLayerDefn())
    feat.SetGeometry(poly)
    lyr_dist.CreateFeature(feat)


    lyr_dest.SetSpatialFilter(poly)

    lyr_dest.Clip(lyr_dist, lyr_shop, options=['SKIP_FAILURES=NO'])

    for target in lyr_shop:

        uid = target.GetField('uid')
        values[idx, uid] = 1

  return values




def focal_average_others(start_prop, dest_prop, value_prop, buffer_size, default_value, ret_prop):
  # start_prop carries start locations
  # dest_prop value layer to obtain neighbour values

  tmp_prop = copy.deepcopy(ret_prop)



  # Brute assumption here for the CRS, this should be in the dataset itself somewhere...
  spatial_ref = osr.SpatialReference()
  spatial_ref.ImportFromEPSG(28992)

  # First we make a point feature with houses
  name = 'houses'

  geo_out = 'foodenv.gpkg'
  # ds = ogr.GetDriverByName('GPKG').CreateDataSource(geo_out)



  memdriver = ogr.GetDriverByName('MEMORY')
  ds = memdriver.CreateDataSource(geo_out)










  # Second we make a point feature from which we will obtain the values
  # Holding all objects
  lyr_stores = ds.CreateLayer('values', geom_type=ogr.wkbPoint, srs=spatial_ref)


  field = ogr.FieldDefn('value', ogr.OFTReal)
  lyr_stores.CreateField(field)


  # ToDo: Here we need to get the object ids, actually...
  for idx, p in enumerate(dest_prop):#.pset_domain):
    point = ogr.Geometry(ogr.wkbPoint)

    point.AddPoint(p[0], p[1])
    feat = ogr.Feature(lyr_stores.GetLayerDefn())
    feat.SetGeometry(point)

    val = value_prop.values()[idx]
    feat.SetField('value', val)

    lyr_stores.CreateFeature(feat)


  lyr_stores = None
  lyr_stores = ds.GetLayer('values')

  default_value = default_value.values()[0]#,...]
  # For each object in point locations:
  c = 0
  for idx, p in enumerate(start_prop): #.pset_domain:

    lyr_shop = ds.CreateLayer('destination_locations', geom_type=ogr.wkbPoint, srs=spatial_ref)
    # just a round buffer
    lyr_dist = ds.CreateLayer('source_buffer', geom_type=ogr.wkbPolygon, srs=spatial_ref)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(p[0], p[1])
    poly = point.Buffer(float(buffer_size.values()[idx]))
    feat = ogr.Feature(lyr_dist.GetLayerDefn())
    feat.SetGeometry(poly)
    lyr_dist.CreateFeature(feat)


    lyr_stores.SetSpatialFilter(poly)

    lyr_stores.Clip(lyr_dist, lyr_shop, options=['SKIP_FAILURES=NO'])

    shops_within = lyr_shop.GetFeatureCount()

    object_value = 0.0
    if shops_within == 0:
      object_value = default_value
    else:
      val = 0.0
      fcount = 0
      for shop_feat in lyr_shop:
        val += shop_feat.GetField('value')
        fcount += 1

      object_value = val / fcount

    tmp_prop.values()[idx] = object_value

    ds.DeleteLayer('destination_locations')
    ds.DeleteLayer('source_buffer')


  return tmp_prop





def _focal_agents(values):
#(idx, tmp_prop, nr_locs, values_weight, extent)
      idx = values[0]
      tmp_prop = values[1]
      nr_locs = values[2]
      values_weight = values[3]
      extent = values[4]
      spatial_ref = values[5]
      lyr_dst = values[6]
      operation = values[7]
      fail = values[8]

      point_values = numpy.empty(nr_locs)
      point_values.fill(numpy.nan)

      # Raster for points to query
      nr_rows = extent[4]
      nr_cols = extent[5]
      cellsize = math.fabs(extent[2] - extent[0]) / nr_cols


      minX = extent[0]
      maxY = extent[3]

      #if ds.GetLayerByName('extent'):
      #      ds.DeleteLayer('extent')
      #ds.DeleteLayer('extent')

      ds_extent = ogr.GetDriverByName('MEMORY').CreateDataSource('ds_extent')

      extent_lyr = ds_extent.CreateLayer('extent', geom_type=ogr.wkbPolygon,  srs=spatial_ref)
      assert extent_lyr

      feat = ogr.Feature(extent_lyr.GetLayerDefn())

      ring = ogr.Geometry(ogr.wkbLinearRing)

      ring.AddPoint(minX, maxY)
      ring.AddPoint(minX + nr_cols * cellsize, maxY)
      ring.AddPoint(minX + nr_cols * cellsize, maxY - nr_rows * cellsize)
      ring.AddPoint(minX, maxY - nr_rows * cellsize)
      ring.AddPoint(minX, maxY)

      poly = ogr.Geometry(ogr.wkbPolygon)
      poly.AddGeometry(ring)

      feat.SetGeometry(poly)
      extent_lyr.CreateFeature(feat)

      #if ds.GetLayerByName('intersect'):
      #      ds.DeleteLayer('intersect')

      intersect_layer = ds_extent.CreateLayer('locations', geom_type=ogr.wkbPoint, srs=spatial_ref)
      assert intersect_layer

      lyr_dst.Intersection(extent_lyr, intersect_layer)

      pcraster.setclone(nr_rows, nr_cols, cellsize, minX, maxY)

      raster = pcraster.numpy2pcr(pcraster.Scalar, values_weight, numpy.nan)

      point_values.fill(numpy.nan)

      for idx, feature in enumerate(intersect_layer):
        x = feature.GetGeometryRef().GetX()
        y = feature.GetGeometryRef().GetY()

        mask_value, valid = pcraster.cellvalue_by_coordinates(raster, x, y)
        agent_value = feature.GetField('value')
        point_values[idx] = mask_value * agent_value

      indices = ~numpy.isnan(point_values)
      masked = point_values[indices]

      res = 0
      if operation == 'average':
        res = numpy.average(masked)
      elif operation == 'sum':
        res = numpy.sum(masked)
      else:
        raise NotImplementedError

      if fail == True:
        assert res != 0

      tmp_prop.values()[idx] = res




def focal_agents(dest, weight, source, operation='average', fail=False):
    """

    dest: point property set (determines property return type)

    weight: field property (weight/mask)

    source: point property (values to gather from)

    operation: type of operation, being 'average' (default), 'sum'
    """


    # hack rename...
    source_point = dest
    source_field = weight
    dest_prop = source

    if not isinstance(source_point.space_domain, Points):
      msg = _color_message(f'Property "{source_point.name}" must be of domain type Point')
      raise TypeError(msg)

    if not isinstance(source_field.space_domain, Areas):
      msg = _color_message(f'Property "{source_field.name}" must be of domain type Area')
      raise TypeError(msg)

    if not isinstance(dest_prop.space_domain, Points):
      msg = _color_message(f'Property "{dest_prop.name}" must be of domain type Point')
      raise TypeError(msg)

    dst_crs = source_point.space_domain.epsg
    field_crs = source_field.space_domain.epsg
    point_crs = dest_prop.space_domain.epsg

    cnt = 1
    for arg in [dst_crs, field_crs, point_crs]:
      if not arg:
        msg = _color_message(f'Operation requires a CRS, set the EPSG code of the phenomenon (argument {cnt})')
        raise ValueError(msg)
      cnt += 1

    if field_crs != point_crs:
      msg = _color_message(f'Incompatible CRS {field_crs} != {point_crs}')
      raise ValueError(msg)

    assert dst_crs == field_crs


    pp = next(iter(source_point._properties))
    tmp_prop = copy.deepcopy(source_point._properties[pp])



    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(point_crs)


    ds = ogr.GetDriverByName('MEMORY').CreateDataSource('mem')

    # Second we make a point feature from which we will obtain the locations
    # Holding all objects
    lyr_dst = ds.CreateLayer('locations', geom_type=ogr.wkbPoint, srs=spatial_ref)

    field = ogr.FieldDefn('value', ogr.OFTReal)
    lyr_dst.CreateField(field)


    for idx, p in enumerate(dest_prop.space_domain):
      point = ogr.Geometry(ogr.wkbPoint)

      point.AddPoint(p[0], p[1])
      feat = ogr.Feature(lyr_dst.GetLayerDefn())
      feat.SetGeometry(point)

      try:
        val = dest_prop.values()[idx][0]
      except:
        val = dest_prop.values()[idx]

      feat.SetField('value', float(val))

      lyr_dst.CreateFeature(feat)

    lyr_dst = None
    lyr_dst = ds.GetLayer('locations')



    nr_locs = dest_prop.nr_objects

    todos = []
    for idx, p in enumerate(source_point.space_domain):
      values_weight = source_field.values()[idx]

      extent = source_field.space_domain._extent(idx)

      item = (idx, tmp_prop, nr_locs, values_weight, extent, spatial_ref, lyr_dst, operation, fail)
      todos.append(item)

    cpus = multiprocessing.cpu_count()
    tasks = len(todos)
    chunks = max(cpus, int(tasks / cpus))
    pool = multiprocessing.Pool(cpus)
    pool.imap(_focal_agents, todos, chunksize=chunks)

    #_focal_agents(todos[0])

    return tmp_prop
    # sequential #

    nr_locs = dest_prop.nr_objects

    point_values = numpy.empty(nr_locs)
    point_values.fill(numpy.nan)

    for idx, p in enumerate(source_point.space_domain):
      values_weight = source_field.values()[idx]

      extent = source_field.space_domain._extent(idx)


      # Raster for points to query
      nr_rows = extent[4]
      nr_cols = extent[5]
      cellsize = math.fabs(extent[2] - extent[0]) / nr_cols


      minX = extent[0]
      maxY = extent[3]

      #if ds.GetLayerByName('extent'):
      #      ds.DeleteLayer('extent')
      #ds.DeleteLayer('extent')

      ds_extent = ogr.GetDriverByName('MEMORY').CreateDataSource('ds_extent')

      extent_lyr = ds_extent.CreateLayer('extent', geom_type=ogr.wkbPolygon,  srs=spatial_ref)

      feat = ogr.Feature(extent_lyr.GetLayerDefn())

      ring = ogr.Geometry(ogr.wkbLinearRing)

      ring.AddPoint(minX, maxY)
      ring.AddPoint(minX + nr_cols * cellsize, maxY)
      ring.AddPoint(minX + nr_cols * cellsize, maxY - nr_rows * cellsize)
      ring.AddPoint(minX, maxY - nr_rows * cellsize)
      ring.AddPoint(minX, maxY)

      poly = ogr.Geometry(ogr.wkbPolygon)
      poly.AddGeometry(ring)

      feat.SetGeometry(poly)
      extent_lyr.CreateFeature(feat)

      #if ds.GetLayerByName('intersect'):
      #      ds.DeleteLayer('intersect')

      intersect_layer = ds_extent.CreateLayer('locations', geom_type=ogr.wkbPoint, srs=spatial_ref)

      lyr_dst.Intersection(extent_lyr, intersect_layer)

      pcraster.setclone(nr_rows, nr_cols, cellsize, minX, maxY)

      raster = pcraster.numpy2pcr(pcraster.Scalar, values_weight, numpy.nan)

      point_values.fill(numpy.nan)

      for idx, feature in enumerate(intersect_layer):
        x = feature.GetGeometryRef().GetX()
        y = feature.GetGeometryRef().GetY()

        mask_value, valid = pcraster.cellvalue_by_coordinates(raster, x, y)
        agent_value = feature.GetField('value')
        point_values[idx] = mask_value * agent_value

      indices = ~numpy.isnan(point_values)
      masked = point_values[indices]

      res = 0
      if operation == 'average':
        res = numpy.average(masked)
      elif operation == 'sum':
        res = numpy.sum(masked)
      else:
        raise NotImplementedError

      if fail == True:
        assert res != 0

      tmp_prop.values()[idx] = res


    return tmp_prop




def where(condition, property1, property2):
  """ returns property1 for true condition, property2 otherwise
  """

  if not isinstance(condition, Property):
      msg = _color_message('condition must be of type Property')
      raise TypeError(msg)
  if not isinstance(property1, Property):
      msg = _color_message('property1 must be of type Property')
      raise TypeError(msg)
  if not isinstance(property2, Property):
      msg = _color_message('property2 must be of type Property')
      raise TypeError(msg)


  allowed = numpy.array([0, 1])
  for item in condition.values().values:
      condition_val = condition.values()[item]
      assert numpy.dtype(condition_val.dtype) == numpy.uint8, f'{condition_val.dtype} != numpy.uint8'
      diff = numpy.setdiff1d(condition_val, allowed)
      assert len(diff) == 0, 'Only 0 and 1 values allowed for condition'

  tmp_prop = copy.deepcopy(property1)

  for item in condition.values().values:
    cval = condition.values()[item]
    tval = property1.values()[item].astype(numpy.float64)
    fval = property2.values()[item]
    tmp_prop.values()[item] = numpy.where(cval, tval, fval)

  return tmp_prop
