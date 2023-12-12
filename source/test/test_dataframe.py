import pathlib
import unittest

import numpy as np

import campo

import lue.data_model as ldm


class TestDataframe(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        pass

    @classmethod
    def setUpClass(self):
        pass

    def test_1(self):
        """ Coordinates of mobile agents """

        arr = np.empty((3, 2))
        arr[:,0] = np.array([1, 3, 5])
        arr[:,1] = np.array([2, 4, 6])

        dataset = ldm.open_dataset("TestMobileAgents_test_1.lue", "r")

        for timestep in range(1, 6):
            coords = campo.dataframe.coordinates(dataset, "a", "mobile_points", timestep)
            self.assertTrue(((arr + timestep) == coords).all())

    def test_2(self):
        """ Writing GeoPackage of mobile agents """

        arr = np.empty((3, 2))
        arr[:,0] = np.array([1, 3, 5])
        arr[:,1] = np.array([2, 4, 6])

        dataset = ldm.open_dataset("TestMobileAgents_test_1.lue", "r")
        dataframe = campo.dataframe.select(dataset.a, property_names=['mp'])

        for timestep in range(1, 6):
            coords = campo.dataframe.coordinates(dataset, "a", "mobile_points", timestep)
            tmp_df = campo.to_df(dataframe, timestep)
            campo.mobile_points_to_gpkg(coords, tmp_df, f"tmp_{timestep}.gpkg", 'EPSG:28992')


    def test_3(self):
        """ Writing GeoTiff stationary dynamic field agent """

        dataset = ldm.open_dataset("TestDynamicModel_test_1.lue", "r")
        df = campo.dataframe.select(dataset.phen, property_names=['fdata'])

        agent_id = 0
        crs = "EPSG:4326"
        directory = "TestDataframe"

        if not pathlib.Path(directory).exists():
            pathlib.Path(directory).mkdir()

        for timestep in range(1, 6):
            raster = df["phen"]["field"]["fdata"][agent_id][timestep - 1]
            filename = pathlib.Path(directory, f"fdata_{agent_id}_{timestep}.tiff")
            campo.to_geotiff(raster, filename, crs)
