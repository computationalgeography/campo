import unittest
import os
import sys

import numpy as np

import lue
import lue.data_model as ldm

import campo.dataframe as df



class TestDynSame(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    nr_objects = 3
    rank = 2
    time_boxes = 1
    timesteps = 4

    dataset = ldm.create_dataset("test_dyn_same.lue")
    phen = dataset.add_phenomenon("catchment")

    id = [2, 5, 4]
    phen.object_id.expand(nr_objects)[:] = id

    # Time
    time_configuration = ldm.TimeConfiguration(
        ldm.TimeDomainItemType.box
    )
    epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, "2000-02-03", ldm.Calendar.gregorian)
    clock = ldm.Clock(epoch, ldm.Unit.year, 2)

    # Space
    point_space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.point #box
    )

    point_rank = 1
    point_pset = phen.add_property_set(
        "dynamic_point",
        time_configuration, clock,
        point_space_configuration,
        space_coordinate_dtype=np.dtype(np.float32), rank=point_rank)

    box = np.arange(nr_objects * 2, dtype=np.float32).reshape(
        nr_objects, 2)

    print(box)
    #print(point_pset.space_domain.value[:])

    point_pset.space_domain.value.expand(nr_objects)[:] = box

    point_pset.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = id

    point_pset.object_tracker.active_object_index.expand(time_boxes * nr_objects)[:] = [0, 0, 0]

    point_pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0

    time_domain = point_pset.time_domain
    time_domain.value.expand(time_boxes)[:] = [0, 3]

    property1 = point_pset.add_property("property1", dtype=np.dtype(np.float32), shape=(timesteps,),
        value_variability=ldm.ValueVariability.variable)
    np.random.seed(2)
    v1 = np.random.rand(timesteps * nr_objects).astype(np.float32).reshape(nr_objects, timesteps)
    property1.value.expand(nr_objects)[:] = v1


    property2 = point_pset.add_property("property2", dtype=np.dtype(np.int32), shape=(timesteps,),
        value_variability=ldm.ValueVariability.variable)
    np.random.seed(2)
    v2 = (20 * np.random.rand(timesteps * nr_objects)).astype(np.int32).reshape(nr_objects, timesteps)
    property2.value.expand(nr_objects)[:] = v2


    area_space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.box
    )

    space_rank = 2
    area_pset = phen.add_property_set(
        "dynamic_area",
        time_configuration, clock,
        area_space_configuration,
        space_coordinate_dtype=np.dtype(np.float32), rank=space_rank)

    box = np.arange(nr_objects * space_rank * 2, dtype=np.float32).reshape(
        nr_objects, space_rank * 2)
    area_pset.space_domain.value.expand(nr_objects)[:] = box

    area_pset.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = id

    area_pset.object_tracker.active_object_index.expand(time_boxes * nr_objects)[:] = [0, 0, 0]

    area_pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0

    time_domain = area_pset.time_domain
    time_domain.value.expand(time_boxes)[:] = [0, 3]

    shape = (timesteps, 2, 4)
    count_datatype = ldm.dtype.Count

    ## Property with same shaped 2D object arrays
    property1_datatype = np.dtype(np.float32)
    property1 = area_pset.add_property(
        "property1", dtype=property1_datatype, shape=shape,
        value_variability=ldm.ValueVariability.variable)
    values = np.random.rand(timesteps * nr_objects * shape[0] * shape[1]).astype(property1_datatype).reshape(nr_objects, timesteps, shape[1], shape[2])
    property1.value.expand(nr_objects)[:] = values

    property2_datatype = np.dtype(np.int32)
    property2 = area_pset.add_property(
        "property2", dtype=property2_datatype, shape=shape,
        value_variability=ldm.ValueVariability.variable)
    values2 = (20 * np.random.rand(timesteps * nr_objects * shape[0] * shape[1])).astype(property2_datatype).reshape(nr_objects, timesteps, shape[1], shape[2])
    property2.value.expand(nr_objects)[:] = values2

    # Discretization property
    space_globals = phen.add_collection_property_set("globals")

    discretization = space_globals.add_property(
        "discretization", dtype=count_datatype, shape=(space_rank,))

    discretization.value.expand(1)[:] = np.array([shape[0],shape[1]],
            dtype=count_datatype).reshape(1, space_rank)

    property1.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)

    property2.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)


    ldm.assert_is_valid(dataset)



  @classmethod
  def tearDownClass(self):
    #os.remove("test_dyn_diff.lue")
    pass


  def  test_1(self):
    """ test property values """

    dataset = ldm.open_dataset("test_dyn_same.lue")

    frame = df.select(dataset.catchment, property_names=['property1', 'property2'])


    p = frame['catchment']['dynamic_point']['property1']

    arr = np.array([[0.4359949 , 0.02592623, 0.5496625 , 0.4353224 ],
       [0.4203678 , 0.3303348 , 0.20464863, 0.619271  ],
       [0.29965466, 0.2668273 , 0.6211338 , 0.5291421 ]], dtype=np.float32)

    obj_values = p['values']
    self.assertEqual(True, np.allclose(arr, obj_values.values))


    p = frame['catchment']['dynamic_point']['property2']
    obj_values = p['values']
    arr = np.array([[ 8,  0, 10,  8],
       [ 8,  6,  4, 12],
       [ 5,  5, 12, 10]], dtype=np.int32)

    self.assertEqual(True, np.allclose(arr, obj_values.values))


    p = frame['catchment']['dynamic_area']['property2']
    obj_values = p['values']
    arr = np.array([[[[11,  6,  5, 18],
         [ 8, 10, 12, 16]],

        [[12,  3, 11,  9],
         [10, 13,  4,  3]],

        [[ 2,  5,  0, 12],
         [ 5,  3,  1,  5]],

        [[ 4,  5,  9, 10],
         [16, 19,  0,  4]]],


       [[[12,  3, 17,  4],
         [14, 13, 15,  0]],

        [[ 4, 14,  1,  0],
         [ 7, 11,  1,  1]],

        [[ 0,  7, 13,  3],
         [17,  8, 12,  5]],

        [[12, 19,  8,  4],
         [ 8,  8, 10, 10]]],


       [[[ 0,  3,  9, 14],
         [15, 15, 10, 19]],

        [[ 6,  9, 14, 17],
         [ 8, 16,  8, 14]],

        [[ 0,  0, 18,  2],
         [13,  5,  4,  7]],

        [[18, 11, 18, 14],
         [10, 10,  4,  0]]]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, obj_values.values))


  #def  test_2(self):
    #""" test coordinates values """
    #self.assertEqual(True, False)


  #def  test_3(self):
    #""" test access by objecd id """
    #self.assertEqual(True, False)

  #def  test_4(self):
    #""" test access by time step """
    #self.assertEqual(True, False)
