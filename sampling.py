import json
import argparse
from pprint import pprint
from distutils.util import strtobool
from datetime import datetime

import numpy as np

from algorithms import sampling
from utils import dump_results

def bool_type(x):
  return bool(strtobool(x))

DEFAULT_SAMPLING_METHOD = "RandomWalkSampling"

def parse_args():
  parser = argparse.ArgumentParser(
    description=("Graph Sampling: Script to generate sampling set from a"
                 "signal graph"))


  parser.add_argument("-v", "--verbose",
                      type=bool_type,
                      default=False,
                      help="Verbose")

  parser.add_argument("--graph-file",
                      type=str,
                      required=True,
                      help="Path to the graph file to be loaded for sampling")

  parser.add_argument("--sampling-method",
                      type=str,
                      default=DEFAULT_SAMPLING_METHOD,
                      help=("Name of the class used for graph sampling. The"
                            " sampling class must be importable from"
                            "algorithms.sampling module. Defaults to '{0}',"
                            " i.e. algorithms.sampling.{0}."
                            "".format(DEFAULT_SAMPLING_METHOD)))

  parser.add_argument("--sampling-params",
                      type=json.loads,
                      default={},
                      help=("Sampling algorithms parameters passed in json"
                            " format. These are passed directly to the"
                            " sampling method constructor"))

  parser.add_argument("--results-file", default=None, type=str,
                      help="File to write results to")

  args = vars(parser.parse_args())

  return args

def main(args):
  if args.get('verbose', False):
    print(args)

  sampling_method_name = args["sampling_method"]
  sampling_params = args["sampling_params"]

  SamplingMethodClass = getattr(sampling, sampling_method_name)

  graph = args.get("graph")
  if graph is not None:
    sampling_method = SamplingMethodClass(graph, sampling_params)
  else:
    graph_file = args["graph_file"]
    sampling_method = SamplingMethodClass(graph_file, sampling_params)

  results = args.copy()

  run_results = sampling_method.run()

  results.update(run_results)

  results_file = args.get("results_file")
  if results_file is None:
    return results
  else:
    dump_results(results, results_file)

if __name__ == "__main__":
  args = parse_args()
  main(args)
