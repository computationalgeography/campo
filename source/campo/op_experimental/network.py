import copy
import numpy
import random
import networkx as nx

from ..values import Values


def neighbour_network(nodes, neighbours, probability, seed=None):

    G = nx.watts_strogatz_graph(n=nodes, k=neighbours, p=probability, seed=seed)

    a = nx.to_numpy_array(G, dtype=numpy.int8)

    # To avoid that location 0 always corresponds to node 0 we shuffle the nework
    # this may lead to locations pointing at themselves?!
    #numpy.random.shuffle(a)

    return a


def network_average_def(source_prop, value_prop, default):

    tmp_prop = copy.deepcopy(source_prop)

    shapes = [()] * tmp_prop.nr_objects

    tmp_prop._values = Values(tmp_prop.nr_objects, shapes, numpy.nan)

    for idx, i in enumerate(tmp_prop.values()):
        neighbour_ids = numpy.nonzero(source_prop.values()[idx]>0)
        val = 0.0
        if len(neighbour_ids[0]) == 0:
            tmp_prop.values()[idx] = default.values()[0]
        else:
            for n in neighbour_ids[0]:
                nval = value_prop.values()[n]
                val += nval
            tmp_prop.values()[idx] = val / len(neighbour_ids[0])

    return tmp_prop


def network_average(source_prop, value_prop, fname):

    tmp_prop = copy.deepcopy(value_prop)

    for idx, i in enumerate(tmp_prop.values()):
        neighbour_ids = numpy.nonzero(source_prop.values()[idx]>0)
        val = 0.0
        for n in neighbour_ids[0]:
            #nval = value_prop.values.values[n]
            nval = value_prop.values()[n]
            val += nval
        tmp_prop.values()[idx] = val / len(neighbour_ids[0])

    return tmp_prop


def spread_neighbours(neighbours, threshold, random_seed, breeds, mask, albedos, ages, seed=None):

    if seed:
        random.seed(seed)

    nr_agents = len(mask.values().values)
    shape = threshold.values().values[0].shape
    thresh = threshold.values().values[0].reshape(shape[0] * shape[1])
    mask_val = numpy.zeros(len(mask.values().values))
    new_mask = numpy.zeros(len(mask.values().values))

    for idx, it in enumerate(mask.values()):
        mask_val[idx] = it
        new_mask[idx] = it
    rseed = random_seed.values().values
    breed = breeds.values().values
    albedo = albedos.values().values
    age = ages.values().values

    for agent_id, neigh in enumerate(neighbours.values()):
        is_active =  mask_val[agent_id] == 1

        # only actives of the current timestep do something
        if is_active:
            agent_breed = int(breed[agent_id])
            agent_albedo = albedo[agent_id]
            tr = thresh[agent_id]
            seed_value = rseed[agent_id][0]
            wneigh = neigh.copy()
            wneigh[agent_id] = 0

            if seed_value < tr:
                empty = []
                # determine free neighbours, also exclude the newly seeded
                for nidx in range(0, nr_agents):
                    if wneigh[nidx] == 1 and new_mask[nidx] == -1:
                        empty.append(nidx)

                # select one free one...
                if len(empty) > 0:
                    select = random.choice(empty)

                    # update mask
                    new_mask[select] = 1
                    # and others
                    breed[select] = numpy.array([float(agent_breed)])
                    albedo[select] = agent_albedo
                    age[select] = numpy.array([1])

    # update mask with new alives
    for idx, v in enumerate(mask.values()):
        mask.values()[idx] = numpy.array([new_mask[idx]])

