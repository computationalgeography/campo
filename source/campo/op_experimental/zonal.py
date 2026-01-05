from osgeo import gdal
from osgeo import osr
from osgeo import ogr

gdal.UseExceptions()

import math
import numpy as np

from campo.points import Points
from campo.areas import Areas
from campo.property import Property

def zonal_values_to_feature(point_pset, field_pset, field_prop_class, field_prop_var, operation):
  ''' Queries aggregative raster values of a zone of a field property based on the location
    of point agents within a classification map, given a certain aggregative operation. 
    Writes this as a new point agent property. Only works for one fieldagent existing at the location. 
    Fieldagents with overlapping domains cannot generate an output
    E.g.: According to both the agent's location and a soil map (field_prop_class), the agent is positioned in 
        soil '2' , which is clay. With the operation 'mean', the mean rainfall (from field_prop_var) 
        is calculated and attributed to the agent
  Parameters:
    point_pset: property set of the point agents to be attributed the location 
    field_pset: property set of a single field 
    field_prop_class: property describing classes or groups of cells of which the zonal extent shall be the windowsize of the aggregration
    field_prop_var: property describing the variable which needs to be aggregated,
      in case of a boolean map, 'True' values are 1
    operation: operation: aggregative numpy operation as a string ('sum', 'mean', 'min', 'max', 'etc')
  Returns: 
    point_prop: property of point agents with values of aggregated field values'''
  
  # Generate operator, first checking if operation is available in numpy
  if not hasattr (np, operation):
    raise ValueError (f'Unsupported numpy operation, {operation}')
  operator = getattr(np, operation)

  # Identifying the zone the agent is in
  agents_zoneIDs = raster_values_to_feature(point_pset,field_pset, field_prop_class)
  # Generate empty point property given point property space definitions
  point_prop = Property('emptycreatename', point_pset.uuid, point_pset.space_domain, point_pset.shapes)
  # make as many field properties as there are agents:  
  # Loop over space attributes of the different points in the point agents propertyset
  for pidx, ID in enumerate(agents_zoneIDs.values()):
    # Making a boolean map concerning the extent of the zone for each agent
    aggr_zone_var = np.zeros(1)
    for fidx,area in enumerate(field_pset.space_domain):
        zone_extent = np.where (field_prop_class.values()[fidx] == ID, 1, 0)
        variable_zone_array = np.multiply (zone_extent, field_prop_var.values()[fidx])
        # we don't need to flip this time, since the raster_values_to_feature already gave 
        # the right topological relationship between the field and the agent: 
        # the zone_extent array describes the zone in which the agent is positioned. 
        # This array might be flipped, but this won't lead to any different outcomes of aggregative operations
        aggr_zone_var[fidx] = operator (variable_zone_array)
    #field_prop_array [pidx] = field_prop# array as long as the number of agents filled with a field prop for each agent
    # Write the value to the point property for each point agent
    point_prop.values()[pidx] = aggr_zone_var.item() 
    
  return point_prop