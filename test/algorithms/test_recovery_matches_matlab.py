import networkx as nx
import numpy as np
from algorithms.recovery.sparse_label_propagation import (
  sparse_label_propagation,
)
import matplotlib.pyplot as plt
from pylab import stem, setp, show

LFR_GROUND_TRUTH = [3.979606662997337, 1.000242625480433, 1.99792236948117, 2, 2.992988448364223, 2, 4, 3.980117268042257, 1.997785710028256, 3, 3, 2.99591324294664, 1.997685078871964, 2.995421424626084, 1.99769788130109, 1.000459600757504, 3.979525664560459, 1.000115003425038, 0.9999999999999999, 3.979284301246234, 1.000172699370529, 3.979411482194054, 1.000389033063048, 1.000214404313962, 1.000236232907598, 3.979338573381184, 4, 1.000326872165087, 1.000192992535085, 3.979445146005451]

SYNTH_GROUND_TRUTH = [0.9898989898989899, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.576431220346167, 4.556636332700664, 4.536660254023168, 1.010101033218102, 1, 1.024194267886259, 1.045431326168368, 1.066207749170329, 4.782828318986993, 5, 4.712193149726601, 4.71340119492774, 4.713843370160276]

LFR_LABELS = [(0,4), (1,1), (2,2), (3,2), (4,3), (5,2), (6,4), (7,4), (8,2), (9,3), (10,3), (11,3), (12,2), (13,3), (14,2), (15,1), (16,4), (17,1), (18,1), (19,4), (20,1), (21,4), (22,1), (23,1), (25,1), (25,4), (26,4), (27,1), (28,1), (29,4)]

LFR_EDGES = [(0, 7), (0, 16), (0, 25), (0, 29), (1, 23), (1, 24), (1, 27), (1, 28), (2, 3), (2, 4), (2, 12), (2, 14), (3, 2), (3, 8), (3, 14), (3, 26), (4, 2), (4, 9), (4, 13), (4, 29), (5, 8), (5, 12), (5, 14), (5, 25), (6, 7), (6, 22), (6, 26), (6, 29), (7, 0), (7, 6), (7, 21), (7, 26), (8, 3), (8, 5), (8, 12), (8, 14), (9, 4), (9, 10), (9, 11), (9, 13), (10, 9), (10, 11), (10, 13), (11, 9), (11, 10), (11, 13), (12, 2), (12, 5), (12, 8), (12, 14), (13, 4), (13, 9), (13, 10), (13, 11), (14, 2), (14, 3), (14, 5), (14, 8), (14, 12), (15, 18), (15, 19), (15, 22), (15, 27), (15, 28), (16, 0), (16, 19), (16, 25), (16, 26), (16, 29), (17, 18), (17, 23), (17, 24), (17, 27), (17, 28), (18, 15), (18, 17), (18, 20), (18, 22), (18, 27), (18, 28), (19, 15), (19, 16), (19, 21), (19, 25), (19, 26), (19, 29), (20, 18), (20, 22), (20, 23), (20, 24), (20, 27), (20, 28), (21, 7), (21, 19), (21, 25), (21, 26), (21, 27), (21, 29), (22, 6), (22, 15), (22, 18), (22, 20), (22, 24), (22, 28), (23, 1), (23, 17), (23, 20), (23, 24), (23, 27), (23, 28), (24, 1), (24, 17), (24, 20), (24, 22), (24, 23), (24, 27), (24, 28), (25, 0), (25, 5), (25, 16), (25, 19), (25, 21), (25, 26), (25, 29), (26, 3), (26, 6), (26, 7), (26, 16), (26, 19), (26, 21), (26, 25), (26, 29), (27, 1), (27, 15), (27, 17), (27, 18), (27, 20), (27, 21), (27, 23), (27, 24), (28, 1), (28, 15), (28, 17), (28, 18), (28, 20), (28, 22), (28, 23), (28, 24), (29, 0), (29, 4), (29, 6), (29, 16), (29, 19), (29, 21), (29, 25), (29, 26)]

def test_recovery_matches_original():
  N = 100
  signal_template = [1,1,1,1,1,5,5,5,5,5]
  sampling_set = [1 + i * 5 for i in range(N // 5)]
  weights = [2 if i % 5 != 0 else 1 for i in range(1, N)]

  graph = nx.Graph()
  for index in range(N-1):
    weight = weights[index]
    graph.add_edge(index, index + 1, weight=weight)
    signal = signal_template[index % len(signal_template)]
    graph.node[index]['value'] = signal
  graph.node[N-1]['value'] = 5

  graph = nx.relabel.convert_node_labels_to_integers(graph, 0)
  slp_hatx = sparse_label_propagation(graph, sampling_set,
      params={'number_of_iterations': 99, 'lambda':1.0, 'alpha':2.0})

  assert np.allclose(np.array(SYNTH_GROUND_TRUTH), np.squeeze(slp_hatx))

def test_recovery_matches_original_lfr():
  labels = {}
  edgelist = {}
  for node_index, label in LFR_LABELS:
    labels[node_index] = label

  graph = nx.Graph()
  for start, end in LFR_EDGES:
    graph.add_edge(start, end)

  for node_index, label in labels.items():
    graph.node[node_index]['value'] = label
  sampling_set = [6, 9, 10, 18, 3, 26, 5]

  slp_hatx = sparse_label_propagation(graph, sampling_set,
      params={'number_of_iterations': 1999, 'lambda':1.0, 'alpha':2.0})
  assert np.allclose(np.squeeze(slp_hatx), np.array(LFR_GROUND_TRUTH))