import numpy as np
import random 
from pathlib import Path 
import sys
from field_agent.field_agent_interactions import raster_values_to_feature, zonal_values_to_feature
import campo
import math
import matplotlib.pyplot as plt

def randommove_to_boolean (boolean_fieldprop, field_pset, point_prop):
    '''
    - boolean_fieldprop = a property that is a field and contains true values for places where an agent may move to   
    - field_pset = a property set describing the domain of the field of the study area (Type: propertyset)
    - point_propset = the property set that has the move (= point agents)
    - nragents = the number of point agents 
    return lists of coordinates with the same length as the number of agents in a point propertyset (sueful wehn you want to make them move there) 
    '''
    # need to flip again because when calculating with this map points have different orientation than field (see rerasterize)
    if isinstance(boolean_fieldprop, np.ndarray):
        map_flipped = np.flip (boolean_fieldprop, axis=0)
    elif isinstance (boolean_fieldprop, campo.property.Property):
        map_flipped = np.flip (boolean_fieldprop.values()[0], axis=0) 
    else:
        raise TypeError ('boolean_fieldprop needs to be of type campo.property or of a numpy array with same dimensions as field property values')
    
    nragents = len (point_prop.values().values.values())
    for fidx, area in enumerate (field_pset.space_domain): 
        nr_cols = int(area[5])
        xmin = area [0]
        ymin = area [1] 
        resolution = math.fabs (area[2] - xmin)/nr_cols
    # finding the indices of the places where the fieldcondition is true 
    coords_idx = np.argwhere (map_flipped) #coordinates of the spawning grounds in [y,x]
    # collecting the coordinate combination in a tuple so as to prevent them from being 'disconnected' from eachother 
    coords_list = [tuple(row) for row in coords_idx] 
    random_newindex = random.sample (coords_list, nragents) # nr of agents is the subsetsize
    # seperating the tuples in the list in two seperate list
    yindex, xindex = zip(*random_newindex) #assuming that tuple list is reversed, first gives y then x as in column = x and row = y 
    xindex = np.array (xindex)
    yindex = np.array (yindex)
    xcoords = np.zeros(nragents)
    ycoords = np.zeros(nragents)

    # make from x index a x coordinate by using resolution and bounding box information
    for i, xvalue in enumerate(xindex):
        xcoords [i] = (xvalue*resolution + xmin) 
    for j, yvalue in enumerate(yindex): 
        ycoords[j] = (yvalue *resolution + ymin)
    return xcoords, ycoords 