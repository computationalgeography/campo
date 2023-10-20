import unittest

import numpy as np

import campo


class TestProperty(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):

        with open('locations.csv', 'w') as content:
            content.write('1,2\n3,4\n5,6\n7,8')

        self.ds = campo.Campo(seed=13)

        self.a = self.ds.add_phenomenon('a')
        self.a.add_property_set('b', 'locations.csv')

    def test_1(self):
        """ Agents getting same values """

        self.a.b.c = 500
        arr = np.array([500, 500, 500, 500], dtype=np.int32)

        for idx, value in enumerate(self.a.b.c.values()):
            self.assertEqual(arr[idx], value[0])

    def test_2(self):
        """ Agents getting values from normal distribution """
        self.a.b.lower = -8
        self.a.b.upper = 2
        self.a.b.c = campo.normal(self.a.b.lower, self.a.b.upper)

        arr = np.array([-4.34648688, -14.15666382, -6.08387205, -7.86072554])
        for idx, value in enumerate(self.a.b.c.values()):
            self.assertAlmostEqual(arr[idx], value[0])

    def test_3(self):
        """ Agents getting values from uniform distribution """
        self.a.b.lower = -4
        self.a.b.upper = 10
        self.a.b.c = campo.uniform(self.a.b.lower, self.a.b.upper)

        arr = np.array([-2.91920759, 9.25052093, 4.59308367, -3.96316945])
        for idx, value in enumerate(self.a.b.c.values()):
            self.assertAlmostEqual(arr[idx], value[0])
