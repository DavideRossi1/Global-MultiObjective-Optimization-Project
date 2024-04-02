import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Game import Game
from Env import Env
from AgentEA import AgentEA
from AgentRL import AgentRL
import Constants as C

def main():
    """
    Main function of the game: plays the game and plots/renders the updates 
    """
    # build the environment
    env = Env(*C.ENVSIZE, *C.CARSIZE)
    agent = buildAndExtractBestIndividual()
    # if desired, plot the environment and play the game
    if C.PLOTSTEPS:
        game = Game(env, agent) 
        plt.figure(figsize=C.ENVSIZE)
        plt.imshow(game.env.street, cmap='gray')
        _ = FuncAnimation(plt.gcf(), game.playStep, fargs=(), frames=10000000, interval=C.WAIT)
        plt.show()
    # otherwise, just play the game
    else:
        for _ in range(C.NGAMES):
            game = Game(env, agent)
            game.play()

def buildAndExtractBestIndividual():
    """
    Build the agent, train it if desired and save it in a file if desired.

    Returns:
        AgentRL or compiled DEAP tree: the agent to play the game
    """
    print("Building the agent...")
    agentClass = AgentEA if C.USEGA else AgentRL
    agentName = "Genetic Algorithm" if C.USEGA else "Reinforcement Learning"
    if C.IMPORTAGENT:
        print("Agent found, importing...")
        agent = agentClass(C.IMPORTAGENTPATH)
        print("Agent imported")
    else:
        print("No previous agents found, a new agent will be learned using", agentName)
        agent = agentClass()
        print("Agent learned")
    if C.EXPORTTREE and C.USEGA:
        agent.saveTreeImageIn(C.EXPORTTREEPATH)
    if C.EXPORTAGENT:
        agent.saveAgentIn(C.EXPORTAGENTPATH)
    print("Starting the game...")
    return agent.bestIndividualCompiled if C.USEGA else agent
    

# Let's play!
main()