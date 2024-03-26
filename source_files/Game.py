import Constants as C
import matplotlib.pyplot as plt
from Env import Env

class Game():
    def __init__(self, env, agent):
        self.env = env
        self.agent = agent
        self.score = 0
        self.maxscore = 0
        self.gameOver = False
        self.globalReward = 0
        self.carspeed = C.SPEED
        self.enemyspeed = C.SPEED
        self.counter = C.COUNTER
        
    def play(self, training=False):
        """
        Play the game with the given speeds for the two cars
        """
        while not self.gameOver:
            self.playStep(None, training)
        
    def playStep(self, frame, training=False):
        """
        Play a step of the game: move both cars and check if the game is over
        """        
        action = self.getAction()
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
        self.globalReward += self.getReward(action)
        if C.SAVESCORESNAME != 0:
            self.saveScores()
        if C.PLOTSTEPS and not training:
            plt.clf()  # Clear the current plot
            plt.imshow(self.env.street, cmap='gray', extent=[0, self.env.envWidth, 0, self.env.envHeight])  # Update the plot with the new env data
            plt.title(f"Current score: {self.score}, Max Score: {self.maxscore}")
        self.updateCounter() 

    def getAction(self):
        # if desired, print the environment on the terminal
        if C.PRINTSTEPS:
            print(self.env)
        state = self.env.get_state()
        action = self.agent(*state)
        if C.PRINTSTEPS:
            print("Action: ", action)
        return 0 if abs(action)<0.001 else 1 if action>0 else 2
    
    def getReward(self, action):
        if self.gameOver:
            self.crash()
            reward = -1000
        else:
            # reward in case of no crash is given by 4 terms:
            # 1) how far you are from the enemy car (normalized by the height of the environment): the farther you are, the better the reward
            # 2) how close you are to the center of the environment (only if PACMAN=False): the closer you are, the better the reward
            # 3) if you moved, you get a slightly negative reward (to encourage the agent to move only when necessary and to stand still when waiting for the enemy)
            # 4) if you used the boost, you get a negative reward (to discourage the use of the it and only use it in case of emergency)
            distFromEnemyNormalized = min(*self.env.enemyDistance())/float(C.ENVSIZE[1])
            distFromCenter = abs(self.env.playerPosition-C.ENVSIZE[1]/2)
            rewardForCenter = 0 if C.PACMAN else 2/(1+distFromCenter)
            rewardForMoving = 0 if (action==0) else -1
            #rewardForBoost = -100  if action_conv==3 or action_conv==4 else 0
            reward = distFromEnemyNormalized + rewardForCenter + rewardForMoving #+ rewardForBoost
        return reward

    def updateCounter(self):
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
        f = open(C.SAVESCORES,'a')
        f.write(str(self.score) + ', '+str(self.maxscore) + '\n')
        f.close()
    