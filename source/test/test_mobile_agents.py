import datetime
import unittest
import os
import sys

import numpy as np

import campo

import lue.data_model as ldm



class TestMobileAgents(unittest.TestCase):

  @classmethod
  def tearDownClass(self):
    pass

  @classmethod
  def setUpClass(self):

    with open('locations.csv', 'w') as content:
      content.write('1,2\n3,4\n5,6')

    self.ds = campo.Campo()

    self.a = self.ds.add_phenomenon('a')
    self.a.add_property_set('stationary_points', 'locations.csv')
    self.a.add_property_set('mobile_points', 'locations.csv')


  def test_1(self):
      """ Mobility of point agents """

      self.assertFalse(self.a.stationary_points.is_mobile)
      self.assertFalse(self.a.mobile_points.is_mobile)

      self.a.mobile_points.is_mobile = True

      self.assertTrue(self.a.mobile_points.is_mobile)


      # initial section
      self.a.stationary_points.sp = 500
      self.a.mobile_points.mp = 500

      # dummy time
      date = datetime.date(2000, 1, 1)
      time = datetime.time(0, 0)
      start = datetime.datetime.combine(date, time)
      unit = campo.TimeUnit.month
      stepsize = 1
      timesteps = 5

      # create the output lue data set
      self.ds.create_dataset("TestMobileAgents_test_1.lue")
      self.ds.set_time(start, unit, stepsize, timesteps)

      self.a.stationary_points.sp.is_dynamic = True
      self.a.mobile_points.mp.is_dynamic = True

      curr_sp = self.a.stationary_points.get_space_domain()
      curr_mp = self.a.mobile_points.get_space_domain()

      x_coords = np.array([1,3,5])
      y_coords = np.array([2,4,6])
      arr = np.empty((3, 2))
      arr[:,0] = x_coords
      arr[:,1] = y_coords

      self.assertTrue((x_coords == curr_sp.xcoord).all())
      self.assertTrue((y_coords == curr_sp.ycoord).all())

      self.assertTrue((x_coords == curr_mp.xcoord).all())
      self.assertTrue((y_coords == curr_mp.ycoord).all())

      curr_sp.xcoord = x_coords + 1
      curr_sp.ycoord = y_coords + 1

      curr_mp.xcoord = x_coords + 1
      curr_mp.ycoord = y_coords + 1

      self.a.stationary_points.set_space_domain(curr_sp)
      self.a.mobile_points.set_space_domain(curr_mp)

      # write after modifying coordinates
      self.ds.write()

      # dynamic section
      for timestep in range(1, timesteps + 1):
          # just modify values
          self.a.stationary_points.sp += 100
          self.a.mobile_points.mp += 100

#          curr_sp = self.a.stationary_points.get_space_domain(timestep)
          curr_mp = self.a.mobile_points.get_space_domain(timestep)
          # set coordinates of current timestep
          curr_mp.xcoord = x_coords + timestep
          curr_mp.ycoord = list(y_coords + timestep)

          self.a.mobile_points.set_space_domain(curr_mp, timestep)

          self.ds.write(timestep)

          self.assertTrue(((x_coords + timestep) == curr_mp.xcoord).all())
          self.assertTrue(((y_coords + timestep) == curr_mp.ycoord).all())


      # ldm.assert_is_valid("TestMobileAgents_test_1.lue")

      dataset = ldm.open_dataset("TestMobileAgents_test_1.lue", "r")
      lue_pset = dataset.phenomena["a"].property_sets["mobile_points"]
      object_ids = dataset.phenomena["a"].object_id[:]

      for timestep in range(1, timesteps + 1):
          coord_start_idx = len(object_ids) * (timestep - 1)
          coord_end_idx = coord_start_idx + len(object_ids)
          vals = lue_pset.space_domain.value[coord_start_idx:coord_end_idx]
          self.assertTrue(((arr + timestep) == vals).all())
