from deap import base, creator, tools, gp, algorithms
import operator
import random
import numpy as np
from Env import Env
from Game import Game
import Constants as C
import pygraphviz as pgv

class AgentEA():
    """
    Agent class that uses Evolutionary Algorithms to train and play the game
    
    Args:
        individualPath (string, optional): the path of the file containing the individual to be imported. Defaults to None (build the individual from scratch)
    """
    def __init__(self, individualPath=None):
        
        self.buildPset()
        self.buildToolBox()
        if individualPath is None:
            self.bestIndividual = None
            self.bestIndividualCompiled = None
            self.learnAgent()   
        else:
            self.loadAgentFrom(individualPath)
        
    def compileBestIndividual(self):
        """
        Compile the best individual to obtain a function that can be used to play the game
        """
        self.bestIndividualCompiled = self.toolbox.compile(self.bestIndividual, pset = self.pset)
    
    def buildPset(self):
        """
        Build the primitive set for the genetic programming. A state is a tuple of 5 elements:
        - if the enemy car is in front of you (bool)
        - the vertical distance between you and the enemy car (float)
        - if the enemy car is on the left of you (bool)
        - the distance between you and the closest obstacle on the left (float)
        - the distance between you and the closest obstacle on the right (float)
        """
        self.pset = gp.PrimitiveSetTyped("MAIN", [bool, float, bool, float, float], float, "IN")

        def protectedInv(x):
            return 1.0/x if x != 0 else 1  
        def if_then_else(input, output1, output2):
            return output1 if input else output2

        self.pset.addPrimitive(operator.add, [float, float], float)
        self.pset.addPrimitive(operator.sub, [float, float], float)
        self.pset.addPrimitive(operator.mul, [float, float], float)
        self.pset.addPrimitive(protectedInv, [float], float)

        self.pset.addPrimitive(operator.and_, [bool, bool], bool)
        self.pset.addPrimitive(operator.or_, [bool, bool], bool)
        self.pset.addPrimitive(operator.not_, [bool], bool)

        self.pset.addPrimitive(if_then_else, [bool, float, float], float)
        self.pset.addPrimitive(operator.lt, [float, float], bool) # <
        self.pset.addPrimitive(operator.eq, [float, float], bool) # ==

        #pset.addTerminal(False, bool)
        #pset.addTerminal(True, bool)
        #pset.addEphemeralConstant("rand101", partial(random.uniform,0,100),float)

    def buildToolBox(self):  
        """"
        Build the toolbox for the genetic algorithm
        """     
        self.toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=self.pset)

        def fitness(individual):
            """
            Compute the fitness of the individual by let it play the game
            
            Args:
                individual (DEAP tree): the individual to evaluate
                
            Returns:
                float: the fitness of the individual, given as the global reward obtained by it
            """
            individualCompiled = self.toolbox.compile(individual)
            env = Env(*C.ENVSIZE, *C.CARSIZE)
            game = Game(env, individualCompiled, training=True)
            game.play()
            return game.globalReward,
        
        self.toolbox.register("evaluate", fitness)
        self.toolbox.register("expr", gp.genHalfAndHalf, pset=self.pset, min_=C.MINTREESIZE, max_=C.MAXTREESIZE)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("compile", gp.compile, pset=self.pset)
        self.toolbox.register("select", tools.selTournament, tournsize=C.TOURNAMENTSIZE)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)

    def learnAgent(self):
        """
        Learn the agent using a Evolutionary Algorithm (EA) with the parameters specified in the Toolbox and in the Constants file
        """
        random.seed(314)
        pop = self.toolbox.population(n = C.POPSIZE)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
        # if desired, save the scores in a file
        if C.SAVESCORESNAME!=0:
            f=open(C.SAVESCORES,'w')
            comments="# Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {}, Counter: {}\n".format(C.SPEED,C.BOOST,C.CONTINUOUSENV,C.ENVSIZE,C.CARSIZE,C.COUNTER)
            f.write(comments)
            f.close()
        algorithms.eaSimple(pop, self.toolbox, C.CXPROBABILITY, C.MUTPROBABILITY, C.NGENERATIONS, stats, halloffame=hof)
        self.bestIndividual = hof[0]
        self.compileBestIndividual()
  
    def saveTreeImageIn(self,file):
        """
        Save a human readable tree image in the specified file

        Args:
            file (string): the file where to save the tree image, in pdf format
        """
        nodes, edges, labels = gp.graph(self.bestIndividual)
        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")
        for i in nodes:
            n = g.get_node(i)
            n.attr["label"] = labels[i]
        g.draw(file) 
        
    def saveAgentIn(self,file):
        """
        Save the best individual in the specified file

        Args:
            file (string): the file where to save the best individual
        """
        f = open(file, "w")
        f.write(str(self.bestIndividual))
        f.close()

    def loadAgentFrom(self,file):
        """
        Load the individual from the specified file

        Args:
            file (string): the file where to load the individual from
        """
        f = open(file, "r")
        indStr = f.read()
        f.close()
        self.bestIndividual = gp.PrimitiveTree.from_string(indStr, pset=self.pset) 
        self.compileBestIndividual() 
