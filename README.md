# Reinforcement Learning for Graph Signal Recovery
This project implements a reinforcement learning approach for graph sampling in
graph signal recovery problems. Reinforcement learning policy is trained to
walk a graph and sample nodes. Sparse label propagation is applied to the
sampled nodes to recover the graph signal. Tools for the training and
evaluation of rl algorithms for the sampling problem are provided.

## Installation and Dependencies

The project requires Python 3.6

Python package dependencies:

* OpenAI Gym
* OpenAI Baselines
* Numpy
* TensorFlow 1.3
* Networkx 2.0
* Matplotlib
* Pygame

All package dependencies can be installed by running:

``` bash
pip install -r requirements.txt
```

## Running Experiments

Reinforcement learning experiments are implemented in files contained in
`experiments/` directory. The experiment files are executable. Experiments
support visualization. After training experiment for a while, results of the
latest experiment can be visualized with:

``` bash
python experiments/ppo_graph_sampling_env.py --step visualize
```

## Experiments Contained in the project

The experiments are executed by running the experiment files. Experiments log
results to subdirectories of `results/` directory. JSON formatted training logs
are provided for the reinforcement learning. See `visualization.py` for
examples how to process the logs.

### experiment1
`experiments/experiment1.py` contains code to reproduce experiments from
[Random Walk Sampling for Big Data over
Networks](https://arxiv.org/abs/1704.04799v1). See end of document for details.

### graph_sampling_env
`experiments/graph_sampling_env.py` trains deep Q-learning agent in the
GraphSamplingEnv. Details about the environment design can be found in the next
section.

### ppo_graph_sampling_env
`experiments/ppo_graph_sampling_env.py` trains PPO agent in the
SimpleActionsGraphSamplingEnv. PPO refers to Proximal Policy Optimization. The
PPO implementation is from [OpenAI
baselines](https://github.com/openai/baselines). The graph, observations and
rewards in SimpleActionsGraphSamplingEnv are similar to GraphSamplingEnv.
Instead of crawling the graph as described in the following section, in
SimpleActionsGraphSamplingEnv the actions pick nodes directly to the sampling
set. That means there are as many actions as there are nodes in the graph.

### simple_three_cluster_env
`experiments/simple_three_cluster_env.py` train deep Q-learning agent in a
small, fixed graph to check that the actions are compatible with Q-learning.

## Graph Sampling RL Environment
Graph sampling is formulated as a reinforcement learning problem by defining an
agent that is capable of moving along the graph edges and choosing nodes to
sample, guided by observations and rewards from the environment. The actions of
the agent are moving along the graph edges and sampling nodes. The reward is
defined in terms of the error of the recovered graph signal and the
observations summarize local characteristics of the graph surrounding the
agent. The environment implements the [OpenAI
Gym](https://github.com/openai/gym) environment API, which makes it easy to use
various high performance algorithms with it. The graph sampling environment is
defined in `envs/graph_sampling_env.py`.

The current implementation of the sampling environment is only an initial draft
of the ideas and thus, although it's fully functional, it's not likely to work
for training efficient sampling agents.

### The Graph
At the start of each training run, the environment generates a random
assortative planted partition model. The graph generator is implemented in
`generate_appm.py`. The idea is to train the agent on random graphs forcing it
to learn to generalize across different instances of the graphs.

### Actions
The agent picks actions to move along the edges of the graph and sample
nodes. The high performing reinforcement learning models are limited to fixed
size inputs and outputs, but APPM and other types of graphs may have arbitrary
numbers of nodes and edges.  The degree of the nodes may vary as well. In
order to fix the size of the the action space, we reduce the movement actions
into binary choices following ideas presented in Section 5.2 of [Information
Theory of Decisions and
Actions](https://link.springer.com/chapter/10.1007/978-1-4419-1452-1_19).
Specifically, the environment keeps track of the node the agent is located in
and the currently selected edge. The agent always faces a binary choice of
either moving along the selected edge or advancing to the next edge.

In addition to the two movement actions, the agent can choose to sample the
current node. After sampling the node, the node is added to the sampling set,
reward is computed and the agent is transported to a new random node in the
graph. If the sampling budget is reached, the training episode ends and no
further rewards are available to the agent.

### Observations
The observations summarize characteristics of the graph. Currently, the
observations consist of the local clustering coefficients and degrees of the
nodes close to the agent. To keep the observation size fixed, the statistics of
the neighboring nodes are represented through min, max and mean. In addition,
the clustering coefficient and the degree of the current node and the next node
are presented as is.

### Reward
Each time a node is sampled, the agent receives a reward. After sampling a new
node, the signal recovery algorithm is run. The error of the recovered signal
is used to compute the reward.

### Notes
The current implementation of the environment is unfinished and unlikely to
yield strong sampling performance.

* Randomizing the agent location after each sample is obtained seems like it's
  beating the purpose of the learning algorithm to some extent. If we are able
  to provide the agent with a more global view to the graph, this limitation
  can hopefully be lifted.
* The observations are subject to change in the future iterations of the
  environment.
* The reward computation is work in progress and will be rethought and
  reimplemented soon.
* There are multiple ways to split the actions down into a fixed set of
  actions. The other ways are currently low priority on the list of things to
  experiment with.

## Running RL in the Graph Sampling Environment
Reinforcement learning algorithms implemented in the [OpenAI
Baselines](https://github.com/openai/baselines/) can be used directly with the
graph sampling enviroment. In `experiment2.py` code is provided for running the
Deep Q-Learning agent in the Graph Sampling Environment. Experimental results
will be made available following progress with the environment.

## Random Walk Sampling
Random walk sampling as presented in [Random Walk Sampling for Big Data over
Networks](https://arxiv.org/abs/1704.04799v1) is implemented in
`algorithms/sampling/random_walk_sampling.py`. The results in the paper for
signal recovery on generated appms with random walk sampling in can be
reproduced by running `experiment1.py`, which consists of three steps: graph generation, sampling, and recovery. First, to generate the graphs:

```
python ./experiment1.py \
       --step=graph_generate \
       --cluster_sizes 10 20 30 40 \
       --p=0.3 \
       --q=0.04 \
       --num_graphs=10000 \
       --results_base="./data/experiment1/graphs"
```

This will generate 10000 graphs consisting of 4 clusters with sizes 10, 20, 30, 40, respectively. The parameter p for assortative planted partition model (APPM), specifies the probability that two nodes i,j out of the same cluster are connected by an edge. Similarly, the parameter q for APPM, specifies the probability that two nodes i,j out of two different clusters are connected by an edge. The results are written in ./data/experiment1/graphs/M/<timestamp>.pk.

Once we have graph data, we can run the sampling steps. To reproduce the results in [Random Walk Sampling for Big Data over Networks](https://arxiv.org/abs/1704.04799v1), we run the sampling script twice: once for fixed M and varying L, and once for fixed L and varying M:

```
python ./experiment1.py \
       --step=sampling \
       --sampling-method="RandomWalkSampling" \
       --Ms 10 \
       --Ls 10 20 40 80 160 \
       --graphs_file_pattern="./data/experiment1/graphs/*.pk" \
       --results_base="./data/experiment1/samples/L"

python ./experiment1.py \
       --step=sampling \
       --sampling-method="RandomWalkSampling" \
       --Ms 10 20 30 40 50 80 \
       --Ls 10 \
       --graphs_file_pattern="./data/experiment1/graphs/*.pk" \
       --results_base="./data/experiment1/samples/M"
```

Both of the sampling runs generates samples for all the 10000 graphs generated, with sampling budget `M` and random walk length `L` taken as a cartesian product of `Ms` and `Ls`. The results are stored in folders `./data/experiment1/samples/L` and `./data/experiment1/samples/M` for varying L and M, respectively.

Finally, we can run the graph recovery step using the samples and graphs generated in the last steps:

```
python ./experiment1.py \
       --step=recovery \
       --recovery_method="SparseLabelPropagation" \
       --graphs_path="./data/experiment1/graphs" \
       --samples_path="./data/experiment1/samples/M" \
       --results_base="./data/experiment1/recovery/M" \
       --file_pattern="*.pk"

python ./experiment1.py \
       --step=recovery \
       --recovery_method="SparseLabelPropagation" \
       --graphs_path="./data/experiment1/graphs" \
       --samples_path="./data/experiment1/samples/L" \
       --results_base="./data/experiment1/recovery/L" \
       --file_pattern="*.pk"
```

The results for these runs are presented below:

For fixed walk length L = 10 and variable sampling budget M:

| Sampling Budget M  |        10 |        20 |       30  |        40 |        50 |       80  |
| ------------------ | --------- | --------- | --------- | --------- | --------- | --------- |
| Mean NMSE          | 0.2855969 | 0.2064025 | 0.1032648 | 0.06730792 | 0.0480482 | 0.01553402 |
| Std NMSE           | 0.2195126 | 0.1809782 | 0.1175888 | 0.08862639 | 0.06797459 | 0.02729504 |

For fixed sampling budget M = 10 and variable walk length L:


| Walk Length L |        10 |        20 |      40  |        80 |       160 |
| ------------- | --------- | --------- | -------- | --------- | --------- |
| Mean NMSE     | 0.2855898 | 0.285075 | 0.2867064 | 0.2853296 | 0.2859527 |
| Std NMSE      | 0.2190127 | 0.2186967 | 0.2193373 | 0.2193436 | 0.2201135 |
