import numpy as np
import Constants as C

class Env:
    def __init__(self, height, width, car_height, car_width):
        """
        Initialize the environment by setting the height and width of the environment and the 
        height and width of the cars, which we assume to be equally sized.
        Car position variables refer to the top left corner of the car.
        """
        self.envHeight = height                                 # height of the environment
        self.envWidth = width                                   # width of the environment
        self.carHeight = car_height                             # height of the cars
        self.carWidth = car_width                               # width of the cars
        self.street = np.zeros((height, width), dtype=int)      # initialize the environment as a matrix of zeros
        self.playerPosition = (self.envWidth-self.carWidth)//2  # position your car in the center of the last row
        self.renderCar(1)                                       # generate car
        self.generateEnemyCar()                                 # generate enemy car
    
    def renderCar(self,bool): 
        """
        Render the car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        for i in range(self.carHeight):
            # compute the current line to render
            current_line = self.envHeight - 1 - i
            for j in range(self.carWidth):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.street[current_line, (self.playerPosition+j)%self.envWidth] = bool
    
    def renderEnemyCar(self,bool): 
        """
        Render the enemy car inside the environment: bool=1 to place it, bool=0 to remove it
        """
        # if enemy car is near the end, render only the part of the car that is still inside the environment
        highest_position = min(self.carHeight, self.envHeight - self.enemy_y_position)
        for i in range(highest_position): 
            for j in range(self.carWidth):
                # use %self.width to account for the possibility of car to exit the environment from one side and re-enter from the opposite side
                self.street[self.enemy_y_position + i, (self.enemy_x_position + j)%self.envWidth] = bool
    
    def generateEnemyCar(self): 
        """
        Initialize the enemy car in a random position of the first row
        """
        # position enemy in the first row...
        self.enemy_y_position = 0
        interval = self.envWidth if C.PACMAN else self.envWidth - self.carWidth   
        # ... in a random position
        self.enemy_x_position = np.random.randint(interval) 
        self.renderEnemyCar(1)
        
    def enemyDistance(self):
        """
        Return the minimum horizontal distance between a side of your car and a side of the enemy car
        """
        if C.PACMAN:
            leftEnemyDistance  = (self.playerPosition - self.enemy_x_position)%self.envWidth - self.carWidth
            rightEnemyDistance = (self.enemy_x_position - self.playerPosition)%self.envWidth - self.carWidth
        else:
            enemyLeft = self.enemy_x_position < self.playerPosition
            leftEnemyDistance  = (self.playerPosition - self.enemy_x_position) - self.carWidth if enemyLeft else self.envWidth
            rightEnemyDistance = (self.enemy_x_position - self.playerPosition) - self.carWidth if not enemyLeft else self.envWidth
        return leftEnemyDistance, rightEnemyDistance
    
    def wallDistance(self):
        leftWallDistance  = self.envWidth if C.PACMAN else self.playerPosition
        rightWallDistance = self.envWidth if C.PACMAN else self.envWidth - (self.playerPosition + self.carWidth)
        return leftWallDistance, rightWallDistance

    
    def moveEnemyCar(self, enemyspeed): 
        """
        Move the enemy car along its vertical line, and return the game status
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
        """
        return self.moveCarPM(action, carspeed) if C.PACMAN else self.moveCarNoPM(action, carspeed)      
    
    
    def moveCarNoPM(self, action, carspeed): 
        """
        Move your car along the horizontal axis, following the given action, and return the game status
        """
        gameover = False
        # for each action, check if the car didn't crash with the wall, then move the car
        match action:  
            case 0: #stay still
                pass
            case 1: #right   
                # if the car is still entirely inside the environment after moving...
                if self.playerPosition + self.carWidth + carspeed <= self.envWidth:
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.renderCar(0)
                    self.playerPosition += carspeed
                    self.renderCar(1)
                else:
                    # car crashed with the wall: game is over
                    gameover=True
            case 2: #left   
                # if the car is still entirely inside the environment after moving...
                if self.playerPosition - carspeed >= 0:    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.renderCar(0)
                    self.playerPosition -= carspeed
                    self.renderCar(1)   
                else:
                    # car crashed with the wall: game is over
                    gameover=True       
            # case 3: #right with boost 
            #     # if the car is still entirely inside the environment after moving...
            #     if self.car_x_position+self.car_width+C.BOOST*carspeed<=self.width:   
            #         # ...move it: remove it from the old position, move it and render it in the new position
            #         self.render_car(0)
            #         self.car_x_position+=C.BOOST*carspeed
            #         self.render_car(1)
            #     else:
            #         # car crashed with the wall: game is over
            #         gameover=True 
            # case 4: #left with boost 
            #     # if the car is still entirely inside the environment after moving...
            #     if self.car_x_position-C.BOOST*carspeed>=0:   
            #         # ...move it: remove it from the old position, move it and render it in the new position
            #         self.render_car(0)
            #         self.car_x_position-= C.BOOST*carspeed
            #         self.render_car(1)   
            #     else:
            #         # car crashed with the wall: game is over
            #         gameover=True         
        return gameover    
    
    
    def moveCarPM(self, action, carspeed):
        """
        Move your car along the horizontal axis in a continuous space, following 
        the given action and with the given speed, and return the game status
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
            # case 3: # right with boost
            #     self.playerPosition = (self.playerPosition + C.BOOST*C.SPEED)%self.width   
            # case 4: # left with boost
            #     self.playerPosition = (self.playerPosition - C.BOOST*C.SPEED)%self.width       
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
    
    def sideObstacles(self):
        """
        Return the horizontal distance of the enemy car and the walls, with respect to the car, using integers.
        """        
        leftEnemyDistance, rightEnemyDistance = self.enemyDistance()
        leftWallDistance, rightWallDistance = self.wallDistance()
        if C.PRINTSTEPS:
            print("left and right wall distances: ",leftWallDistance,rightWallDistance)
            print("left and right enemy distances: ",leftEnemyDistance,rightEnemyDistance)
        
        # find the closest obstacle (wall or enemy car) on the left and on the right
        obstacleLeftDistance  = min(leftWallDistance, leftEnemyDistance)
        obstacleRightDistance = min(rightWallDistance, rightEnemyDistance)
        # return the distance of the closest obstacle on the left and on the right
        # Notice that if C.PACMAN=True, walls will always be farther than the enemy car 
        # (hence obstacleLeft==leftEnemyDistance and obstacleRight==rightEnemyDistance)
        return [obstacleLeftDistance, obstacleRightDistance]

    
    def frontObstacles(self):
        """
        Return information about the vertical position of the enemy car with respect to the car, using integers and booleans
        """
        # Enemy is in front of you if the distance between the two cars is less than 0
        enemyInFront = (min(*self.enemyDistance()) < 0)
        # Compute the vertical distance between the two cars
        enemyVerticalDistance = self.envHeight - self.enemy_y_position - 2*self.carHeight                  
        # Boolean value that tells if the enemy car is on the left of the car 
        # (hence, if it is False the enemy is on the right)
        enemyLeftOrRight = (self.enemy_x_position < self.playerPosition)
        if C.PRINTSTEPS:
            print("enemyInFront, enemyVertDist, leftright: ",enemyInFront,enemyVerticalDistance,enemyLeftOrRight)
        return [enemyInFront, enemyVerticalDistance, enemyLeftOrRight]
        
    def get_state(self): 
        """
        Return the state of the environment: a quintuple (enemyInFront, enemyVerticalDistance, enemyLeftOrRight, obstacleLeftDistance, obstacleRightDistance)
        """
        return (*self.frontObstacles(), *self.sideObstacles())
