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
        interval = self.envWidth - self.carWidth  # self.width if C.PACMAN else 
        # ... in a random position
        self.enemy_x_position = np.random.randint(interval) 
        self.renderEnemyCar(1)
        
    def carDistance(self):
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

    
    def moveEnemyCar(self): 
        """
        Move the enemy car along its vertical line, and return the game status
        """
        gameover = False
        scoreIncrease = 0
        # remove old enemy
        self.renderEnemyCar(0) 
        # if enemy is still entirely behind you after moving...
        if self.enemy_y_position + self.carHeight + C.SPEED <= self.envHeight - self.carHeight: 
            # ...simply move it
            self.enemy_y_position += C.SPEED 
            self.renderEnemyCar(1)
        else:   
            # check the horizontal distance between the two cars
            leftCarDistance, rightCarDistance = self.carDistance()  
            distance = min(leftCarDistance,rightCarDistance)
            if distance < 0:   
            # the two cars are one in front of the other: crash!
                gameover = True
            else:       
                if self.enemy_y_position + C.SPEED <= self.envHeight-1: 
                # enemy car is still partially in the environment after moving: move it
                    self.enemy_y_position += C.SPEED
                    self.renderEnemyCar(1)
                else:  
                    # enemy car exits the environment: increase score and generate a new enemy car
                    scoreIncrease = 1
                    self.generateEnemyCar()       
        return gameover, scoreIncrease
                          
    
    def moveCar(self, action): 
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
                if self.playerPosition + self.carWidth + C.SPEED <= self.envWidth:
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.renderCar(0)
                    self.playerPosition += C.SPEED
                    self.renderCar(1)
                else:
                    # car crashed with the wall: game is over
                    gameover=True
            case 2: #left   
                # if the car is still entirely inside the environment after moving...
                if self.playerPosition - C.SPEED >= 0:    
                    # ...move it: remove it from the old position, move it and render it in the new position
                    self.renderCar(0)
                    self.playerPosition -= C.SPEED
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
    
        
   
     
    def __str__(self): 
        """
        Print the environment on terminal
        """
        for i in range(self.envHeight):
            for j in range(self.envWidth):
                print('|X' if self.street[i,j] == 1 else '| ', end='')
            print('|\n')  
        print("\n")
        # if you also want the score to be printed at each step, uncomment the following line
        #print('Score: ',self.score,'\n')  
        
    def binDistance(self,distance):
        """
        Return the binning of the given distance
        """
        return 0 if distance < C.SPEED           else  \
               1 if distance < 2*C.SPEED         else  \
               2 if distance < 2*C.BOOST*C.SPEED else  \
               3  
    
    def sidePositionBinning(self):
        """
        Return the horizontal distance of the enemy car and the walls, with respect to the car, using integers.
        """        
        # cars are at the same height, they could crash from now on
        enemyNear = (self.envHeight - self.enemy_y_position < 2*self.carHeight) 
        # use binning to get different positions of the car with respect to walls and enemy car:
            # 0: wall or enemy car immediately on the left/right, meaning that if you move left/right you lose
            # 1: wall or enemy car 2 steps on the left/right, meaning that if you move left/right 2 times you lose
            # 2: wall or enemy car 2 boosted steps on the left/right, meaning that if you move left/right using boost 2 times you lose
            # 3: wall or enemy car farther than 2 boosted steps on the left/right
        # Notice that to compute the distance from walls we don't use modules, since we are 
        # not interested in walls position in the case of continuous space (PACMAN=True)
        leftWallDistance  = self.playerPosition
        rightWallDistance = self.envWidth - (self.playerPosition + self.carWidth)
        leftWallBinnDistance  = self.binDistance(leftWallDistance)
        rightWallBinnDistance = self.binDistance(rightWallDistance)
        # compute the horizontal distance between the two cars (using modules to consider the case of continuous space),
        # meaning the distance between the closest side of the two cars
        leftEnemyDistance, rightEnemyDistance = self.carDistance()
        # compute the distance between the two cars (using modules to consider the case of continuous space),
        # in the case in which they are at the same height, meaning that they could crash from now on
        leftEnemyBinnDistance  = self.binDistance(leftEnemyDistance)  if enemyNear else 3
        rightEnemyBinnDistance = self.binDistance(rightEnemyDistance) if enemyNear else 3
        
        #print("left and right wall distances: ",leftWallDistance,rightWallDistance)
        #print("left and right enemy distances: ",leftEnemyDistance,rightEnemyDistance)
        # find the closest obstacle (wall or enemy car) on the left and on the right
        obstacle_left  = min(leftWallBinnDistance, leftEnemyBinnDistance)
        obstacle_right = min(rightWallBinnDistance, rightEnemyBinnDistance)
        # return the distance of the closest obstacle on the left and on the right
        pos= [leftEnemyBinnDistance, rightEnemyBinnDistance] if C.PACMAN else [obstacle_left, obstacle_right]
        return pos  
    
    def frontPositionBinning(self):
        """
        Return information about the vertical position of the enemy car with respect to the car, using integers and booleans
        """
        # Compute the horizontal distance between the two cars (using modules to consider the case of continuous space),
        # meaning the distance between the closest side of the two cars
        left,right = self.carDistance()
    
        # Enemy is in front of you if the distance between the two cars is less than 0
        enemyInFront = (min(left,right) < 0)
        # Compute the vertical distance between the two cars
        car_vertical_distance = self.envHeight - self.enemy_y_position - 2*self.carHeight
        # define a constant needed to normalize the results
        b=0 if self.carWidth%(C.BOOST*C.SPEED)==0 else 1
        c=0 if self.carWidth%C.SPEED==0 else 1
        #min_num_steps=env.car_width//(C.BOOST*C.SPEED)+b
        #min_num_steps2=env.car_width//C.SPEED+c
        # In this case I decided to use a different binning:
        # 0: enemy car in front of the car, crash in the next step is nothing changes
        # 1: enemy car in front of the car, crash in 2 steps from now if nothing changes
        # 2: enemy car in front of the car, in the worst case too close to escape even using boost 
        # 3: enemy car in front of the car, in the worst case too close to escape without using boost
        # 4: enemy car not in front of the car or very far away
        pol_dist= 0 if (enemyInFront and (car_vertical_distance < C.SPEED)) else \
                  1 if (enemyInFront and (car_vertical_distance<2*C.SPEED)) else \
                  2 if (enemyInFront and (car_vertical_distance<self.carWidth//(C.BOOST*C.SPEED)+b)) else \
                  3 if (enemyInFront and (car_vertical_distance<self.carWidth//C.SPEED+c)) else \
                  4
                  #new:    
                  #2 if (enemy_in_front and (min_num_steps2<=car_vertical_distance)) else \
                  #3 if (enemy_in_front and (min_num_steps<=car_vertical_distance)) else \
                  #4
                  
                  #middle:
                  #2 if (enemy_in_front and (car_vertical_distance<2*C.BOOST*C.SPEED)) else \
                  #3 if (enemy_in_front and (car_vertical_distance<3*C.BOOST*C.SPEED)) else \
                  #4    
                  
                  # 2 and 3 are actually not ideal for 2 reasons: you CANNOT escape if you move repeatedly,
                  # since the distance is strictly less than the one required to do it, and that factor is
                  # actually smaller than c.speed in almost every case (it is not only in case of big car with
                  # small speed and boost), hence it is rarely used
                  
        # Boolean value that tells if the enemy car is on the left of the car 
        # (hence, if it is False the enemy is on the right)
        enemy_leftright = (self.enemy_x_position < self.playerPosition)
        #print("enemy in front, poldist, leftright: ",enemyInFront,pol_dist,enemy_leftright)
        return [enemyInFront,pol_dist,enemy_leftright]
        
    def get_state(self): 
        """
        Return the state of the environment: a quintuple (enemy_in_front, pol_dist, enemy_leftright, obstacle_left, obstacle_right)
        """
        state=(*self.frontPositionBinning(),*self.sidePositionBinning())
        return np.array(state,dtype=int)
