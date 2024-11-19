import numpy as np
import random 
from pathlib import Path 
import sys
import campo
from sklearn.neighbors import NearestNeighbors
import math
import matplotlib.pyplot as plt

def find_closest_dest (field_pset, boolean_fieldprop, point_pset_orX, pidx_orY): 
    ''' find closest point complying to the boolean fieldprop, from a point
    if point_pset and pidx is inavailable, point_pset may be a xcoordinate  and pidx may be the ycoordinate 
    of the point of which a new destination needs to be found
    parameters: 
        boolean_fieldprop: a boolean map, either as a field-agent property or as a numpy array, describing with 1s the destination
        poi'''
    if isinstance(point_pset_orX, campo.propertyset.PropertySet): 
        point_x = point_pset_orX.space_domain.xcoord [pidx_orY]
        point_y = point_pset_orX.space_domain.ycoord [pidx_orY]
    elif isinstance (point_pset_orX, (np.int64, int, np.float64, float)):
        point_x = point_pset_orX
        point_y = pidx_orY
    else: 
        raise TypeError('make sure third and fourth argument give enough information to substract coordinates, by being a propertyset or integers describing coordinates')
    
    for fidx,area in enumerate(field_pset.space_domain):
      # Get bounding box of field
      nr_cols = int(area[5]) # 
      minX = area [0]
      minY = area [1]
      resolution =  math.fabs(area[2] - minX) / nr_cols

    ix = math.floor((point_x - minX) / resolution) # needs to be rouned down since we define it by the minimum and therefore lower border
    iy = math.floor((point_y - minY) / resolution)
    point = np.array([iy, ix]) # in indexes as in the field , with first row = y, column = x 
    
    # field proerty may be of type property or the values of such a property
    if isinstance (boolean_fieldprop, campo.property.Property):
        field_array = np.flip(boolean_fieldprop.values()[0])
        
    elif isinstance (boolean_fieldprop, np.ndarray): 
        field_array = np.flip (boolean_fieldprop, axis=0)
    else: 
        raise TypeError ('boolean_fieldprop needs to be of type campo.property or of a numpy array with same dimensions as field property values')
    boolean_array = np.where (field_array == 0, 0, 1) # in case it was not boolean yet 
    # Generate a list with all potential destinations, also accommodates for a clump field in which all possible destinations are not 0
    potential_dest_idxs = np.argwhere (boolean_array)
    
    # Convert indices to a 2D array of points 
    # Use NearestNeighbors to find the closest '1' 
    nbrs = NearestNeighbors (n_neighbors= 1, algorithm='ball_tree').fit(potential_dest_idxs)
    distances, indices = nbrs.kneighbors([point]) 
    # these indices are based on the flipped point, so the terugvertaling naar punt gaat dan niet meer, omdat het nu dus een geflipt punt is 
    # the flip operation however has to be performed, otherwise the topological relation is not correctly established 
    new_yidx, new_xidx= tuple(potential_dest_idxs[indices[0][0]]) # but now what do these indices mean on the non flipped array 
    xcoord = new_xidx*resolution + minX 
    ycoord = new_yidx*resolution + minY
    travel_distance = float(distances [0][0])*resolution 
    return xcoord, ycoord, travel_distance