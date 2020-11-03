import math
import pandas as pd
from osgeo import gdal
from osgeo import osr
import os
import subprocess
import tempfile
import numpy
import shutil

import lue.data_model as ldm

from ..dataframe import *
from ..utils import _color_message



def to_gpkg(dataframe, filename, crs=''):
  """
  """

  phen_name = dataframe.keys()

  for phen_name in dataframe.keys():
    phen = dataframe[phen_name]
    for pset_name in phen.keys():
      propset = dataframe[phen_name][pset_name]

      if propset['_campo_space_type'] == 'static_same_point':
        dfObj = pd.DataFrame()
        del dataframe[phen_name][pset_name]['_campo_space_type']

        for prop_name in propset.keys():
          dfObj['CoordX'] = dataframe[phen_name][pset_name][prop_name]['coordinates'].data[:, 0]
          dfObj['CoordY'] = dataframe[phen_name][pset_name][prop_name]['coordinates'].data[:, 1]

          for prop_name in propset.keys():
            prop = dataframe[phen_name][pset_name][prop_name]
            dfObj[prop_name] = prop['values'].data

        with tempfile.TemporaryDirectory() as tmpdir:
              layername, tail = os.path.splitext(os.path.basename(filename))

              csv_fname = os.path.join(tmpdir, f'{layername}.csv')
              csvt_fname = os.path.join(tmpdir, f'{layername}.csvt')

              columns = []
              for c in dfObj:
                if dfObj[c].dtype.kind == 'f':
                  columns.append('Real')
                elif dfObj[c].dtype.kind == 'i':
                  columns.append('Integer')
                else:
                  columns.append('String')

              columns = ','.join(map(str, columns))
              with open(csvt_fname, 'w') as content:
                content.write(columns)

              dfObj.to_csv(csv_fname, index=False)

              s_srs = ''
              t_srs = ''
              if crs != '':
                s_srs = f'-s_srs {crs}'
                t_srs = f'-t_srs {crs}'


              cmd = f'ogr2ogr {s_srs} {t_srs} -oo X_POSSIBLE_NAMES=CoordX -oo Y_POSSIBLE_NAMES=CoordY -f GPKG {filename} {csv_fname}'
              subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)

      #elif propset['_campo_space_type'] == 'static_same_field':
        #raise NotImplementedError
      #elif propset['_campo_space_type'] == 'static_diff_field':
        #raise NotImplementedError
      else:
        msg = _color_message('Only for static point agents')
        raise TypeError(msg)

def to_tiff(dataframe, crs='', directory=''):



  for phen_name in dataframe.keys():
    phen = dataframe[phen_name]
    for pset_name in phen.keys():
      propset = dataframe[phen_name][pset_name]
      if propset['_campo_space_type'] == 'static_same_point':# or propset['_campo_space_type'] == 'diff_same_point':
        msg = _color_message('Only for field agents')
        raise TypeError(msg)

      del dataframe[phen_name][pset_name]['_campo_space_type']

      for prop_name in propset.keys():
        objects = dataframe[phen_name][pset_name][prop_name]

        for obj_id in objects:
          obj = objects[obj_id]

          rows = obj.values.shape[0]
          cols = obj.values.shape[1]
          cellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)

          data = obj.data
          xmin = obj.xcoord[0].values.item()
          ymax = obj.ycoord[-1].values.item()
          geotransform = (xmin, cellsize, 0, ymax, 0, -cellsize)

          fname = os.path.join(directory, f'{prop_name}_{obj_id}.tiff')

          dtype = None
          if data.dtype.kind == 'f':
            dtype = gdal.GDT_Float32
          elif data.dtype.kind == 'i':
            dtype = gdal.GDT_Int32
          elif data.dtype.kind == 'u':
            dtype = gdal.GDT_Byte
          else:
            raise NotImplementedError


          dst_ds = gdal.GetDriverByName('GTiff').Create(fname, cols, rows, 1, dtype)
          dst_ds.SetGeoTransform(geotransform)

          if crs != '':
            aut, code = crs.split(':')
            if aut != 'EPSG':
              msg = _color_message('Provide CRS as EPSG code, e.g."EPSG:4326"')
              raise TypeError(msg)

            srs = osr.SpatialReference()
            srs.ImportFromEPSG(int(code))
            dst_ds.SetProjection(srs.ExportToWkt())

          dst_ds.GetRasterBand(1).WriteArray(data)
          dst_ds = None




def to_csv(frame, filename):

  phen_name = frame.keys()

  dfObj = pd.DataFrame()

  for phen_name in frame.keys():
    phen = frame[phen_name]
    for pset_name in phen.keys():
      propset = frame[phen_name][pset_name]

      for prop_name in propset.keys():
        dfObj['x'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 0]
        dfObj['y'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 1]


      for prop_name in propset.keys():
        prop = frame[phen_name][pset_name][prop_name]

        dfObj[prop_name] = prop['values'].data

  dfObj.to_csv(filename, index=False)



