from deap import base, creator, tools, gp, algorithms
import operator
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pygraphviz as pgv
import seaborn as sns

from Env import Env
from Game import Game
import Constants as C


class AgentEA():
    """
    Agent class that uses Evolutionary Algorithms to train and play the game
    
    Args:
        individualPath (string, optional): the path of the file containing the individual to be imported. Defaults to None (build the individual from scratch)
    """
    def __init__(self, individualPath=None):
        self.buildPset()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=self.pset)
        self.buildToolBox()
        self.buildStats()
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

    def buildStats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(key=len)
        self.mstats = tools.MultiStatistics(fitness=stats, size=stats_size)
        self.mstats.register("min", np.min)
        self.mstats.register("avg", np.mean)
        self.mstats.register("max", np.max)
        self.mstats.register("std", np.std)

    def learnAgent(self):
        """
        Learn the agent using a Evolutionary Algorithm (EA) with the parameters specified in the Toolbox and in the Constants file
        """
        random.seed(314)
        pop = self.toolbox.population(n = C.POPSIZE)
        hof = tools.HallOfFame(1)
        # if desired, save the scores in a file
        if C.SAVESCORES:
            self.repeatEA(hof)
            self.plotStats(C.SAVESCORESPATH)
        else:
            algorithms.eaSimple(pop, self.toolbox, C.CXPROBABILITY, C.MUTPROBABILITY, C.NGENERATIONS, self.mstats, halloffame=hof, verbose=True)                
        self.bestIndividual = hof[0]
        self.compileBestIndividual()

    def repeatEA(self, hof):
        """
        Repeat the EA for a set number of times and saves the average statistics in the set file
        """
        # Write a header file to save info about the run
        f=open(C.SAVESCORESPATH,'w')
        comments="# Speed: {}, Boost: {}, ContEnv: {}, Env size: {}, Car size: {}, Counter: {}\n".format(C.SPEED,C.BOOST,C.CONTINUOUSENV,C.ENVSIZE,C.CARSIZE,C.COUNTER)
        f.write(comments)
        f.close()
        scoresList = []
        for i in range(C.NEVALS):
            print("\nEVALUATION", i+1, "OF", C.NEVALS)
            # Generate the population from scratch
            pop = self.toolbox.population(n = C.POPSIZE)
            # Reset the statistics
            self.buildToolBox()
            self.buildStats()
            pop, logbook = algorithms.eaSimple(pop, self.toolbox, C.CXPROBABILITY, C.MUTPROBABILITY, C.NGENERATIONS, self.mstats, halloffame=hof, verbose=True)
            logbook.header = "gen", "nevals", "fitness", "size"
            logbook.chapters["fitness"].header = "min", "avg", "max"
            logbook.chapters["size"].header = "min", "avg", "max"
            scoresList.append(self.convertLogBookToDataframe(logbook))
        # create a new dataframe with the mean values of the scores
        meanScores = sum(scoresList)/C.NEVALS
        # save the mean scores in the specified file
        meanScores.to_csv(C.SAVESCORESPATH, mode='a', header=True, index=False)
        
        
    def convertLogBookToDataframe(self, logbook):
        """Convert the logbook into a Pandas dataframe

        Args:
            logbook (list of dictionaries): the logbook to convert
            
        Returns:
            Pandas Dataframe: the converted dataframe
        """
        cols = ["min", "avg", "max", "std"]
        fitnessCols = ["fitness_"+c for c in cols]
        sizeCols = ["size_"+c for c in cols]
        base = pd.DataFrame(logbook)
        colsToDrop = ["gen", "nevals"]
        fitness = pd.DataFrame(logbook.chapters["fitness"]).drop(columns = colsToDrop).rename(columns=dict(zip(cols, fitnessCols)))
        size    = pd.DataFrame(logbook.chapters["size"]).drop(columns = colsToDrop).rename(columns=dict(zip(cols, sizeCols)))
        return pd.concat([base, fitness, size], axis=1)   
        
        
    def plotStats(self, meanScoresFile):
        """Plot the stats from the given file

        Args:
            meanScoresFile (string): the file where to read the stats
        """
        sns.set_theme()
        data=pd.read_csv(meanScoresFile,header=1)
        clrs = sns.color_palette("husl", 5)
        fig, ax1 = plt.subplots()
        x=data.loc[:,"gen"]
        means = data.loc[:,"fitness_avg"]
        std = data.loc[:,"fitness_std"]
        meansize = data.loc[:,"size_avg"]
        stdsize = data.loc[:,"size_std"]
        with sns.axes_style("darkgrid"):
            line1 = ax1.plot(x,means,'b-', label = "Fitness")
            ax1.fill_between(x, means-std,means+std, alpha=0.5, facecolor='b')
            ax1.set_xlabel("Generation")
            ax1.set_ylabel("Fitness", color="b")
            for tl in ax1.get_yticklabels():
                tl.set_color("b")
            ax2=ax1.twinx()
            line2 = ax2.plot(x, meansize, "r-", label="Size")
            ax2.fill_between(x, meansize-stdsize,meansize+stdsize, alpha=0.5, facecolor='r')
            ax2.set_ylabel("Size", color="r")
            for tl in ax2.get_yticklabels():
                tl.set_color("r")
            lns = line1 + line2
            labs = [l.get_label() for l in lns]
            ax1.legend(lns, labs) 
        plt.show()
        # meanScores = pd.read_csv(meanScoresFile, header=1)
        # print(meanScores)
        # gen = meanScores.loc[:,"gen"]
        # fit_avg = meanScores.loc[:,"fitness_avg"]
        # size_avg = meanScores.loc[:,"fitness_min"]
        # fig, ax1 = plt.subplots()
        # line1 = ax1.plot(gen, fit_avg, "b-", label="Average Fitness")
        # ax1.set_xlabel("Generation")
        # ax1.set_ylabel("Fitness", color="b")
        # for tl in ax1.get_yticklabels():
        #     tl.set_color("b")
        # ax2 = ax1.twinx()
        # line2 = ax2.plot(gen, size_avg, "r-", label="min fitness")
        # ax2.set_ylabel("Size", color="r")
        # for tl in ax2.get_yticklabels():
        #     tl.set_color("r")
        # lns = line1 + line2
        # labs = [l.get_label() for l in lns]
        # ax1.legend(lns, labs)
        # plt.show()
    
    
    
    
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


