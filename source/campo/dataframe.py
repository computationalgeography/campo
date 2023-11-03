"""
This module contains functions that select information from a LUE dataset
and return it in such a way that it becomes easy for postprocessing
using other Python packages.
"""
import os
import warnings

import numpy as np
import xarray as xr
import pandas as pd

warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

import lue.data_model as ldm


def _timeunit_pdname(unit):
    """ Return string representation of time unit """
    # We append an s to match Pandas keywords
    res = '{}s'.format(unit)
    if '.' in res:
        res = res.partition('.')[2]

    return res


def point_agent(object_ids, space_domain):
  obj_idx = int(np.where(object_ids == object_ids[0])[0])
  dom = space_domain.value[:][obj_idx]
  if len(dom) == 2:
    return True
  else:
    return False

def object_indices(object_ids, selection):
  res = []
  for item in selection:
    idx = int(np.where(object_ids == item)[0])
    res.append(idx)
  return res

def select_constant_same_shape_arrays(
        property_set,
        properties,
        object_ids,
        object_selection):
    # Each array is a same_shape.Property
    # Each array can be translated to a single array with an additional
    # dimension for object IDs
    result = {}

    property_set_name = property_set.id.name

    space_domain = None
    space_discretization = None

    if property_set.has_space_domain:
      space_domain = property_set.space_domain
    else:
      raise NotImplementedError


    for prop in properties:
        prop_name = prop.id.name
        xr_dataset = {}

        # All coordinates go into a dataarray, for selected object IDs
        dom = space_domain.value[:]

        sel_idx = object_indices(object_ids, object_selection)
        sel_oids = np.take(object_ids, sel_idx)

        coordinates = np.take(dom, sel_idx, axis=0)

        if point_agent(object_ids, space_domain):
          dim = 'x, y'
          result['_campo_space_type'] = 'static_same_point'
        else:
          dim = 'xlr, ylr, xul, yul'
          result['_campo_space_type'] = 'static_same_field'

        da = xr.DataArray(coordinates, coords={'id':sel_oids}, dims=['id', dim])

        xr_dataset['coordinates'] = da

        # All values go into a dataarray, for selected object IDs
        val = prop.value[:]
        val_sel = np.take(val, sel_idx, axis=0)

        if point_agent(object_ids, space_domain):
          dim = ['id']
        else:
          dim = ['id', 'x','y']

        da = xr.DataArray(val_sel, coords={'id':sel_oids}, dims=dim)

        xr_dataset['values'] = da


        result[prop_name] = xr_dataset

    return result


def select_constant_different_shape_arrays(
        property_set,
        properties,
        object_ids,
        object_selection):

    # Each array is a different_shape.Property
    # Each array can be translated to a dictionary of arrays per object ID
    result = {'_campo_space_type' : 'static_diff_field'}

    property_set_name = property_set.id.name

    space_domain = None
    space_discretization = None

    if property_set.has_space_domain:
      space_domain = property_set.space_domain
    else:
      raise NotImplementedError

    if properties[0].space_is_discretized:
        space_discretization = properties[0].space_discretization_property()
    else:
      raise NotImplementedError



    # here we hopefully have object ids, domain, discretisation and values
    # and assume it's 2d space fttb
    for prop in properties:
      # One xarray per property
      prop_name = prop.id.name

      xr_dataset = {}

      # Individual data arrays due to different shapes
      for oid in object_selection:
        obj_idx = int(np.where(object_ids == oid)[0])

        dom = space_domain.value[:][obj_idx]
        dis = space_discretization.value[:][obj_idx]
        val = prop.value[oid][:]

        nr_rows, nr_cols = dis

        xul = dom[0]
        yul = dom[1]
        xlr = dom[2]
        ylr = dom[3]

        if nr_rows > 0:
          y_cellsize = (yul - ylr) / nr_rows
        else:
          y_cellsize = 0

        if nr_cols > 0:
          x_cellsize = (xlr - xul) / nr_cols
        else:
          x_cellsize = 0

        x = []
        y = []
        for r in range(0,int(nr_cols)):
          x.append(xul + r * x_cellsize)

        for c in range(0,int (nr_rows)):
          y.append(yul - c * y_cellsize)

        da = xr.DataArray(val, coords=[y, x], dims=['ycoord', 'xcoord'])

        xr_dataset[oid] = da

      result[prop_name] = xr_dataset

    return result


