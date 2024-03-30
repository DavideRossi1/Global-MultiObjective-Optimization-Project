import Constants as C
import matplotlib.pyplot as plt
from Env import Env

class Game():
    def __init__(self, env, agent, training=False):
        """
        Initialize the game with a given environment and agent to play the steps. If training=True, no plots/prints will be rendered

        Args:
            env (Env): the environment where to play the game
            agent (AgentRL or DEAP compiled tree): the agent which will play the game
            training (bool, optional): Decide if the game is created to train the agent or to play. Defaults to False (play the game)
        """
        self.env = env
        self.agent = agent
        self.training = training
        self.score = 0
        self.maxscore = 0
        self.gameOver = False
        self.globalReward = 0
        self.carspeed = C.SPEED
        self.enemyspeed = C.SPEED
        self.counter = C.COUNTER
        
    def play(self):
        """
        Play the game
        """
        while not self.gameOver:
            self.playStep(None)
        
    def playStep(self, frame):
        """
        Play a step of the game: extract the state, compute and apply a corresponding action and update the agent
        
        Args:
            frame (pyplot frame): the frame to be updated in the animation (if PLOTSTEPS=True)
        """        
        if C.PRINTSTEPS and (not self.training):
            print(self.env)
        state = self.env.getState()
        action = self.getAction(state) 
        if C.PRINTSTEPS and (not self.training):
            print("Action: ", action)
        reward = self.applyAction(action) 
        self.globalReward += reward
        if C.SAVESCORESNAME != 0:
            self.saveScores()
        if C.PLOTSTEPS and (not self.training):
            plt.clf()  # Clear the current plot
            plt.imshow(self.env.street, cmap='gray', extent=[0, self.env.envWidth, 0, self.env.envHeight])  # Update the plot with the new env data
            plt.title(f"Current score: {self.score}, Max Score: {self.maxscore}")
        if not C.USEGA and self.training:
            newState = self.env.getState()
            newAction = self.getAction(newState)
            self.agent.updateQtable(state, action, reward, newState, newAction, self.gameOver)
        self.updateCounter()
        
    def getAction(self, state):
        """
        Return the action to be taken for the given state
        
         Args:
            state (array): the current state

        Returns:
            int: the action to take in the current state
        """
        action = self.agent(*state)
        action_conv = 0 if abs(action) < 0.001 else 1 if action > 0 else 2
        return action_conv if C.USEGA else action

    def applyAction(self, action):
        """
        Apply the given action: move both cars, check if the game is over and return the reward

        Args:
            action (int): the action to apply

        Returns:
            float: the reward for the given action
        """
        # move your car and check if it crashed with the wall
        gameover_wall = self.env.moveCar(action, self.carspeed)
         # move enemy car and check if it crashed with your car
        gameover_car, scoreIncrease = self.env.moveEnemyCar(self.enemyspeed) 
        self.score += scoreIncrease    
        # game is over if your car crashed with the wall or with the enemy car
        self.gameOver = gameover_wall or gameover_car      
        # if you reached the maximum score, you won the game: environment is reset
        if self.score >= C.MAXSCORE:
            #print('GAME WON, score: ',self.score)
            self.crash()
            self.gameOver = True
        return self.getReward(action)
        
    def getReward(self, action):
        """
        Compute the reward for the current step

        Args:
            action (int): the action taken

        Returns:
            float: the reward
        """
        if self.gameOver:
            self.crash()
            reward = -1000
        else:
            # reward in case of no crash is given by 4 terms:
            # 1) how far you are from the enemy car (normalized by the height of the environment): the farther you are, the better the reward
            # 2) how close you are to the center of the environment (only if PACMAN=False): the closer you are, the better the reward
            # 3) if you moved, you get a slightly negative reward (to encourage the agent to move only when necessary and to stand still when waiting for the enemy)
            # 4) if you used the boost, you get a negative reward (to discourage the use of the it and only use it in case of emergency)
            rewardForEnemy = min(*self.env.enemyDistance())/float(C.ENVSIZE[1])
            distFromCenter = abs(self.env.playerPosition-C.ENVSIZE[1]/2)
            rewardForCenter = 0 if C.CONTINUOUSENV else 2/(1+distFromCenter)
            rewardForMoving = 0 if (action==0) else -1
            rewardForBoost = -100  if action==3 or action==4 else 0
            reward = rewardForEnemy + rewardForCenter + rewardForMoving + rewardForBoost
        return reward

    def updateCounter(self):
        """
        Update the counter and increase enemy speed if needed
        """
        if self.score == self.counter: 
            self.enemyspeed += 1  # increase the speed 
            self.counter += C.COUNTER # set the next score to be reached to increase the speed
        if self.gameOver:
            self.enemyspeed = C.SPEED # reset the speed 
            self.counter = C.COUNTER 
    
    def crash(self):  
        """
        Save results and reset environment after a crash
        """ 
        # update the max score
        if self.score > self.maxscore: 
            self.maxscore = self.score
            #print('New max score: ',self.maxscore)     
        # save the new score in the specified file
        if C.SAVESCORESNAME != 0:
            self.saveScores()
        # reset the environment
        self.env = Env(*C.ENVSIZE, *C.CARSIZE)
        self.score = 0
        
    def saveScores(self):
        """
        Save the scores in a file
        """
        f = open(C.SAVESCORES,'a')
        f.write(str(self.score) + ', '+str(self.maxscore) + '\n')
        f.close()
    