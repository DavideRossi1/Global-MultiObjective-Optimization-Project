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
        # if desired, print the environment on the terminal
        if C.PRINTSTEPS:
            print(self.env)
        state = self.env.get_state()
        action = self.agent(*state)
        action_conv = 0 if abs(action)<0.001 else 1 if action>0 else 2
        # move your car and check if it crashed with the wall
        gameover_wall = self.env.moveCar(action_conv)
         # move enemy car and check if it crashed with your car
        gameover_car, scoreIncrease = self.env.moveEnemyCar() 
        self.score += scoreIncrease    
        # game is over if your car crashed with the wall or with the enemy car
        self.gameOver = gameover_wall or gameover_car      
        if self.gameOver:
            self.crash()
            reward = -1000
        else:
            left, right = self.env.carDistance()
            # reward in case of no crash is given by 4 terms:
            # 1) how far you are from the enemy car (normalized by the height of the environment): the farther you are, the better the reward
            # 2) how close you are to the center of the environment (only if PACMAN=False): the closer you are, the better the reward
            # 3) if you used the boost, you get a negative reward (to discourage the use of the it and only use it in case of emergency)
            # 4) if you moved, you get a slightly negative reward (to encourage the agent to move only when necessary and to stand still when waiting for the enemy)
            reward = min(left,right)/float(C.ENVSIZE[1]) + (2/(1+float(abs(self.env.playerPosition-C.ENVSIZE[1]/2)))) + (0 if (action==0) else -1) # CHANGED
        # if you reached the maximum score, you won the game: environment is reset
        if self.score > C.MAXSCORE:
            #print('GAME WON, score: ',self.score)
            self.crash()
            self.gameOver = True
        self.globalReward += reward
        if C.SAVESCORESNAME != 0:
            f = open(C.SAVESCORES,'a')
            f.write(str(self.score) + ', '+str(self.maxscore) + '\n')
            f.close()
        if C.PLOTSTEPS and not training:
            plt.clf()  # Clear the current plot
            plt.imshow(self.env.street, cmap='gray', extent=[0, self.env.envWidth, 0, self.env.envHeight])  # Update the plot with the new env data
            plt.title(f"Current score: {self.score}, Max Score: {self.maxscore}")
            
    
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
            f = open(C.SAVESCORES,'a')
            f.write(str(self.score) + ', '+str(self.maxscore) + '\n')
            f.close()     
        # reset the environment
        self.env = Env(*C.ENVSIZE, *C.CARSIZE)
        self.score = 0
    