import copy
import numpy
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

  for idx,i in enumerate(tmp_prop.values()):
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


  for idx,i in enumerate(tmp_prop.values()):
    neighbour_ids = numpy.nonzero(source_prop.values()[idx]>0)
    val = 0.0
    for n in neighbour_ids[0]:
      #nval = value_prop.values.values[n]
      nval = value_prop.values()[n]
      val += nval
    tmp_prop.values()[idx] = val / len(neighbour_ids[0])


  return tmp_prop
