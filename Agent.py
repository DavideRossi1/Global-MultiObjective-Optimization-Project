from deap import base, creator, tools, gp, algorithms
import operator
import random
import numpy as np
from Env import Env
from Game import Game
import Constants as C
import pygraphviz as pgv

class Agent:
    def __init__(self, individualPath=None):
        self.buildPset()
        self.buildToolBox()
        if individualPath is None:
            self.bestIndividual = None
            self.bestIndividualCompiled = None
            self.learnAgent()   
        else:
            self.bestIndividual = self.loadIndividualFromFile(individualPath)
            self.compileBestIndividual() 
        
    def compileBestIndividual(self):
        self.bestIndividualCompiled = self.toolbox.compile(self.bestIndividual, pset = self.pset)
    
    def buildPset(self):
        self.pset = gp.PrimitiveSetTyped("MAIN", [float, float, bool, float, bool], float, "IN")

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
        self.toolbox = base.Toolbox()

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=self.pset)

        def fitness(individual):
            individualCompiled = self.toolbox.compile(individual)
            env = Env(*C.ENVSIZE, *C.CARSIZE)
            game = Game(env, individualCompiled)
            game.play(training=True)
            return game.globalReward,
        
        self.toolbox.register("evaluate", fitness)
        self.toolbox.register("expr", gp.genHalfAndHalf, pset=self.pset, min_=2, max_=6)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("compile", gp.compile, pset=self.pset)
        self.toolbox.register("select", tools.selTournament, tournsize=7)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)

    def learnAgent(self):
        random.seed(318)
        pop = self.toolbox.population(n=200)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("std", np.std)
        stats.register("min", np.min)
        stats.register("max", np.max)
            # if desired, save the scores in a file
        if C.SAVESCORESNAME!=0:
            f=open(C.SAVESCORES,'a')
            comments="#Algorithm: {}, Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {},\n#Counter: {}, Nsteps: {}, Gamma: {}, LearnRate: {}, Eps: {}, Epsdecay: {}\n".format(C.AGENT,C.SPEED,C.BOOST,C.PACMAN,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.NSTEPS,C.GAMMA,C.LEARNING_RATE,C.EPSILON,C.EPSDECAY)
            f.write(comments)
            f.close()
        algorithms.eaSimple(pop, self.toolbox, 0.5, 0.2, 10, stats, halloffame=hof)
        self.bestIndividual = hof[0]
        self.compileBestIndividual()
        
    def saveReadableTreeInFile(self,file):
        nodes, edges, labels = gp.graph(self.bestIndividual)
        g = pgv.AGraph()
        g.add_nodes_from(nodes)
        g.add_edges_from(edges)
        g.layout(prog="dot")
        for i in nodes:
            n = g.get_node(i)
            n.attr["label"] = labels[i]
        g.draw(file) 
        
    def saveIndividualInFile(self,file):
        f = open(file, "w")
        f.write(str(self.bestIndividual))
        f.close()

    def loadIndividualFromFile(self,file):
        f = open(file, "r")
        indStr = f.read()
        f.close()
        self.bestIndividual = gp.PrimitiveTree.from_string(indStr, pset=self.pset)            