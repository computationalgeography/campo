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
        with open("locations.csv", "w") as content:
            content.write("1,2\n3,4\n5,6\n7,8")

        with open("extent.csv", "w") as content:
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")
            content.write("0,0,30,20,2,3\n")

        self.ds = campo.Campo(seed=13)

        self.phen = self.ds.add_phenomenon("phen")
        self.phen.add_property_set("point", "locations.csv")
        self.phen.add_property_set("field", "extent.csv")

        # dummy time
        date = datetime.date(2000, 1, 1)
        time = datetime.time(0, 0)
        self.start = datetime.datetime.combine(date, time)
        self.unit = campo.TimeUnit.month
        self.stepsize = 1
        self.timesteps = 5

    def test_1(self):
        """ Stationary points and fields """

        # initial section
        self.phen.point.pdata = 500
        self.phen.field.fdata = 300

        # create the output lue data set
        filename = "TestDynamicModel_test_1.lue"
        self.ds.create_dataset(filename)
        self.ds.set_time(self.start, self.unit, self.stepsize, self.timesteps)

        self.phen.point.pdata.is_dynamic = True
        self.phen.field.fdata.is_dynamic = True

        # write after modifying coordinates
        self.ds.write()

        # dynamic section
        for timestep in range(1, self.timesteps + 1):
            self.phen.point.pdata += 200
            self.phen.field.fdata += 100

            self.ds.write(timestep)

        # ldm.assert_is_valid(filename)

    def test_2(self):
        """ Points and fields different phenomena """

        # initial section
        ds = campo.Campo(seed=13)

        phen1 = ds.add_phenomenon("phen1")
        phen2 = ds.add_phenomenon("phen2")

        phen1.add_property_set("point", "locations.csv")
        phen2.add_property_set("field", "extent.csv")

        phen1.point.pdata = 500
        phen2.field.fdata = 300

        # create the output lue data set
        filename = "TestDynamicModel_test_2.lue"
        ds.create_dataset(filename)
        ds.set_time(self.start, self.unit, self.stepsize, self.timesteps)

        phen1.point.pdata.is_dynamic = True
        phen2.field.fdata.is_dynamic = True

        # write after modifying coordinates
        ds.write()

        # dynamic section
        for timestep in range(1, self.timesteps + 1):
            phen1.point.pdata += 200
            phen2.field.fdata += 100
            ds.write(timestep)

        dataset = ldm.open_dataset(filename, "r")
        pset_points = dataset.phenomena["phen1"].property_sets["point"]
        pset_fields = dataset.phenomena["phen2"].property_sets["field"]

        nr_pagents = len(dataset.phenomena["phen1"].object_id[:])
        nr_fagents = len(dataset.phenomena["phen2"].object_id[:])
        self.assertTrue(nr_pagents == 4)
        self.assertTrue(nr_fagents == 4)

        pvalues = pset_points.pdata.value[:]
        fvalues = pset_fields.fdata.value[0][:]

        pvalid = np.repeat([700, 900, 1100, 1300, 1500], nr_pagents).reshape(self.timesteps, nr_pagents).T
        rows = 2
        cols = 3
        fvalid = np.repeat([400, 500, 600, 700, 800], rows * cols).reshape(self.timesteps, rows, cols)

        self.assertTrue(np.array_equal(fvalues, fvalid))
        self.assertTrue(np.array_equal(pvalues, pvalid))