def create_point_pdf(frame, filename):

  phen_name = frame.keys()

  wdir = os.getcwd()
  data_dir = os.path.join(wdir,'data')

  tmp_csv = os.path.join(data_dir, 'agents.csv')


  phen_name = frame.keys()

  dfObj = pd.DataFrame()

  for phen_name in frame.keys():
    phen = frame[phen_name]
    for pset_name in phen.keys():
      propset = frame[phen_name][pset_name]

      for prop_name in propset.keys():
        dfObj['x'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 0]
        dfObj['y'] = frame[phen_name][pset_name][prop_name]['coordinates'].data[:, 1]


      for prop_name in propset.keys():
        prop = frame[phen_name][pset_name][prop_name]

        dfObj[prop_name] = prop['values'].data

  dfObj.to_csv(tmp_csv, index=False)

  gpkg_fname_out = os.path.join(data_dir, 'agents.gpkg')

  cmd = 'ogr2ogr -s_srs EPSG:28992 -t_srs EPSG:28992 -oo X_POSSIBLE_NAMES=x -oo Y_POSSIBLE_NAMES=y -f GPKG {} {}'.format(gpkg_fname_out, tmp_csv)

  subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)


  cmd = 'gdal_translate -of PDF -a_srs EPSG:28992 data/clone.tiff points.pdf -co OGR_DATASOURCE=out.vrt'

  clone_path = os.path.join(data_dir, 'clone.tiff')
  vrt_path = os.path.join(data_dir, 'sources.vrt')
  cmd = 'gdal_translate -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={}'.format(clone_path, filename, vrt_path)


  subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)




def create_field_pdf(frame, filename):

  phen_name = frame.keys()

  wdir = os.getcwd()
  data_dir = os.path.join(wdir,'data')

  tmpdir = 'tmp'
  if os.path.exists(tmpdir):
    shutil.rmtree(tmpdir)

  os.mkdir(tmpdir)


  #with tempfile.TemporaryDirectory() as tmpdir:
  fnames = []
  lnames = []

  for phen_name in frame.keys():
    phen = frame[phen_name]
    for pset_name in phen.keys():
      propset = frame[phen_name][pset_name]

      for prop_name in propset.keys():

        objects = frame[phen_name][pset_name][prop_name]

        for obj_id in objects:
          obj = objects[obj_id]

          rows = obj.values.shape[0]
          cols = obj.values.shape[1]
          cellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)

          data = obj.data
          data = data/(data.max()/250.0)
          xmin = obj.xcoord[0].values.item()
          ymax = obj.ycoord[-1].values.item()
          geotransform = (xmin, cellsize, 0, ymax, 0, -cellsize)

          fname = os.path.join(tmpdir, '{:03d}'.format(obj_id))
          #fname = os.path.join('{:03d}'.format(obj_id))
          fnames.append(fname)
          lnames.append('shop{:03d}'.format(obj_id))


          dst_ds = gdal.GetDriverByName('GTiff').Create(fname, cols, rows, 1, gdal.GDT_Byte)
          dst_ds.SetGeoTransform(geotransform)
          srs = osr.SpatialReference()
          srs.ImportFromEPSG(28992)
          dst_ds.SetProjection(srs.ExportToWkt())
          dst_ds.GetRasterBand(1).WriteArray(data)
          dst_ds = None


  outfile = os.path.join(wdir, filename)
  clone = os.path.join(data_dir, 'clone.tiff')
  roads = os.path.join(data_dir, 'roads.gpkg')
  roads = os.path.join(data_dir, 'sources.vrt')

  rasters = ','.join(fnames)
  names = ','.join(lnames)


  cmd = 'gdal_translate -q -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={} -co OGR_DISPLAY_FIELD="roads" -co EXTRA_RASTERS={} -co EXTRA_RASTERS_LAYER_NAME={} -co OFF_LAYERS={}'.format(clone, outfile,roads,rasters,names,names )
  #cmd = 'gdal_translate -q -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={} -co OGR_DISPLAY_FIELD="roads" -co EXTRA_RASTERS={} -co EXTRA_RASTERS_LAYER_NAME={}'.format(clone, outfile,roads,rasters,names)
  cmd = 'gdal_translate -q -of PDF -a_srs EPSG:28992 {} {} -co OGR_DATASOURCE={} -co EXTRA_RASTERS={} -co EXTRA_RASTERS_LAYER_NAME={}'.format(clone, outfile,roads,rasters,names)

  subprocess.check_call(cmd, shell=True, stdout=subprocess.DEVNULL)
  shutil.rmtree(tmpdir)
