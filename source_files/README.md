# Implementation details
This directory contains the main files needed to learn and run an agent to play the game. 
Two agents are available, and they share the signature for all the main functions (learning, loading and saving the agent), so that they can be called the same way in the main file.
Some details about the implementation of the algorithms are provided in the following sections.

## Genetic Algorithm
The genetic algorithm used to learn the agent is implemented using the `DEAP` library. The entire code about this agent is contained in the [AgentEA file](AgentEA.py). This file contains a set of functions needed to use the DEAP library: `buildPset()`, `buildToolBox()` and `buildStats()`, whose use is explained more deeply inside the code. The main function is `learnAgent()`, which is called by the constructor if no agent is imported. This function is used to learn the agent by calling the `DEAP` function `eaSimple()`, whose pseudo-code is

```python
evaluate(population)
for g in range(ngen):
    population = select(population, len(population))
    offspring = varAnd(population, toolbox, cxpb, mutpb)
    evaluate(offspring)
    population = offspring
```

where `select` is done using a tournament selection, and`varAnd` applies a crossover (for each couple of individuals $x_i, x_{i+1}$ with probability `cxpb`) and a mutation (for each individual $x_i$ with probability `mutpb`), both with replacement (i.e. the offsprings substitute the parents).

## Reinforcement Learning
The reinforcement learning algorithm used to learn the agent is implemented using a self implementation of Temporal Difference algorithm. The entire code about this agent is contained in the [AgentRL file](AgentRL.py). Also in this case, the main function is `learnAgent()`, which has the following pseudo-code:
```python
for episode in range(n_episodes):
    for game in range(n_games):
        playGame()
    if meanscoreEpisode > threshold:
        break
```
where `playGame()` is a function that plays the game until game over and updates the Q-table at each step.

