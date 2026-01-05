import os
import numpy as np

import pcraster as pcr

import lue.data_model as ldm

from .points import Points
from .areas import Areas
from .phenomenon import Phenomenon
from .utils import _color_message

import campo.config as cc


class Campo(object):
    """ """

    def __init__(self, seed=None, cpus=1, debug=False):

        self._phenomena = {}
        self._nr_timesteps = None
        self._lue_time_configuration = None
        self.lue_filename = None

        self._debug = debug

        self._start_timestep = None
        self._clock_unit_value = None
        self._clock_stepsize = None

        if seed is None:
            cc.rng = np.random.default_rng()
        else:
            cc.seed = seed
            pcr.setrandomseed(cc.seed)
            cc.rng = np.random.default_rng(cc.seed)

        if cpus > 1:
            cc.cpus = cpus
            raise NotImplementedError(f"WIP cpus")

    def __repr__(self, indent=0):
        msg = '{}Campo:\n'.format('  ' * indent)
        if len(self._phenomena) == 0:
            msg += '{}Phenomena: 0'.format('  ' * (indent+1))
        else:
            for p in self._phenomena:
                msg += self._phenomena[p].__repr__(indent + 1)

        return msg

    def _add_framework(self, nr_objects):
        """      """

        # LUE
        self.lue_dataset.add_phenomenon('framework')
        tmp = self.lue_dataset.phenomena['framework']

        lue_time_extent = tmp.add_property_set(
                "fame_time_cell",
                ldm.TimeConfiguration(ldm.TimeDomainItemType.box), self.lue_clock)

        # just a number, TODO sampleNumber?
        simulation_id = 1

        # dynamic...
        time_cell = tmp.property_sets["fame_time_cell"]

        time_boxes = 1

        #time_cell.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = np.arange(0, nr_objects, dtype=np.dtype(np.uint64))

        #time_cell.object_tracker.active_object_index.expand(time_boxes * nr_objects)[:] = list(np.zeros(nr_objects, dtype=np.dtype(np.uint64)))

        time_cell.object_tracker.active_set_index.expand(time_boxes)[:] = 0

        #time_domain = point_pset.time_domain
        time_cell.time_domain.value.expand(time_boxes)[:] = [0, self._nr_timesteps]

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def add_phenomenon(self, phenomenon_name):

        if phenomenon_name in self._phenomena:
            msg = "'{}' is already present as phenomenon name".format(phenomenon_name)
            raise ValueError(msg)

        phen = Phenomenon(phenomenon_name)
        self._phenomena[phenomenon_name] = phen

        return phen

    def create_dataset(self, filename, working_dir=os.getcwd()):
        """ """
        fpath = os.path.join(working_dir, filename)

        root, ext = os.path.splitext(fpath)
        if ext == '':
            fpath += '.lue'

        if os.path.exists(filename):
            os.remove(filename)

        self.lue_filename = fpath

        ldm.create_dataset(self.lue_filename)

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def _generate_lue_property(self, phen_name, property_set, prop):

        dataset = ldm.open_dataset(self.lue_filename, 'w')

        pset = dataset.phenomena[phen_name].property_sets[property_set.name]

        dtype = prop.values().values[0].dtype

        nr_objects = prop.nr_objects

        if isinstance(property_set.space_domain, Points):

            if prop.is_dynamic:
                time_boxes = 1
                p_shape = (self._nr_timesteps,)
                lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), shape=p_shape, value_variability=ldm.ValueVariability.variable)
                lue_prop.value.expand(nr_objects)

                # Just create these once...
                if pset.object_tracker.active_object_id.nr_ids == 0:
                    pset.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = dataset.phenomena[phen_name].object_id[:]
                    pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0

                    time_domain = pset.time_domain
                    time_domain.value.expand(time_boxes)[:] = np.array([0, self._nr_timesteps])
            else:
                lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype))
                lue_prop.value.expand(nr_objects)

        elif isinstance(property_set.space_domain, Areas):

            if prop.is_dynamic:
                time_boxes = 1
                lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), rank=2,
                  shape_per_object=ldm.ShapePerObject.different,
                  shape_variability=ldm.ShapeVariability.constant)

                # Just create these once...
                if pset.object_tracker.active_object_id.nr_ids == 0:
                    pset.object_tracker.active_object_id.expand(time_boxes * nr_objects)[:] = dataset.phenomena[phen_name].object_id[:]
                    pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0

                    time_domain = pset.time_domain
                    time_domain.value.expand(time_boxes)[:] = np.array([0, self._nr_timesteps])
            else:
                # Same shape
                # prop = pset.add_property(property_name, dtype=np.dtype(dtype), shape=shape)

                # Different shape
                lue_prop = pset.add_property(prop.name, dtype=np.dtype(dtype), rank=2)

            space_discr = pset.campo_discretization

            # if number of rows/columns not yet set...
            if pset.campo_discretization.value[0][0] == 0 and pset.campo_discretization.value[0][1] == 0:

                shapes = np.arange(1, nr_objects * 2 + 1, dtype=ldm.dtype.Count) \
                              .reshape(nr_objects, 2)

                for idx, item in enumerate(property_set.space_domain):
                    shapes[idx] = [item[4], item[5]]

                space_discr.value[:] = shapes

            rank = 2
            if prop.is_dynamic:
                for idx, item in enumerate(property_set.space_domain):
                    lue_prop.value.expand(idx, tuple([item[4], item[5]]), self._nr_timesteps)
            else:
                shapes = np.zeros(nr_objects * rank, dtype=ldm.dtype.Count).reshape(nr_objects, rank)

                for idx, item in enumerate(property_set.space_domain):
                    shapes[idx][0] = item[4]
                    shapes[idx][1] = item[5]

                lue_prop.value.expand(dataset.phenomena[phen_name].object_id[:], shapes)

            lue_prop.set_space_discretization(
                ldm.SpaceDiscretization.regular_grid,
                space_discr)

        else:
            raise NotImplementedError

        dataset = None

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def _generate_lue_property_set(self, phen_name, property_set):

        dataset = ldm.open_dataset(self.lue_filename, 'w')

        rank = -1
        space_type = None
        space_configuration = None
        static = False
        if self._lue_time_configuration is None:
            static = True

        if isinstance(property_set.space_domain, Points):
            space_type = ldm.SpaceDomainItemType.point
            rank = 2
        else:
            space_type = ldm.SpaceDomainItemType.box
            rank = 2

        if(property_set.is_mobile and not static):
            space_configuration = ldm.SpaceConfiguration(
               ldm.Mobility.mobile,
               space_type
               )
        else:
            space_configuration = ldm.SpaceConfiguration(
                ldm.Mobility.stationary,
                space_type
                )

        if static:
            tmp_pset = dataset.phenomena[phen_name].add_property_set(property_set.name, space_configuration, np.dtype(np.float64), rank=rank)
        else:
            epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, self._start_timestep, ldm.Calendar.gregorian)
            clock = ldm.Clock(epoch, self._clock_unit_value, self._clock_stepsize)
            time_configuration = ldm.TimeConfiguration(ldm.TimeDomainItemType.box)
            tmp_pset = dataset.phenomena[phen_name].add_property_set(property_set.name, time_configuration, clock, space_configuration, np.dtype(np.float64), rank=rank)

        tmp_pset = dataset.phenomena[phen_name].property_sets[property_set.name]

        space_coordinate_dtype = tmp_pset.space_domain.value.dtype

        # Assign coordinates
        if space_type == ldm.SpaceDomainItemType.point:

            nr_timesteps_and_objects = None
            if (property_set.is_mobile):
                    # Coordinates per timestep
                nr_timesteps_and_objects = property_set.nr_objects * self._nr_timesteps
            else:
                nr_timesteps_and_objects = property_set.nr_objects

            tmp_values = np.empty((nr_timesteps_and_objects, 2), dtype=space_coordinate_dtype)

            # only for the initial
            for idx, item in enumerate(property_set.space_domain):
                tmp_values[idx, 0] = item[0]
                tmp_values[idx, 1] = item[1]

            tmp_pset.space_domain.value.expand(nr_timesteps_and_objects)[-nr_timesteps_and_objects:] = tmp_values

            time_boxes = 1

            if tmp_pset.object_tracker.active_object_id.nr_ids == 0:
                tmp_pset.object_tracker.active_object_id.expand(time_boxes * nr_timesteps_and_objects)[:] = np.arange(nr_timesteps_and_objects)
                tmp_pset.object_tracker.active_set_index.expand(time_boxes)[:] = 0
                if not static:
                    time_domain = tmp_pset.time_domain
                    time_domain.value.expand(time_boxes)[:] = np.array([0, self._nr_timesteps])

        elif space_type == ldm.SpaceDomainItemType.box:

            tmp_values = np.empty((property_set.nr_objects, 4), dtype=tmp_pset.space_domain.value.dtype)

            for idx, item in enumerate(property_set.space_domain):
                tmp_values[idx, 0] = item[0]
                tmp_values[idx, 1] = item[1]
                tmp_values[idx, 2] = item[2]
                tmp_values[idx, 3] = item[3]

            tmp_pset.space_domain.value.expand(property_set.nr_objects)[-property_set.nr_objects:] = tmp_values

            # For fields we also add a discretisation property
           # tmp_prop = tmp_location.add_property('fame_discretization', dtype=np.dtype(np.int64), shape=(1,2), value_variability=lue.ValueVariability.constant)
           # tmp_prop.value.expand(self._nr_objects)
           # for idx, item in enumerate(space_domain):
           #   tmp_prop.value[idx]= [item[4], item[5]]

            tmp_prop = tmp_pset.add_property('campo_discretization', dtype=ldm.dtype.Count, shape=(2,))
            tmp_prop.value.expand(property_set.nr_objects)

        else:
            raise NotImplementedError

        for prop in property_set.properties.values():
            self._generate_lue_property(phen_name, property_set, prop)

        dataset = None

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def _generate_lue_phenomenon(self,  phenomenon):
        pset = next(iter(phenomenon.property_sets.values()))

        nr_objects = pset.nr_objects

        dataset = ldm.open_dataset(self.lue_filename, 'w')

        dataset.add_phenomenon(phenomenon.name)
        tmp = dataset.phenomena[phenomenon.name]
        tmp.object_id.expand(nr_objects)[:] = np.arange(nr_objects, dtype=ldm.dtype.ID)

        for p in phenomenon.property_sets.values():
            self._generate_lue_property_set(phenomenon.name, p)

        dataset = None

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def _lue_write_property(self, phen_name, pset, prop, timestep):
        dataset = ldm.open_dataset(self.lue_filename, 'w')

        # todo restructure this method...

        # if possible return without performing disk access
        if not prop.is_dynamic:
            # do not write 'static' data in dynamic section
            if timestep is not None:
                return

        lue_pset = dataset.phenomena[phen_name].property_sets[pset.name]
        object_ids = dataset.phenomena[phen_name].object_id[:]

        if pset._lue_filename is None:
            pset._lue_filename = self.lue_filename

        # Agents mobile during time
        if(pset.is_mobile and timestep is not None):
            coord_start_idx = len(object_ids) * (timestep - 1)
            coord_end_idx = coord_start_idx + len(object_ids)

            campo_pset = self._phenomena[phen_name].property_sets[pset.name]
            campo_coords_ts = campo_pset.space_domain._get_coordinates()

            lue_pset.space_domain.value[coord_start_idx:coord_end_idx] = campo_coords_ts

        # Writing property values
        if not prop.is_dynamic:
            lue_prop = lue_pset.properties[prop.name]
            if isinstance(prop.space_domain, Points):
                for idx, val in enumerate(prop.values().values):
                    lue_prop.value[idx] = prop.values().values[idx]
            elif isinstance(prop.space_domain, Areas):
                for idx, val in enumerate(prop.values().values):
                    lue_prop.value[object_ids[idx]][:] = prop.values().values[idx]
            else:
                raise NotImplementedError

        else:
            if timestep is not None:
                lue_prop = lue_pset.properties[prop.name]
                if isinstance(prop.space_domain, Points):
                    for idx, val in enumerate(prop.values().values):
                        #lue_prop.value[:][idx, timestep - 1] = prop.values().values[idx]
                        tmp = lue_prop.value[idx]
                        tmp[timestep - 1] = prop.values().values[idx]
                        lue_prop.value[idx] = tmp
                else:
                    for idx, val in enumerate(prop.values().values):
                        lue_prop.value[object_ids[idx]][timestep - 1] = prop.values().values[idx]

        dataset = None

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)

    def write(self, timestep=None):
        """ Writing current state to a LUE dataset

        :param timestep: None for initial, integer timestep number otherwise
        """

        dataset = ldm.open_dataset(self.lue_filename, 'r')
        # Get list of phenomena such that we can close the dataset immediately
        dataset_phenomena = dataset.phenomena.names
        dataset = None

        for p in self._phenomena:
            if not p in dataset_phenomena:
                self._generate_lue_phenomenon(self._phenomena[p])

        for phen in self._phenomena:
            for pset in self._phenomena[phen].property_sets.values():
                for prop in pset.properties.values():
                    self._lue_write_property(phen, pset, prop, timestep)

    def set_time(self, start, unit, stepsize, nrTimeSteps):
        """  """
        self._start_timestep = start.isoformat()
        self._nr_timesteps = nrTimeSteps
        self._clock_unit_value = unit.value
        self._clock_stepsize = stepsize

        if (not self.lue_filename):
            msg = _color_message(f"Dataset filename not yet specified, use create_dataset before")
            raise RuntimeError(msg)

        epoch = ldm.Epoch(ldm.Epoch.Kind.common_era, self._start_timestep, ldm.Calendar.gregorian)
        clock = ldm.Clock(epoch, self._clock_unit_value, self._clock_stepsize)

        self._lue_time_configuration = True
        time_configuration = ldm.TimeConfiguration(ldm.TimeDomainItemType.box)

        dataset = ldm.open_dataset(self.lue_filename, 'w')
        dataset.add_phenomenon('framework')
        tmp = dataset.phenomena['framework']

        tmp.add_property_set(
                "campo_time_cell",
                time_configuration, clock)

        # dynamic...
        time_cell = tmp.property_sets["campo_time_cell"]

        time_boxes = 1

        time_cell.object_tracker.active_set_index.expand(time_boxes)[:] = 0
        time_cell.time_domain.value.expand(time_boxes)[:] = np.array([0, self._nr_timesteps])

        dataset = None

        if self._debug:
            ldm.assert_is_valid(self.lue_filename)
