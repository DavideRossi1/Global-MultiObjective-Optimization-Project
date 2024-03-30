import pygame
import time
import random

pygame.init()
red=(255,0,0)
black=(0,0,0) 

# environment parameters:
CAR_SPEED = 2           # speed of your car. 1 is human speed
POLICE_SPEED = 4        # speed of the police cars. 3 is human speed
DISPLAY_RESULT = True   # do you want the results to be displayed at the end of the game?
GAME_DIFF = 0.1         # difficulty of the game: how much cars increase their speed. 0.1 is human difficulty
DISPLAYSIZE = (840,650) # size of the display
CARSIZE = (104,200)     # size of the car image
EDGE = 130              # size of the road edge

display = pygame.display.set_mode(DISPLAYSIZE) 
pygame.display.set_caption("Play")  

BACKGROUNDIMG = pygame.image.load("GUIGame/car_images/background.png")
CARIMG = pygame.image.load("GUIGame/car_images/car.png").convert_alpha()
ENEMYIMGS = [pygame.image.load("GUIGame/car_images/car"+str(i)+".png").convert_alpha() for i in range(7)]

def policecar(enemy_x_position, enemy_y_position, car):
    #load car images
    display.blit(ENEMYIMGS[car], (enemy_x_position,enemy_y_position))      #display the police car

def background():
    # create the background
    display.blit(BACKGROUNDIMG,(0,0))
 
def car(car_x_position, car_y_position): 
    """
    Displays the car in the position (x,y)
    """
    #create car function
    display.blit(CARIMG,(car_x_position, car_y_position))     #set position of the car
    
def crash(score): 
    """
    Displays the message "Game Over" with the game score, and restarts the game after 3 seconds
    """
    if DISPLAY_RESULT:      
        message_display("Game Over",score)
        time.sleep(3)           # Wait 3 seconds before starting a new game
    main()
    
def message_display(text,score): 
    """"
    Displays a message on the screen
    """    
    large_text=pygame.font.Font("freesansbold.ttf",DISPLAYSIZE[1]//8) # font style and size
    gameOverSurf,gameOverRect = text_object(text,large_text,red)     #set function to edit the message
    scoreSUrf,scoreRect       = text_object("Score: "+str(score),large_text,black)
    gameOverRect.center=((DISPLAYSIZE[0]//2),(0.4*DISPLAYSIZE[1]))                      #set the position of the messages on the screen
    scoreRect.center=((DISPLAYSIZE[0]//2),(0.6*DISPLAYSIZE[1]))
    display.blit(gameOverSurf,gameOverRect)                    #display the messages
    display.blit(scoreSUrf,scoreRect)
    pygame.display.update()
       
def text_object(text,font,color):    
# display the message after the car has crashed
    text_surface=font.render(text,True,color)     #set color of the message
    return text_surface,text_surface.get_rect()   #after that restart the game & ready to give some input 



# main loop
def main(): 
    score = 0
    car_x = (DISPLAYSIZE[0]-CARSIZE[0])/2   # initial position of the car
    car_y = DISPLAYSIZE[1]-CARSIZE[1] 
    policecar_speed = POLICE_SPEED        # starting speed of the police car
    police_x = random.randrange(EDGE,(DISPLAYSIZE[0]-EDGE-CARSIZE[0])) # police car will comes in x axis in random value 
    police_y = -DISPLAYSIZE[1]                       # police car will comes in y axis in negative value because car is coming from opposite side 
    police_width = 0.8*CARSIZE[0]                     # width of the police car
    police_height = 0.85*CARSIZE[1]                   # height of the police car
    enemyCar = random.randrange(0,6)                  # choose a new police car
    
    while True:                   # start the game 
        for event in pygame.event.get():  # define the events
            action = getAction(event)
        car_x += action                       # move the car
        background()                      # display the background
        policecar(police_x,police_y,enemyCar) # display the police car
        police_y += policecar_speed         # move the police car
        car(car_x,car_y)                          # display the car
        if car_x<EDGE or car_x>DISPLAYSIZE[0]-EDGE-CARSIZE[0]:    # if the car is out of the road    
            crash(score)   # display game over and restart the game
        
        if police_y>DISPLAYSIZE[1]:     # if the police car is out of the screen
            score+=1
            policecar_speed += GAME_DIFF*policecar_speed      # increases the speed of the police car at each iteration
            police_y=0-police_height  #only one car will cross the road in one time
            police_x=random.randrange(EDGE,(DISPLAYSIZE[0]-EDGE-CARSIZE[0]))  #then other car will come in random position
             
        if car_y < police_y + police_height:
            if (police_x >= car_x and police_x <= car_x + CARSIZE[0]) or (police_x + police_width >= car_x and police_x + police_width <= car_x + CARSIZE[0]):
                crash(score)   
        pygame.display.update() # update the display
        
 
def getAction(event):
    x_change = 0
    if event.type==pygame.QUIT:          # quit
        pygame.quit()
        quit()
    if event.type==pygame.KEYDOWN:       # pressure of arrow keys
        if event.key==pygame.K_LEFT:        # left arrow:
            x_change = -CAR_SPEED                     # car will move left side 1
        if event.key==pygame.K_RIGHT:       # right arrow:
            x_change = CAR_SPEED                      # car will move right side 1
    # if event.type==pygame.KEYUP:         # no pressure of arrow keys  
    #     x_change = 0                          # stand still      
    return x_change 
        
main() # start the game
pygame.quit() 
quit()     