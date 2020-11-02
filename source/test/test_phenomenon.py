import unittest
import os
import sys

import campo



class TestPhenomenon(unittest.TestCase):

  @classmethod
  def tearDownClass(self):
    pass

  @classmethod
  def setUpClass(self):

    with open('locations.csv', 'w') as content:
      content.write('1,2\n3,4')

    self.ds = campo.Campo()

    self.a = self.ds.add_phenomenon('a')



  def test_1(self):
      """ accessing non-existing property set """

      with self.assertRaises(Exception) as context_manager:
          self.a.notfound

      self.assertRegex(str(context_manager.exception),
          "No property set 'notfound' in phenomenon 'a'")


  def test_2(self):
    """ empty phenomenon properties """
    self.assertEqual(self.a.name, 'a')
    self.assertEqual(self.a.nr_propertysets, 0)
    self.assertEqual(self.a.nr_agents, 0)


  def test_3(self):
    """ adding property set """
    self.a.add_property_set('b', 'locations.csv')
    self.assertEqual(self.a.nr_propertysets, 1)

    self.assertEqual(self.a.nr_agents, 2)
    self.assertEqual(list(self.a._property_sets.keys()), ['b'])

