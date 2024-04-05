
""" DOCUMENTATION
This file contains all the constants needed to set up the project. Set them as you prefer.
At the end of the file you'll find some routines to set the right paths for agents and scores
files, according to the parameters set before. Some agents and scores files are already present,
and you can create new ones by setting the right parameters and running the main.py file.
"""

# Boolean. Main parameter: decide if to use GA or RL to evolve the agent
USEGA = True


#######################################################
################### GAME PARAMETERS ###################
#######################################################

# Boolean. If True, environment becomes a continuous space, hence you can exit the environment 
# from one side and re-enter from the opposite side:
CONTINUOUSENV=True  

# Integer. Speed multiplier: when boost is activated, your speed becomes BOOST*SPEED:
BOOST=1       

# Integer. Number of points to be scored before increasing the speed of the enemy cars, 
# hence increasing the difficulty. Set it to a value higher than MAXSCORE to keep the 
# enemy speed constant for the entire game:
COUNTER=100 

# Integer. Maximum score that can be reached, game restarts after it is reached:     
MAXSCORE=1000  
 
# Integer. Starting speed of both you and the enemy cars:
SPEED=1 
         
# Couple of integers. Height and width of the environment:
ENVSIZE=(10,10)

# Couple of integers. Height and width of the cars. A good choice to have something realistic is 
# ~1/4 of the height and ~1/6 of the width of the environment. Avoid setting them with too big 
# values (larger than ~1/3 of the height and ~1/4 of the width of the environment in the case of 
# standard space), otherwise it will be too difficult to avoid the enemy cars:
CARSIZE=(2,2)         



#######################################################
################### PLOT PARAMETERS ###################
#######################################################

# Boolean. If True, the environment is printed in the terminal at each step:
PRINTSTEPS=False   

# Boolean. If True, the environment is plotted and animated 
# (the animation won't stop until the user closes the plot):
PLOTSTEPS=False

# Integer. Time in milliseconds between each step in the case PLOTSTEPS=True. 
# Increase it to slow down the animation:  
WAIT=10

# number of games to be played after the agent has been learned/imported:
NGAMES=1        
   
   
   
#######################################################
#################### EA PARAMETERS ####################
#######################################################

# Integer. Initial population size
POPSIZE=200

# Integer. Number of generations of EA
NGENERATIONS=15

# Integers. Minimum and maximum size for tree individuals used in EA
MINTREESIZE=2
MAXTREESIZE=6

# Double in [0,1]. Crossover and mutation probability
CXPROBABILITY=0.5
MUTPROBABILITY=0.2

# Integer. Tournament size for tournament selection
TOURNAMENTSIZE=7

# Integer. Number of times the EA is repeated to evaluate the learning process
NREPS=10



#######################################################
#################### RL PARAMETERS ####################
#######################################################

# Integer. Maximum number of episodes to play before stopping the learning
NEPISODES = 20

# Integer. Size of a single episode for learning.
EPSIZE = 10

# Integer. If the episode average score overcomes this threshold, the learning is stopped
SCORETHRESHOLD = 1000

# Agent algorithm to be used for training: SARSA, Qlearning, ExpectedSARSA:
AGENT="ExpectedSARSA"      

# Double in [0,1]. Discount factor for temporal difference learning:
GAMMA=1            

# Positive double. Learning rate for temporal difference learning:
LEARNING_RATE=0.01 

# Double in [0,1]. Epsilon used for the epsilon-greedy policy. 
# 0 means no exploration, 1 means no exploitation:
EPSILON=0.5      

# Double in [0,1]. Epsilon decay factor: the epsilon used for the epsilon-greedy policy 
# is multiplied by this factor at each step
EPSDECAY=0.90      



#######################################################
################## PATHS PARAMETERS ###################   
#######################################################

# Note: all paths and names of the files are automatically created according to parameters set before.
 
# Boolean. Decide if to import an already trained agent from a file
IMPORTAGENT=False

# Boolean. Decide if to save the agent in a file, in order to use it later:
EXPORTAGENT=True

# Boolean. Decide if to save a readable tree image in a file:
# Otherwise, set with 0:
EXPORTTREE=True

# Boolean. Decide if to save the scores in a file:   
SAVESCORES=True                    
          










     

# routine to set the right path for files
agent = "AgentGA/" if USEGA else "AgentRL/" 
isContSpace = "ContinuousSpace/" if CONTINUOUSENV else "StandardSpace/"
boost = "boost/" if BOOST>1 else "noBoost/" 
counter = "counter/" if COUNTER<MAXSCORE else "noCounter/"
if USEGA:
    fileName = "pop{}_ngen{}_tsz{}.".format(POPSIZE,NGENERATIONS,TOURNAMENTSIZE)
else:
    fileName = "neps{}_epsz{}_thr{}_{}.".format(NEPISODES,EPSIZE,SCORETHRESHOLD,AGENT)
agentPath = "agents/" + agent + isContSpace + boost + counter + fileName
scorePath = "scores/" + agent + isContSpace + boost + counter + fileName
if IMPORTAGENT:
    IMPORTAGENTPATH = agentPath + "txt"
if EXPORTAGENT:
    EXPORTAGENTPATH = agentPath + "txt"
if EXPORTTREE:
    EXPORTTREEPATH  = agentPath + "pdf"
if SAVESCORES:
    SAVESCORESPATH  = scorePath
