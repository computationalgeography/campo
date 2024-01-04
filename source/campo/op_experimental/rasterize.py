from osgeo import gdal
from osgeo import osr
from osgeo import ogr

gdal.UseExceptions()

import math
import numpy as np

from ..property import Property


def feature_to_raster(field_pset, point_pset):

    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromEPSG(28992)

    ogr_source=ogr.GetDriverByName('MEMORY').CreateDataSource('memSource')

    tmp_prop = Property('emptycreatename', field_pset.uuid, field_pset.space_domain, field_pset.shapes)

    for idx, area in enumerate(field_pset.space_domain):
        # Point feature for current location
        point_x = point_pset.space_domain.xcoord[idx]
        point_y = point_pset.space_domain.ycoord[idx]

        layername = 'locations'
        if ogr_source.GetLayerByName(layername):
            ogr_source.DeleteLayer(layername)

        lyr = ogr_source.CreateLayer(layername, geom_type=ogr.wkbPoint, srs=spatial_ref)

        feat = ogr.Feature(lyr.GetLayerDefn())
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(point_x, point_y)
        feat.SetGeometry(point)

        lyr.CreateFeature(feat)

        # Raster
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


def feature_to_raster_all(field_pset, point_pset):

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

    for idx, area in enumerate(field_pset.space_domain):

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


def feature_values_to_raster(field_pset, point_pset, point_prop):

    tmp_prop = Property('emptycreatename', field_pset.uuid, field_pset.space_domain, field_pset.shapes)

    for idx, area in enumerate(field_pset.space_domain):

        nr_rows = int(area[4])
        nr_cols = int(area[5])

        raster = np.zeros((nr_rows *  nr_cols))

        for pidx, coordinate in enumerate(point_pset.space_domain):
            raster[pidx] = point_prop.values()[pidx][0]

        tmp_prop.values()[idx] = raster.reshape((nr_rows, nr_cols))

    return tmp_prop



