
# This file contains all the constants needed to set up the project. Set them as you prefer


 # Integer. Starting speed of both you and the enemy cars:
SPEED=1          

# Integer. Speed multiplier: when boost is activated, your speed becomes BOOST*SPEED:
BOOST=1       

 # Integer. Maximum score that can be reached, game restarts after it is reached:     
MAXSCORE=10000    

# Integer. Number of points to be scored before increasing the speed of the enemy cars, 
# hence increasing the difficulty. Set it to a high value to maintain the enemy speed constant:
COUNTER=10000000   

# Couple of integers. Height and width of the environment:
ENVSIZE=(10,10)

# Couple of integers. Height and width of the cars. A good choice to have something realistic is 
# ~1/4 of the height and ~1/6 of the width of the environment. Avoid setting them with too big 
# values (larger than ~1/3 of the height and ~1/4 of the width of the environment in the case of 
# no pacman), otherwise it will be too difficult to avoid the enemy cars:
CARSIZE=(2,2)    

# Boolean. If True, environment becomes a continuous space, hence you can exit the environment 
# from one side and re-enter from the opposite side:
PACMAN=True       

# String, or 0. If you want to use a old policy, set with the name of the file containing the policy. 
# Otherwise, set with 0 to train a new policy:
IMPORTAGENTNAME=0#"testAgent.txt"

# String, or 0. If you want to save the learned policy in a file, set with the name of the file. 
# Otherwise, set with 0:
EXPORTTREENAME=0#"testTree.pdf"

EXPORTAGENTNAME=0#"testAgent.txt"

# String, or 0. If you want to save the scores in a file, set with the name of the file. 
# Otherwise, set with 0:              
SAVESCORESNAME=0#"testScores.txt"               

# Boolean. If True, the environment is printed in the terminal at each step:
PRINTSTEPS=False   

# Boolean. If True, the environment is plotted and animated 
# (the animation won't stop until the user closes the plot):
PLOTSTEPS=True

# Integer. Time in milliseconds between each step in the case PLOTSTEPS=True. 
# Increase it to slow down the animation:  
WAIT=1                  
          









# ------------------------------ DO NOT CHANGE ANYTHING BELOW THIS LINE -------------------------------------

NGAMES=200            # number of games to be played (used for training purposes, not for plotting)
NSTEPS=10000000       # number of steps to be played (used for training purposes, not for plotting)

# routine to set the right path for files
isPacman = "pacman" if PACMAN else "no_pacman"
if IMPORTAGENTNAME!=0:
    IMPORTAGENT = isPacman+"/"+IMPORTAGENTNAME
if EXPORTAGENTNAME!=0:
    EXPORTAGENT = isPacman+"/"+EXPORTAGENTNAME
if EXPORTTREENAME!=0:
    EXPORTTREE = isPacman+"/"+EXPORTTREENAME
if SAVESCORESNAME!=0:
    SAVESCORES = "scores/"+isPacman+"/"+SAVESCORESNAME
