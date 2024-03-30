import numpy as np
import Constants as C
from Env import Env
from Game import Game

class AgentRL():
    """
    Agent class that uses the Temporal Difference Control model to train and play the game
    """
    def __init__(self,individualPath=None):
        """
        Initialize the agent by training it or importing it from the given path, and set the parameters for the epsilon-greedy policy.
        """
        assert C.AGENT in ['SARSA','Qlearning','ExpectedSARSA'], "Algorithm not recognized"
        self.gamma = C.GAMMA                 # discount factor
        self.spaceSize = (2,5,2,4,4)         # size of the states space
        self.actionSize = 5                  # number of possible actions
        self.learningRate = C.LEARNING_RATE  # learning rate
        self.algorithm = C.AGENT             # algorithm to be used: SARSA, Qlearning, ExpectedSARSA
        self.eps = C.EPSILON  
        # if no policy is imported, initialize Qvalues to 0
        if individualPath is None:
            self.Qvalues = np.zeros( (*self.spaceSize, self.actionSize) )
            self.learnAgent()
        # otherwise, import the policy from a txt file
        else:
            self.loadAgentFrom(individualPath)
        
    def updateQtable(self, state, action, reward, new_state, new_action, gameover):
        """
        Update the policy for the current state and action, using the TDControl algorithm
        
         Args:
            state (array): the current state
            action (int): the current action taken
            reward (float): the reward obtained by applying the action
            new_state (array): the state obtained after applying the action
            new_action (int): the action to be taken in the new state
            gameover (bool): True if the game is over, False otherwise
        """
        if gameover:
            deltaQ = reward - self.Qvalues[(*state, action)]
        else: 
            match self.algorithm:
                case 'SARSA':         # delta=R+gamma*Q(S',A')-Q(S,A)
                    deltaQ = reward + self.gamma*self.Qvalues[(*new_state, new_action)] - self.Qvalues[(*state, action)]
                case 'Qlearning':     # delta=R+gamma*max_a(Q(S',a))-Q(S,A)
                    deltaQ = reward + self.gamma*np.max(self.Qvalues[(*new_state,)]) - self.Qvalues[(*state, action)]
                case 'ExpectedSARSA': # delta=R+gamma*sum_a(pi(a|S')*Q(S',a))-Q(S,A)
                    deltaQ = reward + self.gamma*np.dot(self.Qvalues[(*new_state,)], self.policy(new_state)) - self.Qvalues[(*state, action)]
        # update the policy with TD(0)
        self.Qvalues[(*state, action)] += self.learningRate * deltaQ
        
    def policy(self,state): 
        """
        Return the policy for the given state
        
        Args:
            state (array): the current state
        """
        # start with a uniform probability of choosing each action
        policy = np.ones(self.actionSize)*self.eps/self.actionSize
        # select the action(s) with the highest Qvalue for the given state
        best_value = np.max(self.Qvalues[(*state,)])
        best_actions = (self.Qvalues[(*state,)] == best_value)
        # update the policy
        policy += best_actions * (1-self.eps) / np.sum(best_actions)
        return policy
    
    def learnAgent(self):
        """
        Learn the agent using the TDControl model
        """
        if C.SAVESCORESNAME!=0:
            f=open(C.SAVESCORES,'w')
            comments="# Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {}, Counter: {}\n".format(C.SPEED,C.BOOST,C.CONTINUOUSENV,C.ENVSIZE,C.CARSIZE,C.COUNTER)
            f.write(comments)
            f.close()
        for i in range(C.NBATCHESRL):
            totalScore = 0
            for _ in range(C.BATCHSIZE):
                env = Env(*C.ENVSIZE, *C.CARSIZE)
                game = Game(env, self, training=True)
                game.play()
                totalScore += game.maxscore
            meanScoreBatch = totalScore/C.BATCHSIZE
            print("Mean score for batch",i,":",meanScoreBatch)
            if meanScoreBatch >= C.SCORETHRESHOLD:
                break
                 
    def __call__(self, *state):
        """
        Return the action to be taken for the given state
        
        Args:
            state (array): the current state (given as a tuple of elements)
        """
        if np.random.rand() < self.eps: 
            # random action, with uniform probability, with probability eps
            prob_actions = np.ones(self.actionSize) / self.actionSize   
        else:
            # choose the best action, with probability 1-eps
            best_value = np.max(self.Qvalues[(*state,)]) 
            best_actions = (self.Qvalues[ (*state,) ] == best_value) # in case there is more than one best action...
            prob_actions = best_actions / np.sum(best_actions)
        # reduce the epsilon for the epsilon-greedy policy, to make the agent more greedy at each step
        self.eps*=C.EPSDECAY
        return np.random.choice(self.actionSize, p=prob_actions)  
        
    def saveAgentIn(self, file): 
        """
        Save the learned policy in a txt file
        
        Args:
            file (string): the name of the file where to save the policy
        """
        # A header is added to the file, containing the parameters used for training
        comments="Algorithm: {}, Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {}, Counter: {}, Gamma: {}, LearnRate: {}, Eps: {}, Epsdecay: {}".format(C.AGENT,C.SPEED,C.BOOST,C.CONTINUOUSENV,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.GAMMA,C.LEARNING_RATE,C.EPSILON,C.EPSDECAY)
        onedimension_Qvalues=np.reshape(self.Qvalues, np.prod(self.spaceSize)*self.actionSize)
        np.savetxt(file,onedimension_Qvalues,header=comments)
    
    def loadAgentFrom(self, file):
        """
        Load the policy from a txt file

        Args:
            file (string): the name of the file where the policy is saved
        """
        onedimension_Qvalues = np.loadtxt(file)
        self.Qvalues = np.reshape(onedimension_Qvalues, (*self.spaceSize, self.actionSize))
            
