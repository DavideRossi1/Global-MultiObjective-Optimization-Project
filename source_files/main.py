from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

from Game import Game
from Env import Env
from Agent import Agent
import Constants as C

def main():
    """
    Main function of the game: plays the game and plots/renders the updates 
    """
    # build the environment
    env = Env(*C.ENVSIZE, *C.CARSIZE)
    agent = buildAndExtractBestIndividual()
    game = Game(env, agent) 
    # if desired, plot the environment and play the game
    if C.PLOTSTEPS:
        plt.figure(figsize=C.ENVSIZE)
        plt.imshow(game.env.street, cmap='gray')
        _ = FuncAnimation(plt.gcf(), game.playStep, fargs=(), frames=C.NSTEPS, interval=C.WAIT)
        plt.show()
    # otherwise, just play the game
    else:
        for _ in range(C.NGAMES):
            game.play()


def buildAndExtractBestIndividual():
    if C.IMPORTAGENTNAME!=0:
        agent = Agent(individualPath = C.IMPORTAGENT)
    else:
        agent = Agent()
    if C.EXPORTTREENAME != 0:
        agent.saveTreeImageIn(C.EXPORTTREE)
    if C.EXPORTAGENTNAME != 0:
        agent.saveIndividualIn(C.EXPORTAGENT)
    return agent.bestIndividualCompiled

# Let's play!
main()