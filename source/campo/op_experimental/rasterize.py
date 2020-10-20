from osgeo import gdal
from osgeo import osr
from osgeo import ogr

import math



from ..points import Points
from ..areas import Areas
from ..property import Property








def feature_to_raster(field_pset, point_pset):


  spatial_ref = osr.SpatialReference()
  spatial_ref.ImportFromEPSG(28992)


  outdriver=ogr.GetDriverByName('MEMORY')
  source=outdriver.CreateDataSource('memData')
  tmp=outdriver.Open('memData', 1)
  lyr = source.CreateLayer('locations', geom_type=ogr.wkbPoint, srs=spatial_ref)


  for coordinate in point_pset.space_domain:
    feat = ogr.Feature(lyr.GetLayerDefn())
    feat.SetGeometry(ogr.CreateGeometryFromWkt('POINT({} {})'.format(float(coordinate[0]), float(coordinate[1]))))

    lyr.CreateFeature(feat)


  tmp_prop = Property('emptycreatename', field_pset.uuid, field_pset.space_domain, field_pset.shapes)

  for idx,area in enumerate(field_pset.space_domain):

    nr_rows = int(area[4])
    nr_cols = int(area[5])
    cellsize = cellsize = math.fabs(area[2] - area[0]) / nr_cols


    minX = area[0]
    maxY = area[3]


    target_ds = gdal.GetDriverByName('MEM').Create('', nr_cols, nr_rows, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((minX, cellsize, 0, maxY, 0, -cellsize))
    target_ds.SetProjection(spatial_ref.ExportToWkt())

    gdal.PushErrorHandler('CPLQuietErrorHandler')
    err = gdal.RasterizeLayer(target_ds, [1], lyr, burn_values=[1], options=['ALL_TOUCHED=TRUE'])
    gdal.PopErrorHandler()

    band = target_ds.GetRasterBand(1)
    array = band.ReadAsArray()

    tmp_prop.values()[idx] = array


  return tmp_prop