def select_variable_same_shape_constant_shape_arrays(
        property_set,
        properties,
        all_object_ids,
        object_selection):

    # Each array is a same_shape.constant_shape.Property
    # Each array can be translated to ...
    result = {}


    property_set_name = property_set.id.name

    space_domain = None
    space_discretization = None
    time_domain = None
    time_discretization = None

    if property_set.has_space_domain:
      space_domain = property_set.space_domain
    else:
      raise NotImplementedError

    #if properties[0].space_is_discretized:
        #space_discretization = properties[0].space_discretization_property()
    #else:
      #raise NotImplementedError

    if property_set.has_time_domain:
      time_domain = property_set.time_domain
    else:
      raise NotImplementedError

    object_tracker = property_set.object_tracker

    object_ids = object_tracker.active_object_id[:]

    assert time_domain.value.nr_boxes == 1

    # Construct list of time steps...
    nr_timesteps = int(time_domain.value[0][1] + 1)

    clock = time_domain.clock
    epoch = clock.epoch
    origin = epoch.origin
    nr_units = clock.nr_units

    keys = { _timeunit_pdname(clock.unit) : nr_units }

    # List of time steps
    timesteps = pd.date_range(origin, periods=nr_timesteps, freq=pd.DateOffset(**keys) ).values

    for prop in properties:
        prop_name = prop.id.name
        xr_dataset = {}

        # All coordinates go into a dataarray, for selected object IDs
        dom = space_domain.value[:]

        sel_idx = object_indices(object_ids, object_selection)
        sel_oids = np.take(object_ids, sel_idx)

        coordinates = np.take(dom, sel_idx, axis=0)

        if point_agent(object_ids, space_domain):
          dim = 'x, y'
          result['_campo_space_type'] = 'dynamic_same_point'
        else:
          dim = 'xlr, ylr, xul, yul'
          result['_campo_space_type'] = 'dynamic_same_field'
        da = xr.DataArray(coordinates, coords={'id':sel_oids}, dims=['id', dim])

        xr_dataset['coordinates'] = da

        # All values go into a dataarray, for selected object IDs
        val = prop.value[:]
        val_sel = np.take(val, sel_idx, axis=0)

        if point_agent(object_ids, space_domain):
          dim = ['id', 'time']
        else:
          dim = ['id', 'time', 'x','y']

        da = xr.DataArray(val_sel, coords={'id':sel_oids}, dims=dim)

        xr_dataset['values'] = da


        result[prop_name] = xr_dataset

    return result


def select_variable_same_shape_variable_shape_arrays(
        property_set,
        arrays):

    # Each array is a same_shape.variable_shape.Property
    # Each array can be translated to ...
    result = []

    assert False, "TODO"

    return result


def select_variable_different_shape_constant_shape_arrays(
        property_set,
        properties,
        all_object_ids,
        object_selection):

    # Each array is a different_shape.constant_shape.Property
    # Each array can be translated to ...
    result = {}


    property_set_name = property_set.id.name

    space_domain = None
    space_discretization = None
    time_domain = None
    time_discretization = None

    if property_set.has_space_domain:
      space_domain = property_set.space_domain
    else:
      raise NotImplementedError

    if properties[0].space_is_discretized:
        space_discretization = properties[0].space_discretization_property()
    else:
      raise NotImplementedError

    if property_set.has_time_domain:
      time_domain = property_set.time_domain
    else:
      raise NotImplementedError

    object_tracker = property_set.object_tracker

    object_ids = object_tracker.active_object_id[:]

    assert time_domain.value.nr_boxes == 1

    # Construct list of time steps...
    nr_timesteps = int(time_domain.value[0][1])# + 1

    clock = time_domain.clock
    epoch = clock.epoch
    origin = epoch.origin
    nr_units = clock.nr_units

    keys = { _timeunit_pdname(clock.unit) : nr_units }

    # List of time steps
    timesteps = pd.date_range(origin, periods=nr_timesteps, freq=pd.DateOffset(**keys) ).values


    # here we hopefully have object ids, domain, discretisation and values
    # and assume it's 2d space fttb
    for prop in properties:
      # One xarray per property
      prop_name = prop.id.name

      xr_dataset = {}

      # Individual data arrays due to different shapes
      for oid in object_selection:
        obj_idx = int(np.where(object_ids == oid)[0])

        dom = space_domain.value[:][obj_idx]
        dis = space_discretization.value[:][obj_idx]

        val = prop.value[oid][:]

        nr_rows, nr_cols = dis
        assert nr_rows != 0
        assert nr_cols != 0

        xul = dom[0]
        yul = dom[1]
        xlr = dom[2]
        ylr = dom[3]

        if nr_rows > 0:
          y_cellsize = abs(yul - ylr) / nr_rows
        else:
          y_cellsize = 0

        if nr_cols > 0:
          x_cellsize = abs(xlr - xul) / nr_cols
        else:
          x_cellsize = 0

        x = []
        y = []
        for r in range(0,int(nr_cols)):
          x.append(xul + r * x_cellsize)

        for c in range(0,int (nr_rows)):
          y.append(yul + c * y_cellsize)

        da = xr.DataArray(val, coords=[timesteps, y, x], dims=['time', 'ycoord', 'xcoord'])

        xr_dataset[oid] = da

      result[prop_name] = xr_dataset

    return result


def select_variable_different_shape_variable_shape_arrays(
        property_set,
        arrays):

    # Each array is a different_shape.variable_shape.Property
    # Each array can be translated to ...
    result = []

    assert False, "TODO"

    return result


