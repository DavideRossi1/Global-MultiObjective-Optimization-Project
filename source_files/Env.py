import numpy as np
import Constants as C

class Env:
    def __init__(self, height, width, carHeight, carWidth):
        """
        Initialize the environment by setting the height and width of the environment and the 
        height and width of the cars, which we assume to be all equal. 
        Car position variables refer to the top left corner of the car.
        
        Args:
            height (int): the environment height
            width (int): the environment width
            carHeight (int): the cars height
            carWidth (int): the cars width            
        """
        self.envHeight = height                                
        self.envWidth = width                                 
        self.carHeight = carHeight                            
        self.carWidth = carWidth                             
        self.street = np.zeros((height, width), dtype=int)          # initialize the environment as a matrix of zeros
        self.playerPosition = (self.envWidth - self.carWidth) // 2  # position your car in the center of the last row
        self.renderCar(1)                                      
        self.generateEnemyCar()                              
        
    def renderCar(self,placeOrRemove): 
        """
        Render the car inside the environment.
        
        Args:
            placeOrRemove (bool): 1 to place the car, 0 to remove it
        """
        for i in range(self.carHeight):
            # compute the current line to render
            currentLine = self.envHeight - 1 - i
            for j in range(self.carWidth):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.street[currentLine, (self.playerPosition+j)%self.envWidth] = placeOrRemove
    
    def renderEnemyCar(self,placeOrRemove): 
        """
        Render the enemy car inside the environment.
        
        Args: 
            placeOrRemove (bool): 1 to place the car, 0 to remove it
        """
        # if enemy car is near the end, render only the part of the car that is still inside the environment
        highestPosition = min(self.carHeight, self.envHeight - self.enemy_y_position)
        for i in range(highestPosition): 
            for j in range(self.carWidth):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.street[self.enemy_y_position + i, (self.enemy_x_position + j)%self.envWidth] = placeOrRemove
    
    def generateEnemyCar(self): 
        """
        Initialize the enemy car in a random position of the first row
        """
        # position enemy in the first row...
        self.enemy_y_position = 0
        maxValidPosition = self.envWidth if C.CONTINUOUSENV else self.envWidth - self.carWidth   
        # ... in a random position
        self.enemy_x_position = np.random.randint(maxValidPosition) 
        self.renderEnemyCar(1)
        
    def enemyDistance(self):
        """
        Return the horizontal distance between a side of your car and the opposit side of the enemy car
        
        Returns:
            int, int: left and right enemy distance
        """
        if C.CONTINUOUSENV:
            leftEnemyDistance  = (self.playerPosition - self.enemy_x_position)%self.envWidth - self.carWidth
            rightEnemyDistance = (self.enemy_x_position - self.playerPosition)%self.envWidth - self.carWidth
        else:
            isEnemyLeft = self.enemy_x_position < self.playerPosition
            leftEnemyDistance  = (self.playerPosition - self.enemy_x_position) - self.carWidth if isEnemyLeft else self.envWidth
            rightEnemyDistance = (self.enemy_x_position - self.playerPosition) - self.carWidth if not isEnemyLeft else self.envWidth
        return leftEnemyDistance, rightEnemyDistance
    
    def wallDistance(self):
        """Return the distance from left and right wall

        Returns:
            int, int: left and right enemy distance
        """
        leftWallDistance  = self.envWidth if C.CONTINUOUSENV else self.playerPosition
        rightWallDistance = self.envWidth if C.CONTINUOUSENV else self.envWidth - (self.playerPosition + self.carWidth)
        return leftWallDistance, rightWallDistance

    
    def moveEnemyCar(self, enemyspeed): 
        """
        Move the enemy car along its vertical line, and return the game status
        
        Args:
            enemyspeed: the speed of the enemy car
            
        Returns:
            bool, int: if the game is over (enemy crashed against the player car) and the score increase
        """
        gameover = False
        scoreIncrease = 0
        # remove old enemy
        self.renderEnemyCar(0) 
        # compute the future position of the enemy car
        futurePosition = self.envHeight - (self.enemy_y_position + enemyspeed)
        # if enemy is still entirely behind you after moving...
        if futurePosition >= 2*self.carHeight: 
            # ...simply move it
            self.enemy_y_position += enemyspeed 
            self.renderEnemyCar(1)
        else:   
            # check the horizontal distance between the two cars
            if min(*self.enemyDistance()) < 0:   
            # the two cars are one in front of the other: crash!
                gameover = True
            else:       
                if futurePosition > 0: 
                # enemy car is still partially in the environment after moving: move it
                    self.enemy_y_position += enemyspeed
                    self.renderEnemyCar(1)
                else:  
                    # enemy car exits the environment: increase score and generate a new enemy car
                    scoreIncrease = 1
                    self.generateEnemyCar()       
        return gameover, scoreIncrease
                          
    def moveCar(self, action, carspeed):
        """
        Move your car along the horizontal axis, following the given action, and return the game status
        
        Args:
            action (int): the action to take
            carspeed (int): the speed of the car
        
        Returns:
            bool: if the game is over (car crashed against the wall)
        """
        return self.moveCarContEnv(action, carspeed) if C.CONTINUOUSENV else self.moveCarStdEnv(action, carspeed)      
    
    
    def moveCarStdEnv(self, action, carspeed): 
        """
        Move your car along the horizontal axis, following the given action, and return the game status
        
        Args:
            action (int): the action to take
            carspeed (int): the speed of the car
        
        Returns:
            bool: if the game is over (car crashed against the wall)
        """
        gameover = False
        # for each action:
        # - check if the car is still entirely inside the environment after moving
        # - if inside, remove it from the old position, move it and render it in the new position
        # - else, car crashed with the wall: game is over
        match action:  
            case 0: #stay still
                pass
            case 1: #right   
                if self.playerPosition + self.carWidth + carspeed <= self.envWidth:
                    self.renderCar(0)
                    self.playerPosition += carspeed
                    self.renderCar(1)
                else:
                    gameover=True
            case 2: #left   
                if self.playerPosition - carspeed >= 0:    
                    self.renderCar(0)
                    self.playerPosition -= carspeed
                    self.renderCar(1)   
                else:
                    gameover=True       
            case 3: #right with boost 
                if self.playerPosition + self.carWidth + C.BOOST*carspeed <= self.envWidth:   
                    self.renderCar(0)
                    self.playerPosition += C.BOOST*carspeed
                    self.renderCar(1)
                else:
                    gameover=True 
            case 4: #left with boost 
                if self.playerPosition - C.BOOST*carspeed >= 0:   
                    self.renderCar(0)
                    self.playerPosition -= C.BOOST*carspeed
                    self.renderCar(1)   
                else:
                    gameover=True         
        return gameover    
    
    
    def moveCarContEnv(self, action, carspeed):
        """
        Move your car along the horizontal axis in a continuous space, following the given action, and return the game status
        
        Args:
            action (int): the action to take
            carspeed (int): the speed of the car
        
        Returns:
            False: the game is never over in this case, car can't crash with the wall
        """
        self.renderCar(0)
        # What happens is basically the same as in the movecar function, but the car can exit 
        # the environment from one side and re-enter from the opposite side, hence the position 
        # of the car is computed as the remainder of the division by the width of the environment 
        # and no crash with the wall is possible
        match action:
            case 0: #stay still
                pass
            case 1: #right
                self.playerPosition = (self.playerPosition + carspeed)%self.envWidth     
            case 2: #left
                self.playerPosition = (self.playerPosition - carspeed)%self.envWidth 
            case 3: # right with boost
                self.playerPosition = (self.playerPosition + C.BOOST*C.SPEED)%self.envWidth   
            case 4: # left with boost
                self.playerPosition = (self.playerPosition - C.BOOST*C.SPEED)%self.envWidth       
        self.renderCar(1)
        # game is never over in this case: you can't crash with the wall
        return False
    
    def __str__(self): 
        """
        Print the environment on terminal
        """
        res = ""
        for i in range(self.envHeight):
            for j in range(self.envWidth):
                res += "|X" if self.street[i,j] == 1 else "| "
            res += "|\n"  
        # if you also want the score to be printed at each step, uncomment the following line
        #res.join('Score: ',self.score,'\n')  
        return res
    
    def bin(self, distance):
        """
        Bin the given distance into 4 categories

        Args:
            distance (int): the distance to bin

        Returns:
            int: the converted distance
        """
        return 0 if distance < C.SPEED else \
               1 if distance < 2*C.SPEED else \
               2 if distance < 2*C.BOOST*C.SPEED else \
               3
            
    def sideObstacles(self):
        """
        Return the horizontal distance of the enemy car and the walls, with respect to the car, using integers.
        
        Returns:
            int, int: distance from the closest obstacle on the left and on the right
        """        
        leftEnemyDistance, rightEnemyDistance = self.enemyDistance()
        leftWallDistance, rightWallDistance = self.wallDistance()
        if C.PRINTSTEPS:
            print("left and right wall distances: ", leftWallDistance,rightWallDistance)
            print("left and right enemy distances: ", leftEnemyDistance,rightEnemyDistance) 
        # find the closest obstacle (wall or enemy car) on the left and on the right
        obstacleLeftDistance  = min(leftWallDistance, leftEnemyDistance)
        obstacleRightDistance = min(rightWallDistance, rightEnemyDistance)
        # return the distance of the closest obstacle on the left and on the right
        # Notice that we are in a continuous environment, walls will always be farther than the enemy car 
        # (hence obstacleLeftDistance==leftEnemyDistance and obstacleRightDistance==rightEnemyDistance)
        if not C.USEGA:
            # Bin the distance if using RL, to avoid a too large state space
            obstacleLeftDistance, obstacleRightDistance = self.bin(obstacleLeftDistance), self.bin(obstacleRightDistance)
        return [obstacleLeftDistance, obstacleRightDistance]
               
    def frontObstacles(self):
        """
        Return information about the vertical position of the enemy car with respect to the car, using integers and booleans
        
        Returns:
            bool, int, bool: if the enemy car is in front of you, the vertical distance between the two cars, if the enemy car is on your left or right
        """
        # Enemy is in front of you if the distance between the two cars is less than 0
        enemyInFront = (min(*self.enemyDistance()) < 0)
        # Compute the vertical distance between the two cars
        enemyVerticalDistance = self.envHeight - self.enemy_y_position - 2*self.carHeight                  
        # Boolean value that tells if the enemy car is on the left of the car 
        # (hence, if it is False the enemy is on the right)
        enemyLeftOrRight = (self.enemy_x_position < self.playerPosition)
        if not C.USEGA:
            # Bin the distance if using RL, to avoid a too large state space
            b = 0 if self.carWidth%(C.BOOST*C.SPEED)==0 else 1
            c = 0 if self.carWidth%C.SPEED==0 else 1
            enemyVerticalDistance = 0 if enemyInFront and (enemyVerticalDistance < C.SPEED) else \
                                    1 if enemyInFront and (enemyVerticalDistance < 2*C.SPEED) else \
                                    2 if enemyInFront and (enemyVerticalDistance < self.carWidth//(C.BOOST*C.SPEED)+b) else \
                                    3 if enemyInFront and (enemyVerticalDistance < self.carWidth//C.SPEED+c) else \
                                    4
        if C.PRINTSTEPS:
            print("enemyInFront, enemyVertDist, leftright: ",enemyInFront,enemyVerticalDistance,enemyLeftOrRight)
        return [enemyInFront, enemyVerticalDistance, enemyLeftOrRight]
     
    def getState(self): 
        """
        Return the state of the environment: a quintuple (enemyInFront, enemyVerticalDistance, enemyLeftOrRight, obstacleLeftDistance, obstacleRightDistance)
        
        Returns:
            np array: the state of the environment
        """
        return np.array((*self.frontObstacles(), *self.sideObstacles()), dtype=int)