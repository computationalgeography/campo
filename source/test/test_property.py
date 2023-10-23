import unittest

import numpy as np

import campo


class TestProperty(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):

        # Some dummy spatial domain
        with open('locations.csv', 'w') as content:
            content.write('1,2\n3,4\n5,6\n7,8')

        with open('extent.csv', 'w') as content:
            content.write("0,0,20,40,2,3\n")
            content.write("0,0,20,30,2,3\n")
            content.write("0,0,20,30,2,3\n")
            content.write("0,0,20,30,2,3\n")

        self.ds = campo.Campo(seed=13)

        self.a = self.ds.add_phenomenon('a')
        self.a.add_property_set('b', 'locations.csv')
        self.a.add_property_set('field', 'extent.csv')

    def test_1(self):
        """ Point agents getting same values """

        self.a.b.c = 500
        arr = np.array([500, 500, 500, 500], dtype=np.int32)

        for idx, value in enumerate(self.a.b.c.values()):
            self.assertEqual(arr[idx], value[0])

    def test_2(self):
        """ Point agents getting values from normal distribution """
        self.a.b.lower = -8
        self.a.b.upper = 2
        self.a.b.c = campo.normal(self.a.b.lower, self.a.b.upper)

        arr = np.array([-4.34648688, -14.15666382, -6.08387205, -7.86072554])
        for idx, value in enumerate(self.a.b.c.values()):
            self.assertAlmostEqual(arr[idx], value[0])

    def test_3(self):
        """ Point agents getting values from uniform distribution """
        self.a.b.lower = -4
        self.a.b.upper = 10
        self.a.b.c = campo.uniform(self.a.b.lower, self.a.b.upper)

        arr = np.array([-2.91920759, 9.25052093, 4.59308367, -3.96316945])
        for idx, value in enumerate(self.a.b.c.values()):
            self.assertAlmostEqual(arr[idx], value[0])

    def test_4(self):
        """ Field agents getting same values """

        self.a.field.c = 500
        arr = np.empty((2, 3), dtype=np.int32)
        arr.fill(500)

        for idx, value in enumerate(self.a.field.c.values()):
            self.assertEqual(True, (arr==value).all())


    def test_5(self):
        """ Field agents getting values from normal distribution """
        self.a.field.lower = -8
        self.a.field.upper = 2
        self.a.field.c = campo.normal(self.a.field.lower, self.a.field.upper)

        arr = np.array([[[-9.03245889, -6.83903016, -7.13578628],
                        [-8.71367871, -8.49460764, -6.56111864]],
                        [[ -6.59136801, -8.98786846, -8.73542745],
                        [-11.61358078, -4.64158507, -8.44858176]],
                        [[-5.32544514, -7.16506881, -4.11207445],
                        [-4.92578005, -7.36340312, -5.03847316]],
                        [[ -9.90024704, -5.48276371, -10.96084726],
                        [ -7.31352726, -5.87024706, -7.55273572]]])
        for idx, value in enumerate(self.a.field.c.values()):
            self.assertEqual(True, (np.isclose(arr[idx], value).all()))


    def test_6(self):
        """ Field agents getting values from uniform distribution """
        self.a.field.lower = -4
        self.a.field.upper = 10
        self.a.field.c = campo.uniform(self.a.field.lower, self.a.field.upper)

        arr = np.array([[[ 3.66782514, -3.27845639,  6.34921597],
                        [ 0.48982114, -2.96453377,  9.41855647]],
                        [[ 5.23539849,  2.38096144,  6.25712054],
                        [ 2.69046043, -2.25390133,  4.46411843]],
                        [[6.45710994,  6.4180556,  3.72194362],
                        [8.99888128,  9.23997587, 8.24817527]],
                        [[ 1.20301089, -0.25121896,  3.41736776],
                        [ 5.16034298, -1.75169424,  3.8325035 ]]])

        for idx, value in enumerate(self.a.field.c.values()):
            self.assertEqual(True, (np.isclose(arr[idx], value).all()))


    def test_7(self):
        """ Point agents getting values from random_integers distribution """
        self.a.b.lower = -25
        self.a.b.upper = 25
        self.a.b.c = campo.random_integers(self.a.b.lower, self.a.b.upper)

        arr = np.array([10, -4, -3, -25])
        for idx, value in enumerate(self.a.b.c.values()):
            self.assertEqual(arr[idx], value[0])


    def test_8(self):
        """ Field agents getting values from random_integers distribution """
        self.a.field.lower = -4
        self.a.field.upper = 10
        self.a.field.c = campo.random_integers(self.a.field.lower, self.a.field.upper)

        arr = np.array([[[ 5,  1, -3],
                        [ 1, -4,  9]],
                        [[-2, -4,  6],
                        [ 8, -1,  8]],
                        [[-2,  4,  5],
                        [-2, -2,  7]],
                        [[ 2, -2,  7],
                        [ 0,  0,  5]]])

        for idx, value in enumerate(self.a.field.c.values()):
            self.assertEqual(True, (arr[idx]==value).all())
