import unittest
import os
import sys

import numpy as np

import lue
import lue.data_model as ldm

import campo.dataframe as df





class TestConstSame(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    nr_objects = 3

    dataset = ldm.create_dataset("test_const_same.lue")
    phen = dataset.add_phenomenon("catchment")

    id = [2, 5, 4]
    phen.object_id.expand(nr_objects)[:] = id


    point_space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.point
    )


    point_rank = 2
    point_pset = phen.add_property_set(
        "static_point", point_space_configuration,
        space_coordinate_dtype=np.dtype(np.float32), rank=point_rank)

    box = np.arange(nr_objects * point_rank, dtype=np.float32).reshape(
        nr_objects, point_rank)

    point_pset.space_domain.value.expand(nr_objects)[:] = box

    property1 = point_pset.add_property("property1", dtype=np.dtype(np.float32))
    np.random.seed(2)
    v1 = np.random.rand(nr_objects).astype(np.float32)
    property1.value.expand(nr_objects)[:] = v1

    property2 = point_pset.add_property("property2", dtype=np.dtype(np.int32))
    np.random.seed(2)
    v2 = (20 * np.random.rand(nr_objects)).astype(np.int32)
    property2.value.expand(nr_objects)[:] = v2

    area_space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.box
    )
    space_rank = 2
    area_pset = phen.add_property_set(
        "static_area", area_space_configuration,
        space_coordinate_dtype=np.dtype(np.float32), rank=space_rank)

    box = np.arange(nr_objects * space_rank * 2, dtype=np.float32).reshape(
        nr_objects, space_rank * 2)
    area_pset.space_domain.value.expand(nr_objects)[:] = box

    shape = (2, 4)
    count_datatype = ldm.dtype.Count

    ## Property with same shaped 2D object arrays
    property1_datatype = np.dtype(np.float32)
    property1 = area_pset.add_property(
        "property1", dtype=property1_datatype, shape=shape)
    np.random.seed(2)
    values = np.random.rand(nr_objects * shape[0] * shape[1]).astype(property1_datatype).reshape(nr_objects, shape[0], shape[1])
    property1.value.expand(nr_objects)[:] = values

    property2_datatype = np.dtype(np.int32)
    property2 = area_pset.add_property(
        "property2", dtype=property2_datatype, shape=shape)
    np.random.seed(2)
    values2 = (20 * np.random.rand(nr_objects * shape[0] * shape[1])).astype(property2_datatype).reshape(nr_objects, shape[0], shape[1])

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

    ldm.assert_is_valid(dataset, fail_on_warning=False)



  @classmethod
  def tearDownClass(self):
    #os.remove("test_const_same.lue")
    pass


  def  test_1(self):
    """ test property values """

    dataset = ldm.open_dataset("test_const_same.lue")

    frame = df.select(dataset.catchment, property_names=['property1', 'property2'])

    pp = frame['catchment']['static_point']['property1']

    obj_values = pp['values']
    arr = np.array([0.4359949 , 0.02592623, 0.5496625 ], dtype=np.float32)
    self.assertEqual(True, np.allclose(arr, obj_values.values))


    pp = frame['catchment']['static_point']['property2']
    obj_values = pp['values']
    arr = np.array([8, 0, 10], dtype=np.int32)
    self.assertEqual(True, np.array_equal(arr, obj_values.values))

    fp = frame['catchment']['static_area']['property1']

    obj_values = fp['values']
    arr = np.array([[[0.4359949 , 0.02592623, 0.5496625 , 0.4353224 ],
        [0.4203678 , 0.3303348 , 0.20464863, 0.619271  ]],

       [[0.29965466, 0.2668273 , 0.6211338 , 0.5291421 ],
        [0.13457994, 0.5135781 , 0.18443987, 0.7853351 ]],

       [[0.8539753 , 0.49423683, 0.8465615 , 0.07964548],
        [0.5052461 , 0.0652865 , 0.42812234, 0.09653091]]], dtype=np.float32)
    self.assertEqual(True, np.allclose(arr, obj_values.values))

    fp = frame['catchment']['static_area']['property2']
    obj_values = fp['values']
    arr = np.array([[[ 8,  0, 10,  8],
        [ 8,  6,  4, 12]],

       [[ 5,  5, 12, 10],
        [ 2, 10,  3, 15]],

       [[17,  9, 16,  1],
        [10,  1,  8,  1]]], dtype=np.int32)
    self.assertEqual(True, np.array_equal(arr, obj_values.values))




  def  test_2(self):
    """ test coordinates values """
    dataset = ldm.open_dataset("test_const_same.lue")

    frame = df.select(dataset.catchment, property_names=['property1', 'property2'])

    pp = frame['catchment']['static_point']['property1']

    coords = pp['coordinates']
    arr = np.arange(6, dtype=np.float32).reshape(3, 2)
    self.assertEqual(True, np.allclose(arr, coords.values))

    fp = frame['catchment']['static_area']['property2']

    coords = fp['coordinates']
    arr = np.arange(12, dtype=np.float32).reshape(3, 4)
    self.assertEqual(True, np.array_equal(arr, coords.values))


  #def  test_3(self):
    #""" test access by objecd id """
    #self.assertEqual(True, False)
