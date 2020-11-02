import unittest
import os
import sys

import campo



class TestPropertyset(unittest.TestCase):

  @classmethod
  def tearDownClass(self):
    pass

  @classmethod
  def setUpClass(self):

    with open('locations.csv', 'w') as content:
      content.write('1,2\n3,4')

    self.ds = campo.Campo()

    self.a = self.ds.add_phenomenon('a')
    self.a.add_property_set('b1', 'locations.csv')
    self.a.add_property_set('b2', 'locations.csv')
    self.a.b1.c = 500



  def test_1(self):
      """ accessing non-existing property """

      with self.assertRaises(Exception) as context_manager:
          self.a.b1.notfound

      self.assertRegex(str(context_manager.exception),
          "No property 'notfound' in property set 'b1'")