def select_variable_same_shape_arrays(
        property_set,
        arrays,
        all_object_ids,
        object_ids):

    #result = []

    if ldm.ShapeVariability.constant in arrays:
        return select_variable_same_shape_constant_shape_arrays(
            property_set, arrays[ldm.ShapeVariability.constant], all_object_ids, object_ids)

    if ldm.ShapeVariability.variable in arrays:
        raise NotImplementedError
        result += select_variable_same_shape_variable_shape_arrays(
            property_set, arrays[ldm.ShapeVariability.variable])

    #return result


def select_variable_different_shape_arrays(
        property_set,
        arrays,
        all_object_ids,
        object_ids):

    # result = []

    if ldm.ShapeVariability.constant in arrays:
        return select_variable_different_shape_constant_shape_arrays(
            property_set, arrays[ldm.ShapeVariability.constant], all_object_ids, object_ids)

    if ldm.ShapeVariability.variable in arrays:
        raise NotImplementedError
        result += select_variable_different_shape_variable_shape_arrays(
            property_set, arrays[ldm.ShapeVariability.variable])

    #return result


def select_constant_arrays(
        property_set,
        arrays,
        all_object_ids,
        object_ids):

    if ldm.ShapePerObject.same in arrays:
        return select_constant_same_shape_arrays(property_set, arrays[ldm.ShapePerObject.same], all_object_ids, object_ids)

    if ldm.ShapePerObject.different in arrays:
        return select_constant_different_shape_arrays(property_set, arrays[ldm.ShapePerObject.different], all_object_ids, object_ids)



def select_variable_arrays(
        property_set,
        arrays,
        all_object_ids,
        object_ids):


    if ldm.ShapePerObject.same in arrays:
        return select_variable_same_shape_arrays(property_set, arrays[ldm.ShapePerObject.same], all_object_ids, object_ids)

    if ldm.ShapePerObject.different in arrays:
        return select_variable_different_shape_arrays(property_set, arrays[ldm.ShapePerObject.different], all_object_ids, object_ids)



def select_arrays(
        arrays,
        all_object_ids,
        object_ids):

    result = {}

    for property_set, arrays_ in arrays.items():
        pset_name = property_set.id.name
        if ldm.ValueVariability.constant in arrays_:
            result[pset_name] = select_constant_arrays(property_set, arrays_[ldm.ValueVariability.constant], all_object_ids, object_ids)

        if ldm.ValueVariability.variable in arrays_:
            result[pset_name] = select_variable_arrays(property_set, arrays_[ldm.ValueVariability.variable], all_object_ids, object_ids)

    return result


def select(
        phenomenon,
        #object_ids=[],
        # TODO time=(),
        property_names=[]):

    property_set_names = phenomenon.property_sets.names

    if len(property_names) == 0:
        raise NotImplementedError('Provide list of properties')
    #    for property_set_name in property_set_names:
    #        property_set = phenomenon.property_sets[property_set_name]
    #        property_names += property_set.properties.names

    properties_by_property_set = {}

    for property_name in property_names:
        for property_set_name in property_set_names:
            property_set = phenomenon.property_sets[property_set_name]
            property_names_ = property_set.properties.names

            if property_name in property_names_:
                properties_by_property_set.setdefault(property_set, []).append(
                    property_set.properties[property_name])
                #break

    if not properties_by_property_set:
      msg = 'Could not find one of the properties named {}'.format(property_names)
      raise ValueError(msg)


    # Group properties by value_variability, shape_per_object, shape_variability
    arrays = {}

    for property_set, properties in properties_by_property_set.items():
        for property in properties:

            shape_per_object = property_set.properties.shape_per_object(property.id.name)
            value_variability = property_set.properties.value_variability(property.id.name)

            if value_variability == ldm.ValueVariability.constant:
                arrays.setdefault(property_set, {}).setdefault(
                    value_variability, {}).setdefault(
                        shape_per_object, []).append(property)
            else:
                shape_variability = property_set.properties.shape_variability(property.id.name)

                arrays.setdefault(property_set, {}).setdefault(
                    value_variability, {}).setdefault(
                        shape_per_object, {}).setdefault(
                            shape_variability, []).append(property)

    # Select information, given the kind of array the information is stored in

    # How to ensure that there is only one active period?
    all_object_ids = phenomenon.object_id[:]

    phen_name = phenomenon.id.name

    result = {}
    result[phen_name] = select_arrays(arrays, all_object_ids, all_object_ids)

    return result




def coordinates(dataset, phenomenon, propertyset, timestep):

    lue_pset = dataset.phenomena[phenomenon].property_sets[propertyset]
    object_ids = dataset.phenomena[phenomenon].object_id[:]


    time_start_idx = len(object_ids) * (timestep - 1)
    time_end_idx = time_start_idx + len(object_ids)

    vals = lue_pset.space_domain.value[time_start_idx:time_end_idx]
    return vals