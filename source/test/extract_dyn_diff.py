import math
import os
import sys
import unittest

import numpy as np

import lue
import lue.data_model as ldm

import campo.dataframe as df





class TestDynDiff(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    nr_areas = 3
    rank = 2
    time_boxes = 1
    timesteps = 3

    dataset = ldm.create_dataset("test_dyn_diff.lue")
    area = dataset.add_phenomenon("phenomenon")

    id = [2, 5, 4]
    area.object_id.expand(nr_areas)[:] = id

    # Time
    time_configuration = ldm.TimeConfiguration(
        ldm.TimeDomainItemType.box
    )
    epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, "2000-02-03", ldm.Calendar.gregorian)
    clock = ldm.Clock(epoch, ldm.Unit.year, 2)



    # Space
    space_configuration = ldm.SpaceConfiguration(
        ldm.Mobility.stationary,
        ldm.SpaceDomainItemType.box
    )

    prop_set = area.add_property_set(
        "prop_set",
        time_configuration, clock,
        space_configuration, space_coordinate_dtype=np.dtype(np.float32), rank=rank)


    prop_set.object_tracker.active_object_id.expand(time_boxes * nr_areas)[:] = id

    prop_set.object_tracker.active_object_index.expand(time_boxes * nr_areas)[:] = [0, 0, 0]

    prop_set.object_tracker.active_set_index.expand(time_boxes)[:] = 0

    time_domain = prop_set.time_domain
    time_domain.value.expand(time_boxes)[:] = [0, 2]


    box = np.arange(nr_areas * rank * 2, dtype=np.float32).reshape(
        nr_areas, rank * 2) + 1
    box = np.array([[1,2,3,4],[5,6,11,12],[13,14,20,21]], dtype=np.float32)

    prop_set.space_domain.value.expand(nr_areas)[:] = box

    # Property with differently shaped 2D object arrays
    property1_datatype = np.dtype(np.float32)
    property1 = prop_set.add_property(
        "property1", dtype=property1_datatype, rank=rank,
                shape_per_object=ldm.ShapePerObject.different,
                shape_variability=ldm.ShapeVariability.constant)
    count_datatype = ldm.dtype.Count
    shape = 2 + np.arange(  # Dummy data
        nr_areas * rank, dtype=count_datatype).reshape(nr_areas, rank)

    property2_datatype = np.dtype(np.int32)
    property2 = prop_set.add_property(
        "property2", dtype=property2_datatype, rank=rank,
                shape_per_object=ldm.ShapePerObject.different,
                shape_variability=ldm.ShapeVariability.constant)


    for idx, obj in enumerate(id):
      property1.value.expand(obj, tuple(shape[idx]), timesteps)
      property2.value.expand(obj, tuple(shape[idx]), timesteps)

    # Dummy values
    for idx, obj_id in enumerate(id):
      for t in range(timesteps):
        np.random.seed(t + 2)
        v1 = (10 * np.random.rand(*shape[idx])).astype(property1_datatype)
        np.random.seed(t + 2)
        v2 = (20 * np.random.rand(*shape[idx])).astype(property2_datatype)
        property1.value[obj_id][t] = v1
        property2.value[obj_id][t] = v2

    # Discretization property with 1D object arrays containing the shape of
    # each object's elevation array: nr_rows and nr_cols
    discretization = prop_set.add_property(
        "discretization", dtype=count_datatype, shape=(rank,))
    discretization.value.expand(nr_areas)[:] = shape

    property1.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)

    property2.set_space_discretization(
        ldm.SpaceDiscretization.regular_grid, discretization)


    ldm.assert_is_valid(dataset)



  @classmethod
  def tearDownClass(self):
    os.remove("test_dyn_diff.lue")


  def  test_1(self):
    """ test property values """

    dataset = ldm.open_dataset("test_dyn_diff.lue")

    frame = df.select(dataset.phenomenon, property_names=['property1', 'property2'])


    p = frame['phenomenon']['prop_set']['property1']

    arr = np.array([[[4.359949  , 0.25926232, 5.496625  ],
        [4.353224  , 4.203678  , 3.3033483 ]],

       [[5.507979  , 7.081478  , 2.9090474 ],
        [5.108276  , 8.929469  , 8.962931  ]],

       [[9.670299  , 5.4723225 , 9.726844  ],
        [7.14816   , 6.9772882 , 2.1608949 ]]], dtype=np.float32)

    v = p[2]

    self.assertEqual(True, np.allclose(arr, v.values))


    v = p[5]
    arr = np.array([[[4.359949  , 0.25926232, 5.496625  , 4.353224  , 4.203678  ],
        [3.3033483 , 2.0464864 , 6.1927094 , 2.9965467 , 2.6682727 ],
        [6.2113385 , 5.291421  , 1.3457994 , 5.1357813 , 1.8443986 ],
        [7.8533516 , 8.539753  , 4.9423685 , 8.465615  , 0.7964548 ]],

       [[5.507979  , 7.081478  , 2.9090474 , 5.108276  , 8.929469  ],
        [8.962931  , 1.255853  , 2.0724287 , 0.51467204, 4.408098  ],
        [0.2987621 , 4.568332  , 6.4914403 , 2.7848728 , 6.762549  ],
        [5.908628  , 0.23981883, 5.588541  , 2.5925245 , 4.151012  ]],

       [[9.670299  , 5.4723225 , 9.726844  , 7.14816   , 6.9772882 ],
        [2.1608949 , 9.762745  , 0.06230255, 2.5298235 , 4.347915  ],
        [7.7938294 , 1.9768507 , 8.629932  , 9.834006  , 1.6384224 ],
        [5.9733396 , 0.08986098, 3.865713  , 0.4416006 , 9.566529  ]]],
      dtype=np.float32)

    self.assertEqual(True, np.allclose(arr, v.values))


    v = p[4]
    #self.assertEqual(True, np.allclose(arr, v.values))


    p = frame['phenomenon']['prop_set']['property2']

    v = p[2]
    arr = np.array([[[ 8,  0, 10],
        [ 8,  8,  6]],

       [[11, 14,  5],
        [10, 17, 17]],

       [[19, 10, 19],
        [14, 13,  4]]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, v.values))

    v = p[5]
    arr = np.array([[[ 8,  0, 10,  8,  8],
        [ 6,  4, 12,  5,  5],
        [12, 10,  2, 10,  3],
        [15, 17,  9, 16,  1]],

       [[11, 14,  5, 10, 17],
        [17,  2,  4,  1,  8],
        [ 0,  9, 12,  5, 13],
        [11,  0, 11,  5,  8]],

       [[19, 10, 19, 14, 13],
        [ 4, 19,  0,  5,  8],
        [15,  3, 17, 19,  3],
        [11,  0,  7,  0, 19]]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, v.values))

    v = p[4]
    arr = np.array([[[ 8,  0, 10,  8,  8,  6,  4],
        [12,  5,  5, 12, 10,  2, 10],
        [ 3, 15, 17,  9, 16,  1, 10],
        [ 1,  8,  1,  2, 11,  4,  2],
        [ 4,  6,  9,  4, 12,  9, 10],
        [ 7, 15, 11,  3, 14, 19, 10]],

       [[11, 14,  5, 10, 17, 17,  2],
        [ 4,  1,  8,  0,  9, 12,  5],
        [13, 11,  0, 11,  5,  8,  5],
        [13,  8,  3, 10, 15,  6,  4],
        [ 7, 18, 19, 13, 18, 16,  7],
        [ 1, 13, 11,  7,  4,  8,  9]],

       [[19, 10, 19, 14, 13,  4, 19],
        [ 0,  5,  8, 15,  3, 17, 19],
        [ 3, 11,  0,  7,  0, 19,  8],
        [18, 15, 17,  3,  1, 12,  3],
        [14,  8, 10, 18, 10,  2,  3],
        [10, 10, 12,  8, 12,  7, 12]]], dtype=np.int32)

    self.assertEqual(True, np.array_equal(arr, v.values))


  def test_2(self):
    """ test coordinates values """

    dataset = ldm.open_dataset("test_dyn_diff.lue")

    frame = df.select(dataset.phenomenon, property_names=['property1', 'property2'])

    p = frame['phenomenon']['prop_set']['property1']

    obj = p[2]
    rows = obj.values.shape[1]
    cols = obj.values.shape[2]

    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(1, obj.xcoord[0].values)
    self.assertAlmostEqual(3, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(2, obj.ycoord[0].values)
    self.assertAlmostEqual(4, obj.ycoord[0].values + rows * ycellsize)

    obj = p[5]
    rows = obj.values.shape[1]
    cols = obj.values.shape[2]
    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(5, obj.xcoord[0].values)
    self.assertAlmostEqual(11, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(6, obj.ycoord[0].values)
    self.assertAlmostEqual(12, obj.ycoord[0].values + rows * ycellsize)

    obj = p[4]
    rows = obj.values.shape[1]
    cols = obj.values.shape[2]
    xcellsize = math.fabs(obj.xcoord[1].values - obj.xcoord[0].values)
    ycellsize = math.fabs(obj.ycoord[1].values - obj.ycoord[0].values)

    self.assertAlmostEqual(13, obj.xcoord[0].values)
    self.assertAlmostEqual(20, obj.xcoord[0].values + cols * xcellsize)

    self.assertAlmostEqual(14, obj.ycoord[0].values)
    self.assertAlmostEqual(21, obj.ycoord[0].values + rows * ycellsize)


  def  test_4(self):
    """ test access by time step """


    dataset = ldm.open_dataset("test_dyn_diff.lue")

    frame = df.select(dataset.phenomenon, property_names=['property1', 'property2'])

    p = frame['phenomenon']['prop_set']['property1']


    # Oid 2, 2nd timestep
    obj = p[2]
    res = obj.loc['2002-02-03', :]

    arr = np.array([[[5.507979  , 7.081478  , 2.9090474 ],
        [5.108276  , 8.929469  , 8.962931  ]]], dtype=np.float32)

    self.assertEqual(True, np.allclose(arr, res.values))
