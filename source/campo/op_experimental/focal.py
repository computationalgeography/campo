import copy
import numpy

from osgeo import gdal
from osgeo import ogr
from osgeo import osr


from ..property import Property
from ..points import Points
from ..areas import Areas


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
