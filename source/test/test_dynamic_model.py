import datetime
import unittest

import numpy as np

import campo

import lue.data_model as ldm


class TestDynamicModel(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):

        # Some dummy spatial domain
        with open('locations.csv', 'w') as content:
            content.write('1,2\n3,4\n5,6\n7,8')

        with open('extent.csv', 'w') as content:
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")

        self.ds = campo.Campo(seed=13)

        self.phen = self.ds.add_phenomenon('phen')
        self.phen.add_property_set('point', 'locations.csv')
        self.phen.add_property_set('field', 'extent.csv')



    def test_1(self):
        """ Dynamic model, stationary points and fields """

        # initial section
        self.phen.point.pdata = 500
        self.phen.field.fdata = 300

        # dummy time
        date = datetime.date(2000, 1, 1)
        time = datetime.time(0, 0)
        start = datetime.datetime.combine(date, time)
        unit = campo.TimeUnit.month
        stepsize = 1
        timesteps = 5

        # create the output lue data set
        self.ds.create_dataset("TestDynamicModel_test_1.lue")
        self.ds.set_time(start, unit, stepsize, timesteps)


        self.phen.point.pdata.is_dynamic = True
        self.phen.field.fdata.is_dynamic = True

        # write after modifying coordinates
        self.ds.write()

        # dynamic section
        for timestep in range(1, timesteps + 1):
            self.phen.point.pdata += 200
            self.phen.field.fdata += 100

            self.ds.write(timestep)
