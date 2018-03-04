""" Generate an Assortative Planted Partition Model and a clustered graph
signal over the model. See S. Basirian, A. Jung "Random Walk Sampling for Big
Data over Networks" for details.
"""
import pathlib
import argparse

import networkx as nx
import numpy as np

from utils import dump_graph
from visualization import draw_partitioned_graph

def get_uniform_signal(size):
  return np.random.uniform(0, 1, [size])

def get_integer_signal(size):
  return np.random.random_integers(1, size * 10, [size])

SIGNAL_GENERATORS = {
  'uniform': get_uniform_signal,
  'integer': get_integer_signal,
}

def parse_args():
  parser = argparse.ArgumentParser(
    description="Creates an Assortative Planted Partition Model")

  parser.add_argument("--sizes",
                      type=int,
                      default=[10,20,30,40],
                      nargs='*',
                      help="Sizes of the groups to generate")

  parser.add_argument("--p_in",
                      type=float,
                      default=0.3,
                      help="Probability of connecting vertices within a group")

  parser.add_argument("--p_out",
                      type=float,
                      default=0.05,
                      help="Probability of connecting vertices between groups")

  parser.add_argument("--visualize",
                      action="store_true",
                      default=False,
                      help="Plot the generated graph")

  parser.add_argument("--out_path",
                      default=None,
                      help="Save graph output to out_path")

  parser.add_argument("--cull_disconnected",
                      action="store_true",
                      dest="cull_disconnected",
                      help="Cull nodes that are not connected to the main"
                           " graph")

  parser.add_argument("--no_cull_disconnected",
                      action="store_false",
                      dest="cull_disconnected",
                      help="Use to leave nodes that are not connected to the"
                           " main graph")

  parser.add_argument("--connect_disconnected",
                      action="store_true",
                      dest="connect_disconnected",
                      help="Connect nodes that are not connected to the main"
                           " graph")

  parser.add_argument("--no_connect_disconnected",
                      action="store_false",
                      dest="connect_disconnected",
                      help="Use to leave nodes that are not connected to the"
                           " main graph")

  parser.add_argument("--generator_type",
                      type=str,
                      default="uniform",
                      help="Type of signal generator to use for cluster"
                           " values. Choose from"
                           " {}".format(list(SIGNAL_GENERATORS.keys())))

  parser.add_argument("--shuffle_labels",
                      action="store_true",
                      help="Relabel nodes with random integer labels from 0 to"
                            " number of nodes.")

  parser.add_argument("--no_shuffle_labels",
                      action="store_false",
                      help="Don't relabel nodes with random integer labels"
                           "from 0 to  number of nodes.")

  parser.set_defaults(cull_disconnected=True)
  parser.set_defaults(connect_disconnected=True)
  parser.set_defaults(shuffle_labels=False)

  args = vars(parser.parse_args())
  return args


def add_signal_to_graph(graph, signal):
  for cluster_value, partition in zip(
      signal, graph.graph["partition"]):
    for node_index in partition:
      graph.node[node_index]['value'] = cluster_value

def connect_disconnected_nodes(graph):
  connected_components = [c for c in sorted(nx.connected_components(graph),
                                            key=len,
                                            reverse=True)]
  for component in connected_components[1:]:
    random_node = np.random.choice(tuple(component))
    destination_node = np.random.choice(tuple(connected_components[0]))
    graph.add_edge(random_node, destination_node)

def cull_disconnected_nodes(graph):
  connected_components = [c for c in sorted(nx.connected_components(graph),
                                            key=len,
                                            reverse=True)]
  for component in connected_components[1:]:
    graph.remove_nodes_from(component)


def main(args):
  (sizes, p_in, p_out, generator_type) = (
      args["sizes"], args["p_in"], args["p_out"], args["generator_type"])
  visualize, out_path = args["visualize"], args["out_path"]

  cull_disconnected = args['cull_disconnected']
  connect_disconnected = args['connect_disconnected']
  shuffle_labels = args['shuffle_labels']

  appm = nx.random_partition_graph(sizes, p_in, p_out)
  signal_generator = SIGNAL_GENERATORS[generator_type]
  signal = signal_generator(len(args["sizes"]))
  add_signal_to_graph(appm, signal)

  if cull_disconnected:
    cull_disconnected_nodes(appm)
    appm = nx.relabel.convert_node_labels_to_integers(appm, 0)

  if connect_disconnected:
    connect_disconnected_nodes(appm)
    appm = nx.relabel.convert_node_labels_to_integers(appm, 0)

  if shuffle_labels:
    random_labels = list(range(appm.number_of_nodes()))
    np.random.shuffle(random_labels)
    mapping = {node: label for node, label in zip(appm.nodes(), random_labels)}
    appm = nx.relabel_nodes(appm, mapping, copy=True)

  if visualize:
    draw_partitioned_graph(appm)

  if out_path is not None:
    if out_path.strip(".").strip("/").split("/")[0] == "data":
      pathlib.Path('./data').mkdir(parents=True, exist_ok=True)
    dump_graph(appm, out_path)
  else:
    return appm

if __name__ == "__main__":
  args = parse_args()
  main(args)
