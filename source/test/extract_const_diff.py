import math
import os
import sys
import unittest

import numpy as np

import lue
import lue.data_model as ldm

import campo.dataframe as df


np.random.seed(2)


class TestConstDiff(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    nr_areas = 3
    rank = 2

    dataset = ldm.create_dataset("catchments.lue")
    area = dataset.add_phenomenon("catchment")

    id = [2, 5, 4]
    area.object_id.expand(nr_areas)[:] = id

    space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.box
    )
    constant = area.add_property_set(
        "static", space_configuration,
        space_coordinate_dtype=np.dtype(np.float32), rank=rank)

    box = np.arange(nr_areas * rank * 2, dtype=np.float32).reshape(
        nr_areas, rank * 2) + 1
    box = np.array([[1,2,3,4],[5,6,11,12],[13,14,20,21]], dtype=np.float32)

    constant.space_domain.value.expand(nr_areas)[:] = box

    # Property with differently shaped 2D object arrays
    property1_datatype = np.dtype(np.float32)
    property1 = constant.add_property(
        "property1", dtype=property1_datatype, rank=rank)
    count_datatype = ldm.dtype.Count
    shape = 2 + np.arange(  # Dummy data
        nr_areas * rank, dtype=count_datatype).reshape(nr_areas, rank)
    value = property1.value.expand(id, shape)


    property2_datatype = np.dtype(np.int32)
    property2 = constant.add_property(
        "property2", dtype=property2_datatype, rank=rank)
    count_datatype = ldm.dtype.Count
    value2 = property2.value.expand(id, shape)


    for a in range(nr_areas):
        v = (  # Dummy data
            10 * np.random.rand(*shape[a])).astype(property1_datatype)
        value[id[a]][:] = v
        value2[id[a]][:] = (  # Dummy data
            20 * np.random.rand(*shape[a])).astype(property2_datatype)

    # Discretization property with 1D object arrays containing the shape of
    # each object's elevation array: nr_rows and nr_cols
    discretization = constant.add_property(
        "discretization", dtype=count_datatype, shape=(rank,))
    discretization.value.expand(nr_areas)[:] = shape

    property1.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)

    property2.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)


    ldm.assert_is_valid(dataset)



  @classmethod
  def tearDownClass(self):
    os.remove("catchments.lue")


  def test_1(self):
    """ test array values """

    dataset = ldm.open_dataset("catchments.lue")

    frame = df.select(dataset.catchment, property_names=['property1', 'property2'])


    p = frame['catchment']['static']['property1']

    arr = np.array([[4.359949  , 0.25926232, 5.496625  ],
       [4.353224  , 4.203678  , 3.3033483 ]], dtype=np.float32)

    obj = p[2]

    self.assertEqual(True, np.allclose(arr, obj.values))


    obj = p[5]
    arr = np.array([[1.3457994 , 5.1357813 , 1.8443986 , 7.8533516 , 8.539753  ],
       [4.9423685 , 8.465615  , 0.7964548 , 5.0524607 , 0.65286505],
       [4.2812233 , 0.96530914, 1.2715998 , 5.967453  , 2.26012   ],
       [1.0694568 , 2.203062  , 3.498263  , 4.677875  , 2.0174322 ]],
      dtype=np.float32)

    self.assertEqual(True, np.allclose(arr, obj.values))


    obj = p[4]
    arr = np.array([[3.663424  , 8.508505  , 4.0627503 , 0.27202365, 2.4717724 ,
        0.6714437 , 9.93852   ],
       [9.705803  , 8.0025835 , 6.0181713 , 7.6495986 , 1.6922544 ,
        2.9302323 , 5.240669  ],
       [3.5662427 , 0.45678964, 9.831534  , 4.4135494 , 5.0400043 ,
        3.235413  , 2.5974476 ],
       [3.8688989 , 8.320169  , 7.3674707 , 3.7921057 , 0.13017337,
        7.9740496 , 2.693888  ],
       [5.826849  , 0.2555094 , 6.6220202 , 3.8752344 , 4.970738  ,
        4.1490583 , 3.508719  ],
       [5.509779  , 9.729107  , 1.1277622 , 3.1325853 , 0.4179771 ,
        7.3839974 , 6.575124  ]], dtype=np.float32)

    self.assertEqual(True, np.allclose(arr, obj.values))


    p = frame['catchment']['static']['property2']

    obj = p[2]
    arr = np.array([[ 4, 12,  5],
       [ 5, 12, 10]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, obj.values))

    obj = p[5]
    arr = np.array([[12,  9, 10,  7, 15],
       [11,  3, 14, 19, 10],
       [17,  6, 11,  8,  8],
       [15, 10, 19, 10,  1]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, obj.values))

    obj = p[4]
    arr = np.array([[ 4,  8, 12, 13,  3, 17, 15],
       [ 2, 17, 14, 15, 10,  4, 18],
       [11,  6,  5, 18,  8, 10, 12],
       [16, 12,  3, 11,  9, 10, 13],
       [ 4,  3,  2,  5,  0, 12,  5],
       [ 3,  1,  5,  4,  5,  9, 10]], dtype=np.int32)
    self.assertEqual(True, np.array_equal(arr, obj.values))


  def test_2(self):
    """ test coordinates values """

    dataset = ldm.open_dataset("catchments.lue")

    frame = df.select(dataset.catchment, property_names=['property1', 'property2'])

    p = frame['catchment']['static']['property1']

    obj = p[2]
    rows = obj.values.shape[0]
    cols = obj.values.shape[1]
    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(1, obj.xcoord[0].values)
    self.assertAlmostEqual(3, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(2, obj.ycoord[0].values)
    self.assertAlmostEqual(4, obj.ycoord[0].values + rows * ycellsize)


    obj = p[5]
    rows = obj.values.shape[0]
    cols = obj.values.shape[1]
    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(5, obj.xcoord[0].values)
    self.assertAlmostEqual(11, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(6, obj.ycoord[0].values)
    self.assertAlmostEqual(12, obj.ycoord[0].values + rows * ycellsize)


    obj = p[4]
    rows = obj.values.shape[0]
    cols = obj.values.shape[1]
    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(13, obj.xcoord[0].values)
    self.assertAlmostEqual(20, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(14, obj.ycoord[0].values)
    self.assertAlmostEqual(21, obj.ycoord[0].values + rows * ycellsize)

