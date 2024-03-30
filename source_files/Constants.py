
# This file contains all the constants needed to set up the project. Set them as you prefer

# Boolean. Main parameter: decide if to use GA or RL to evolve the agent
USEGA = True


#######################################################
################### GAME PARAMETERS ###################
#######################################################


# Boolean. If True, environment becomes a continuous space, hence you can exit the environment 
# from one side and re-enter from the opposite side:
CONTINUOUSENV=False  

 # Integer. Starting speed of both you and the enemy cars:
SPEED=1          

# Integer. Speed multiplier: when boost is activated, your speed becomes BOOST*SPEED:
BOOST=2       

 # Integer. Maximum score that can be reached, game restarts after it is reached:     
MAXSCORE=1000   

# Integer. Number of points to be scored before increasing the speed of the enemy cars, 
# hence increasing the difficulty. Set it to a high value to maintain the enemy speed constant:
COUNTER=1000000  

# Couple of integers. Height and width of the environment:
ENVSIZE=(10,10)

# Couple of integers. Height and width of the cars. A good choice to have something realistic is 
# ~1/4 of the height and ~1/6 of the width of the environment. Avoid setting them with too big 
# values (larger than ~1/3 of the height and ~1/4 of the width of the environment in the case of 
# no pacman), otherwise it will be too difficult to avoid the enemy cars:
CARSIZE=(2,2)         


#######################################################
################### PLOT PARAMETERS ###################
#######################################################

# Boolean. If True, the environment is printed in the terminal at each step:
PRINTSTEPS=False   

# Boolean. If True, the environment is plotted and animated 
# (the animation won't stop until the user closes the plot):
PLOTSTEPS=True

# Integer. Time in milliseconds between each step in the case PLOTSTEPS=True. 
# Increase it to slow down the animation:  
WAIT=10 

# number of games to be played after the agent has been learned/imported:
NGAMES=200        
   
   
#######################################################
#################### GA PARAMETERS ####################
#######################################################

# Integer. Initial population size
POPSIZE=200

# Integer. Number of generations of EA
NGENERATIONS=5

# Integers. Minimum and maximum size for tree individuals used in EA
MINTREESIZE=2
MAXTREESIZE=6

# Double in [0,1]. Crossover and mutation probability
CXPROBABILITY=0.5
MUTPROBABILITY=0.2

# Integer. Tournament size for tournament selection
TOURNAMENTSIZE=7 


#######################################################
#################### RL PARAMETERS ####################
#######################################################

# Integer. Maximum number of game batches to play before stopping the learning
NBATCHESRL = 100

# Integer. Batch size for learning.
BATCHSIZE = 50

# Integer. If the batch mean score overcomes this threshold, the learning is stopped
SCORETHRESHOLD = 1000

# Agent algorithm to be used for training: SARSA, Qlearning, ExpectedSARSA:
AGENT="SARSA"      

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

# String, or 0. If you want to use a old agent, set with the name of the file containing it. 
# Otherwise, set with 0 to train a new agent:
IMPORTAGENTNAME=0#"policy_SARSA_noboost_noPM.txt"

# String, or 0. If you want to save the agent in a file, in order to use it later, set with the name of the file.
# Otherwise, set with 0:
EXPORTAGENTNAME=0#"testAgent.txt"

# String, or 0. If you want to save the tree image in a file, set with the name of the file in pdf format. 
# Otherwise, set with 0:
EXPORTTREENAME=0#"testTree.pdf"

# String, or 0. If you want to save the scores in a file, set with the name of the file. 
# Otherwise, set with 0:              
SAVESCORESNAME=0#"testScores.txt"                      
          























# routine to set the right path for files
isPacman = "pacman" if CONTINUOUSENV else "no_pacman"
if IMPORTAGENTNAME!=0:
    IMPORTAGENT = "agents/" + isPacman + "/" + IMPORTAGENTNAME
if EXPORTAGENTNAME!=0:
    EXPORTAGENT = "agents/" + isPacman + "/" + EXPORTAGENTNAME
if EXPORTTREENAME!=0:
    EXPORTTREE  = "agents/" + isPacman + "/" + EXPORTTREENAME
if SAVESCORESNAME!=0:
    SAVESCORES  = "scores/" + isPacman + "/" + SAVESCORESNAME
