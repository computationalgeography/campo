from osgeo import gdal
from osgeo import osr
from osgeo import ogr
gdal.UseExceptions()
import math
import numpy as np
from campo.points import Points
from campo.areas import Areas
from campo.property import Property


def raster_values_to_feature(point_pset, field_pset, field_prop):
  ''' Queries the raster values of one field property on the location of point agents, 
  writes this as a new point agent property set 
  Parameters:
    point_pset: property set of the point agents to be attributed the location 
    field_pset: property set of a single field 
    field_prop: property of which the values are attributed to the newly generated point property
  Returns: 
    point_prop: property of point agents with values of local field values'''
  
  # generate empty point property given point property space definitions
  point_prop = Property('emptycreatename', point_pset.uuid, point_pset.space_domain, point_pset.shapes)
  
  # loop over space attributes of the different points in the point agents propertyset
  for pidx,coordinate in enumerate(point_pset.space_domain):
    point_x = point_pset.space_domain.xcoord[pidx]
    point_y = point_pset.space_domain.ycoord[pidx]

    point_value = np.zeros(1)  
    for fidx,area in enumerate(field_pset.space_domain):

      # get bounding box of field
      nr_cols = int(area[5]) # 
      minX = area [0]
      minY = area [1] 
      
      # translate point coordinate to index on the field array
      cellsize = math.fabs(area[2] - minX) / nr_cols 
      ix = math.floor((point_x - minX) / cellsize) 
      iy = math.floor((point_y - minY) / cellsize) 
      
      # reshape property to a mirrored numpy field array to accommodate right use of point and agent indexes 
      reshaped = np.flip (field_prop.values()[fidx], axis=0) 
      # query the field attribute given point location
      point_value[fidx] = reshaped[iy,ix] 

    # write the value to the point property for each point agent
    point_prop.values()[pidx] = point_value.item() 

  return point_prop