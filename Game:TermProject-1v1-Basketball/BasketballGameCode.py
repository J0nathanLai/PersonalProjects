"""
15-112 1v1 Basketball by Jonathan Lai (jklai)
"""
"""
this is the document for my 112 TP Project:
April 9 - general outline of code.
April 13 - importing images and appstart variables, started on ball physics
April 14 - vertical & horizontal ball physics for dribbling implemented + out of bounds
April 15 - free bounce
April 16 - jumpshot ball physics(in progress) + setup for AI computer-player(in progress) + playerData
April 18 - fix parabolic arc for jumpshot
April 19 - jumpshot power control done, jumpshot ball animation done, score ball animation done, pick up basketball animation done, fix other bugs
April 20 - scoring/point-tracking, AI comp movement, basic pushing collisions with strength (in progress)
April 21 - collisions with dribbling, fix bugs, created backboard, AI comp non-defending functions - not comp defend functions like picking up ball (in progress)
April 22 - fix bugs, AI comp can pick up ball, AI comp chases ball when ball is not in anyones possession, AI shoots not dependent on distance, layup (in progress)
April 23 - AI comp and user can make layups, AI shots depend on distance (essentially it can shoot anywhere from halfcourt) and depends on user's distance, stealing ball, points system, added miss shots
April 24 - fixed miss & make baskets, AI comp and user can take turns shooting depending on who scored the last basket, out of bound reseting and message, shotpower indicator, basket make message, added probability to all the different shots and moves
April 25 - added menu and player selection, implemented players' attributes based on the dictionary, added more players, added instructions, fixed layup bugs and collision bugs
"""
###   Image Citations at the bottom of the document.   ###

from cmu_graphics import *
from PIL import Image
import os, pathlib
import random 

playerDict = {"Russell Westbrook": {"image": "westbrook.png", "speed": 9, "strength": 6, "3pointer": 3, "midrange": 5, "layup": 8, "dribbling": 7, "steal": 6, "block": 4},
              "Lebron James": {"image": "james.png", "speed": 8, "strength": 7, "3pointer": 5, "midrange": 6, "layup": 9, "dribbling": 7, "steal": 5, "block": 6},
              "Kevin Durant": {"image": "durant.png", "speed": 7, "strength": 6, "3pointer": 8, "midrange": 9, "layup": 9, "dribbling": 7, "steal": 5, "block": 4},
              "Stephen Curry ": {"image": "curry.png", "speed": 8, "strength": 4, "3pointer": 9, "midrange": 9, "layup": 9,  "dribbling": 9, "steal": 6, "block": 2},
              "James Harden": {"image": "harden.png", "speed": 6, "strength": 5, "3pointer": 8, "midrange": 7, "layup": 9, "dribbling": 9, "steal": 6, "block": 2},
              "Kawhi Leonard": {"image": "leonard.png", "speed": 6, "strength": 7, "3pointer": 8, "midrange": 9, "layup": 8, "dribbling": 5, "steal": 8, "block": 5}
              }
#------------------------------------------------------------------------------------------------------------------------------
class Game:
    def __init__(self):
        self.gameOver = False
        self.gamePaused = False

#------------------------------------------------------------------------------------------------------------------------------
class Ball:
    def __init__(self, x, y, user, comp, app):
        ballImage = Image.open(os.path.join(pathlib.Path(__file__).parent,"Basketball.png"))        #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.ballImageW, self.ballImageH = ballImage.width//13, ballImage.height//13    #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.ballImage = CMUImage(ballImage)    #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.ballRotate = 0     #intitialize rotation angle for ball

        self.x = x
        self.dx = 0
        self.ddx = 1
        self.y = y
        self.dy = 0 
        self.ddy = 1
        self.dribble = True     #whether ball is being dribbled 
        self.free = False   #whether ball is free bouncing on its own
        self.freeI = 0
        self.tmpdir = 0

        self.shoot = False      #whether ball is in the air 

        self.user = user
        self.comp = comp

        self.scoreIUser = 0
        self.scoreUser = 0
        self.scoreIComp = 0
        self.scoreComp = 0
        self.goal = False

        self.screenW = app.width
        self.screenH = app.height

        self.possession = +1
        
        self.lastTouch = +1
        self.outOfBound = False

        self.floor = 585

        self.gravCoeff = 0.55

        self.shotLocX = 1280
        self.shotPlayerDist = 1280
        self.forceShotLoc = 1280

        self.defLocX = 0

        self.layupTimer = 0

        self.missed = False

        self.scorer = 0

        self.chargeUp = False

    def ballPhy(self, hdir, player):
        if self.dribble == False and self.shoot == False and self.free == True: #free bouncing ball
            self.freeBounce(hdir)        

        elif self.dribble == True and self.possession != 0:  #ball in possession
            self.dribbleBall(player)
            self.free = False

    def shootBallPhy(self, player, shotLocX, defLocX): #if player is 1, then ball moves toward + direction; if player is -1, then ball moves toward - direciton
        if self.goal == False and (self.missed == True or (self.scoring(player, shotLocX, defLocX) == False)):    #if shot is missed or didn't score, result in no goal, then run miss ball phy animation
            self.miss(player, shotLocX)
            self.missed = True
            self.goal = False
        else:
            if self.missed == False and (self.goal == True or (self.scoring(player, shotLocX, defLocX) == True)):  #else if made shot result in goal and not missing shot then run make ball phy animation
                self.dx = 0
                self.dy = 15
                self.y += self.dy
                if player == 1:
                    self.scoreIUser += 1        #using a score index to add points once
                    if self.scoreIUser == 1:
                        if shotLocX < 820:
                            self.scoreUser += 3    #3 points if outside of arch
                        else:
                            self.scoreUser += 2     #2 points if inside of arch
                        self.scorer = 1
                elif player == -1:
                    self.scoreIComp += 1        #using index to add points once
                    if self.scoreIComp == 1:
                        if shotLocX > 460:
                            self.scoreComp += 3     #3 points if outside of arch
                        else:
                            self.scoreComp += 2     #2 points if inside of arch
                        self.scorer = -1                
                self.goal = True

            elif self.goal == False:        #else if goal is false, meaning ball is travelling is about to be shot
                self.scoreIComp, self.scoreIUser = 0, 0 #reset the score index
                if (player == 1 and shotLocX >= 980) or (player == -1 and shotLocX <= 300):         # if shot location for player 1(user) is in the paint or if shot location for comp is in the paint
                    self.layupTimer += 1
                    if self.layupTimer % 2 == 0:    #for every 2/30 of a second run the layup ball physics (used timer to slow down layup motion or else it will move too fast, may see choppy)
                        self.layupBallPhy(player, shotLocX)     #running the layup ball physics
                else:       #or else if shotlocation is not in either of the paints
                    self.comp.shootI += 1   #increase the shooting index to only collect the shooting location at the beginning of the shot (shooting location collected in game_onStep when shootI == 1)
                    if self.dx > 6:     #prevent ball from moving in horizontal direction too fast
                        self.dx = 6
                    self.x += self.dx * player  #ball shot's horizontal direction depends on player
                    self.dx += self.ddx     #performing parabolic shooting arch (algorithmic complexity)
                    self.ddy = -abs(self.ddy)   #performing parabolic shooting arch (algorithmic complexity)
                    self.y -= self.dy   #performing parabolic shooting arch (algorithmic complexity)
                    self.dy += -abs(self.ddy)   #performing parabolic shooting arch (algorithmic complexity)

            if self.y >= self.floor:    #whenever ball reaches floor level perform a bounce
                self.dy = self.dy * 0.85    #ball bounce up less and less
                self.ddy = 1
                self.freeBounce(player)     #determines the horizontal direction in which the ball bounces freely when landing on the floor
                self.shoot = False      #reseting variable
                self.user.userShoot = False
                self.dribble = False
                self.comp.shootI = 0
                self.layupTimer = 0
            self.missed = False

    def scoring(self, player, shotLocX, defLocX):
        ballX = self.x
        ballY = self.y
        hoopXLeft = self.screenW * 0.125
        hoopXRight = self.screenW * 0.875
        hoopY = self.screenH * 0.43
        if ((distance(ballX, ballY, hoopXLeft, hoopY) <= 50 or                          #if ball is near the left hoop
        distance(ballX, ballY, hoopXRight, hoopY) <= 50)) and self.missed == False:     #or right hoop
            playersDist = abs(shotLocX - defLocX)
            probRan = random.random()           #probRan is a random number in range [0, 1)
            if playersDist < 50:        #if the user and comp are close enough
                blockActivated = 1      #then defending player can block (using binary dummy variable to turn on/off the blocking variable)
            else:                   
                blockActivated = 0      #else defending player can't block
            if player == 1:                     #for a shot made by the user
                if shotLocX <= 820:             #if user shot ball beyond 3-point line
                    if probRan < 0.5 * (self.user.pointer3 * 0.1) + playersDist*0.001:       #if probRan is less than 0.5 multiplied by 10% of 3-point rating plus 0.1% of the players' distance
                        self.goal = True                                                    #then shot is made
                        return True
                    else:              
                        self.missed = True                                    #else shot is missed
                        return False
                elif 980 > shotLocX > 820:     #if user shot ball between 3-point line and the paint (midrange shot)
                    if probRan < 0.6 * (self.user.midrange * 0.1) + playersDist*0.001:            #if probRan is less than 0.6 multiplied by 10% of midrange rating plus 0.1% of the players' distance
                        self.goal = True                                                   #then shot is made
                        return True
                    else:
                        self.missed = True                                                 #else shot is missed
                        return False
                elif shotLocX >= 980:          #if user shot ball within the paint (layup)
                    if probRan < 0.8 * (self.user.layup * 0.1) + playersDist*0.001 - (blockActivated * self.comp.block*0.015):    #since, in this game, block acts as a contest and block can only be used when the attacking player is laying up, if players are close enough then block will be activated, else, players won't get blocked
                        self.goal = True                                                   #then shot is made
                        return True             
                    else:
                        self.missed = True                                                 #else shot is missed
                        return False
                """this process of determining basket success is repeated below but for the AI comp player; essentially, the probabily of success for making a basket
                depends on the type of shot (influenced by distance from the basket) and the distance between the two players and the defending player's block rating(for layups)"""
            elif player == -1:     
                if shotLocX >= 460:
                    if probRan < 0.5 * (self.comp.pointer3 * 0.1) + playersDist*0.001:
                        self.goal = True
                        return True
                    else:
                        self.missed = True
                        return False
                elif 460 > shotLocX > 300:
                    if probRan < 0.6 * (self.comp.midrange * 0.1) + playersDist*0.001:
                        self.goal = True
                        return True
                    else:
                        self.missed = True
                        return False
                elif shotLocX <= 300: 
                    if probRan < 0.8 * (self.comp.layup * 0.1) + playersDist*0.001 - (blockActivated * self.user.block*0.015):
                        self.goal = True
                        return True
                    else:
                        self.missed = True
                        return False

    def miss(self, player, shotLocX):
        self.y += abs(self.dy)  #to drop the ball towards the floor
        if abs(self.dy) < 10 or self.dy >= 15:      #to drop ball not too fast and not too slow after missed shot
            self.dy = 10
        if (player == 1 and shotLocX >= 980) or (player == -1 and shotLocX <= 300):     #for layups
            self.dy = abs(self.dy * 2)  #vert direction for missed layup
            self.dx = self.dx * 0.5     #hor direction for missed layup
        elif (player == 1 and shotLocX <= 980) or (player == -1 and shotLocX >= 300):   #for jumpshots
            self.x += -abs(self.dx) * player * 0.6      #hor direction for missed jumpshot
            self.dx += self.ddx
            if self.dx >= 5:        #slow down hor direction for missed jumpshot
                self.dx = 5
        self.missed = True      #make miss variable true so that it will loop over this miss function again in shootBallPhy function

        if self.y >= self.floor:        #after hitting the ground
            self.dy = self.dy * 0.85    #slowly decrease bounce height after hitting ground after a shot
            self.ddy = 1
            self.dx = self.dx * 0.5 * -abs(player)  #horizontal direction after miss and after hitting the ground depends on player's shooting direction
            self.freeBounce(0)      #bounce freely as it hits ground
            self.shoot = False      #reset variables
            self.dribble = False
            self.comp.shootI = 0
            self.layupTimer = 0
            self.user.userShoot = False
        

    def layupBallPhy(self, player, shotLocX):
        if player == 1:
            distFromBasket = abs(shotLocX - 1280*0.875)     #shot location - basket location
        elif player == -1:
            distFromBasket = abs(shotLocX - 1280*0.125)     #shot location - basket location
        else:
            distFromBasket = 0
        layupStrength = distFromBasket * 0.01       #formula - layup strength/power depends on distance 
        self.x += layupStrength * self.dx * player
        self.dx += self.ddx
        if self.dx + self.ddx >= 5:     #not let hor direction grow too fast
            self.dx = 5
        if self.dy >= 5:                #not let vert direction grow too fast
            self.dy = 5
        self.y += -5 * self.dy      
        self.dy += self.ddy
        if self.y <= 240:           #layup physic showing that the ball drops at the vertex height of 240
            self.dx = 0.1
            self.dy = -abs(self.dy)
            
    def pickUp(self):
        self.goal = False
        self.missed = False
        userX = self.user.x
        compX = self.comp.x
        ballX = self.x
        ballY = self.y
        userDist = distance(ballX, ballY, userX, self.floor)
        compDist = distance(ballX, ballY, compX, self.floor)
        if userDist <= 10 or compDist <= 10:        #if either player picks up, reset the below variables
            self.dy = 9         #ball can be dribbled normally at a decent height
            self.dribble = True
            self.shoot = False
            self.user.userShoot = False
            self.shotLocX = self.x
            self.forceShotLoc = 1280
            self.chargeUp = False

        if userDist <= 10:      #change below variables and allow dribbling for user
            self.possession = +1
            self.lastTouch = +1
            self.dribbleBall(+1)
            
        elif compDist <= 10:    #change below variables and allow dribbling for comp
            self.possession = -1
            self.lastTouch = -1
            self.dribbleBall(-1)
        


    def freeBounce(self, hdir):
        self.possession = 0
        self.dx = 0.95*self.dx #rolls on the ground & comes to a stop
        self.x += self.dx * hdir    #hdir the direction which ball freely bounces, it changes depending on who last shot the ball or the dribbling direction
        
        self.y += self.dy
        self.dy += self.ddy
        if self.y >= self.floor:
            self.y = self.floor
            self.dy = -self.gravCoeff* abs(self.dy) #gravity        #from 15112 lecture on Apr 11 (i believe)

    def dribbleBall(self, player):
        self.vertDrib()
        self.horDrib(player)
     
    def vertDrib(self):     #vertical dribbling animation
        self.y += self.dy
        self.dy += self.ddy
        if self.y >= 585:   #not let ball bounce below the floor
            self.y = 585
            self.dy = -0.8 * abs(self.dy) #gravity          #from lecture   Apr 11
        if self.y < 550:    #not let ball bounce above the players' hands
            self.y = 550
            self.dy = -self.dy
    
    def horDrib(self, player):  #aliases the ball's coordinates to the whichever player that is dribbling
        if player == +1:    #follow user's movement
            self.x = self.user.x    
            self.dx = self.user.dx
        elif player == -1:  #follow comp's movement
            self.x = self.comp.x
            self.dx = self.comp.dx
                
    def bounceBackboard(self):
        if  ((1120 <= self.x <= 1170) and (200 <= self.y <= 345) or #if hit either backboards
            (110 <= self.x <= 160) and (200 <= self.y <= 345)):
            self.dx = -abs(self.dx)     #flip the horizontal direction of the ball


    def steal(self, player, app):
        if self.comp.collide == True and app.ball.free == False and app.ball.shoot == False and self.chargeUp == False:    #if someone is dribbling and both players collide
            if player == 1:     #if player 1 (user) steals the ball
                self.possession = 1     #then possession goes to user
                self.lastTouch = 1
                self.x = self.user.x    #ball's location will go to user
                self.shotLocX = app.ball.x
                self.forceShotLoc = 1280
            elif player == -1:  #if comp steals the ball
                self.possession = -1    #then possession goes to comp
                self.lastTouch = -1
                self.x = self.comp.x    #ball's location will go to the comp
                self.shotLocX = app.ball.x
                self.forceShotLoc = 1280
            app.message = "stolen"  #message for stealing ball from opposing player
            

    def drawBall(self):
        drawImage(self.ballImage, self.x, self.y, 
                  width = self.ballImageW, height = self.ballImageH, 
                  rotateAngle = self.ballRotate, align = 'center')  #angle of rotation is updated in game_onStep

#------------------------------------------------------------------------------------------------------------------------------
class User():
    def __init__(self, x, y, playerDict, name):
        userImage = Image.open(os.path.join(pathlib.Path(__file__).parent,playerDict[name]["image"]))    #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.userSpriteList = []
        self.userSpriteList.append(CMUImage(userImage))         #from KirbleBirdStarter demo
        flipped = userImage.transpose(Image.Transpose.FLIP_LEFT_RIGHT)      #from KirbleBirdStarter demo
        flipped = CMUImage(flipped)
        self.userSpriteList.append(flipped)         #from KirbleBirdStarter demo
        self.userImageW, self.userImageH = userImage.width//6, userImage.height//6    #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.userSpriteI = 0

        self.x = x
        self.y = y
        self.dx = 0
        self.ddx = 1
        
        self.userShoot = False

        self.cantGoLeft = False
        self.cantGoRight = False

        #attributes   indexes into the player dictionary with attributes of each player 
        self.speed = playerDict[name]["speed"] * 0.8    #multiplied by 0.8 to prevent players from zooming through the court
        self.strength = playerDict[name]["strength"]
        self.pointer3 = playerDict[name]["3pointer"]
        self.midrange = playerDict[name]["midrange"]
        self.layup = playerDict[name]["layup"]
        self.dribbling = playerDict[name]["dribbling"]
        self.steal = playerDict[name]["steal"]
        self.block = playerDict[name]["block"]

    def movePlayer(self, dir):
        self.x += (self.dx*dir)     #horizontal direction depends on user's input in onKeyHold
        self.dx += self.ddx
        if self.dx + self.ddx >= self.speed: #dx cannot exceed player's speed attribute
            self.dx = self.speed

    def drawUser(self):
        drawImage(self.userSpriteList[self.userSpriteI], self.x, self.y, #the self.userSpriteI indexes into a list of 2 images of the player (an original version and a flipped one)
                  width = self.userImageW, height = self.userImageH, 
                  align = 'bottom')
#------------------------------------------------------------------------------------------------------------------------------   
class Comp():
    def __init__(self, x, y, user, playerDict, name):
        compImage = Image.open(os.path.join(pathlib.Path(__file__).parent,playerDict[name]["image"]))   #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.compSpriteList = []
        self.compSpriteList.append(CMUImage(compImage))         #from KirbleBirdStarter demo
        flipped = compImage.transpose(Image.Transpose.FLIP_LEFT_RIGHT)      #from KirbleBirdStarter demo
        flipped = CMUImage(flipped)
        self.compSpriteList.append(flipped)         #from KirbleBirdStarter demo
        self.compImageW, self.compImageH = compImage.width//6, compImage.height//6  #from basicPILMethods from Piazza post https://piazza.com/class/lcnu63g1yps41j/post/1408
        self.compSpriteI = 0
        
        self.x = x
        self.y = y
        self.dx = 0
        self.ddx = 1

        self.user = user

        self.collide = False

        self.shootI = 0

        self.cantGoRight = False
        self.cantGoLeft = False

        #attributes     indexes into the player dictionary with attributes of each player 
        self.speed = playerDict[name]["speed"] * 0.8        #multiplied by 0.8 to prevent players from zooming through the court
        self.strength = playerDict[name]["strength"]
        self.pointer3 = playerDict[name]["3pointer"]
        self.midrange = playerDict[name]["midrange"]
        self.layup = playerDict[name]["layup"]
        self.dribbling = playerDict[name]["dribbling"]
        self.steal = playerDict[name]["steal"]
        self.block = playerDict[name]["block"]

    def compMovement(self, ballX, possession, counter):
        userX = self.user.x
        userY = self.user.y
        compX = self.x
        compY = self.y
        playersDist = distance(compX, compY, userX, userY)

        if possession == 0:     #if no one has possession, comp chases the ball
            self.compToBallMovement(ballX)
        
        elif playersDist < 50:      #if players collide
            self.collide = True
            self.collision()        #run the collision function which determines the movement speed of both players depending on strength of both players
    
        elif playersDist >= 50:     #if players dont collide
            if counter % 5 == 0:
                self.compSpriteI = (self.compSpriteI + 1) % 2   #flip the image of both players every 1/6 of a second
            elif possession == 1:   #if user has possession
                self.compDefMovement()  #comp chases the user
            elif possession == -1:  #if comp has possession
                self.compAttMovement()  #comp moves toward the opponent's basket
            self.user.cantGoLeft, self.user.cantGoRight = False, False  #reset the movement restriction variables for the user when they dont collide
        if self.x <= 100:  #Prevent AI from going out of Bounds
            self.x = 100
        elif self.x >= 1180:  #Prevent AI from going out of Bounds
            self.x = 1180

    def compToBallMovement(self, ballX):
        self.collide = False
        ballX = ballX
        compX = self.x
        compY = self.y
        distToBall = distance(ballX, compY, compX, compY)
        if distToBall > 5:  #if ball is not near the comp
            if ballX > self.x:  #if ball is on the right of the comp
                self.x += self.dx   #move right
                self.dx += self.ddx 
            elif ballX < self.x:    #if ball is on the left of comp
                self.x += -self.dx  #move left
                self.dx += self.ddx
            if self.x + self.dx >= self.speed: #dx cannot exceed speed
                self.dx = self.speed

    def compDefMovement(self):
        userX = self.user.x
        self.collide = False
        if self.x > userX:  #if user is on the left of comp
            self.x += -self.dx  #move left
            self.dx += self.ddx
            if self.dx + self.ddx >= self.speed * 0.8: #dx cannot exceed its speed*0.8, because defenders dont just rush into the attacking player when standing in front of attacking player
                self.dx = self.speed * 0.8
        elif self.x < userX:    #if user is on the right of the comp
            self.x += self.dx   #chase the user down by moving right
            self.dx += self.ddx
            if self.dx + self.ddx >= self.speed: #dx cannot exceed speed
                self.dx = self.speed

    def compAttMovement(self):
        self.collide = False
        self.x += -self.dx  #move left towards the opponent's basket
        self.dx += self.ddx
        if self.dx + self.ddx >= self.speed: #assuming 5 is the speed, dx cannot exceed 5, should be self.speed
            self.dx = self.speed

    def collision(self):
        userStrength = self.user.strength
        compStrength = self.strength
        if userStrength > compStrength:    #if user is stronger than comp
            diffStrength = userStrength - compStrength
            if self.user.x > self.x:        #if comp is behind user, then comp can't move/push user
                self.user.dx = diffStrength * 0.75  #user is slowed down when they collide, how much they are slowed down depends on the difference in their strength
                self.dx = self.user.dx  #computer's speed depnds on the user's speed
                self.x -= self.dx   #moving left
            elif self.user.x < self.x:                           #or else if comp is in front of user, then comp will get pushed by user if user moves forward
                self.user.dx = diffStrength * 0.75
                self.dx = self.user.dx
                self.x += self.dx   #moving right
        elif userStrength < compStrength:   #if comp is stronger than user
            diffStrength = compStrength - userStrength
            if self.user.x < self.x:        #if user is in front of comp, then user gets pushed
                self.user.cantGoRight = True    #user cant go right because user isn't strong enough
                self.dx = diffStrength * 0.75   #comp is slowed down when they collide, how much they are slowed down depends on the difference in their strength
                self.user.dx = diffStrength * 0.75  #user is slowed down the same as it is being pushed while colliding
                self.x -= self.dx   #moving left
                self.user.x -= self.user.dx     #moving left
            elif self.user.x > self.x:         #if user is behind comp, then user can't move/push comp
                self.user.cantGoLeft = True #user can't move comp when they collide as user is not as strong as comp

        elif userStrength == compStrength:  #if they are equally strong
            if self.user.x < self.x:
                self.user.cantGoRight = True    #user cant go right if user is on the left of the comp
            elif self.user.x > self.x:
                self.user.cantGoLeft = True     #user cant go left if user is on the right of the comp

    def drawComp(self):
        drawImage(self.compSpriteList[self.compSpriteI], self.x, self.y,    #the self.compSpriteI indexes into a list of 2 images of the player (an original version and a flipped one)
                  width = self.compImageW, height = self.compImageH, 
                  align = 'bottom')
#------------------------------------------------------------------------------------------------------------------------------   
def onAppStart(app):  #Menu
    app.game = Game()

    app.imageList = []
    app.nameList = []
    for name in playerDict:     #adding all the available players to a list
        playerImage = playerDict[name]["image"]
        app.imageList.append(playerImage)
        app.nameList.append(name)

    app.imageListLen = len(app.imageList)
    app.photoIndexUser = 0
    app.photoIndexComp = 1

    app.userImage = Image.open(os.path.join(pathlib.Path(__file__).parent, app.imageList[app.photoIndexUser]))
    app.userImageW, app.userImageH = app.userImage.width//3, app.userImage.height//3
    app.userImage = CMUImage(app.userImage)     #displays player's image
    app.userName = app.nameList[app.photoIndexUser]     #displays player's name

    app.compImage = Image.open(os.path.join(pathlib.Path(__file__).parent, app.imageList[app.photoIndexComp]))
    app.compImageW, app.compImageH = app.compImage.width//3, app.compImage.height//3
    app.compImage = CMUImage(app.compImage)     #displays player's image
    app.compName = app.nameList[app.photoIndexComp]     #displays player's name

    app.instructions = False

def menu_onStep(app):
    if abs(app.photoIndexUser) > app.imageListLen - 1: #wrap around list index to allow user to select the player they will use while going through the player list
        app.photoIndexUser %= app.imageListLen
    app.userImage = Image.open(os.path.join(pathlib.Path(__file__).parent, app.imageList[app.photoIndexUser]))
    app.userImage = CMUImage(app.userImage)     #updates chosen players as user selects
    app.userName = app.nameList[app.photoIndexUser]     #updates chosen names as user selects

    if abs(app.photoIndexComp) > app.imageListLen - 1: #wrap around list index to allow user to select the opponenet while going through the player list
         app.photoIndexComp %= app.imageListLen
    app.compImage = Image.open(os.path.join(pathlib.Path(__file__).parent, app.imageList[app.photoIndexComp]))
    app.compImage = CMUImage(app.compImage)     #updates chosen players as user selects
    app.compName = app.nameList[app.photoIndexComp]     #updates chosen names as user selects

def menu_redrawAll(app):
    drawRect(0, 0, 1280, 720, fill = "darkSlateGrey")
    drawLabel("1v1 Basketball", app.width//2, app.height//2 - 200, size = 40, fill = "lightGrey", bold = True, align = "center")        #game title
    drawLabel("Select your player", app.width//4, app.height//2 - 150, size = 30, fill = "lightGrey", align = "center")         #player selection
    drawLabel("Select your opponent", app.width*3//4, app.height//2 - 150, size = 30, fill = "lightGrey", align = "center")         #opponent selection
    drawRect(app.width//4 - 150, app.height//2 - 125, 300, 400, fill = "midnightBlue")    #blue rect
    drawRect(app.width//4 - 150, app.height//2 - 125, 50, 50, fill = "grey")   #left button
    drawLabel("left", app.width//4 - 150+25, app.height//2 - 125+25, size = 20, fill = "black", align = "center")  #left button
    drawRect(app.width//4 + 100, app.height//2 - 125, 50, 50, fill = "grey")  #right button
    drawLabel("right", app.width//4 + 100+25, app.height//2 - 125+25, size = 20, fill = "black", align = "center")   #right button

    drawRect(app.width*3//4 - 150, app.height//2 - 125, 300, 400, fill = "firebrick")     #red rect
    drawRect(app.width*3//4 - 150, app.height//2 - 125, 50, 50, fill = "grey")   #down button
    drawLabel("down", app.width*3//4 - 150+25, app.height//2 - 125+25, size = 20, fill = "black", align = "center")  #down button
    drawRect(app.width*3//4 + 100, app.height//2 - 125, 50, 50, fill = "grey")  #up button
    drawLabel("up", app.width*3//4 + 100+25, app.height//2 - 125+25, size = 20, fill = "black", align = "center")   #up button

    drawImage(app.userImage, app.width//4 - 140, app.height//2 - 100, width = app.userImageW, height = app.userImageH)  #user image
    drawLabel(app.userName, app.width//4, app.height//2 + 200, size = 30, fill = "white", bold = True)  #user name

    drawImage(app.compImage, app.width*3//4 - 140, app.height//2 - 100, width = app.compImageW, height = app.compImageH)    #comp image
    drawLabel(app.compName, app.width*3//4, app.height//2 + 200, size = 30, fill = "white", bold = True)    #comp name

    drawLabel("Press 'Enter' to start game!", app.width//2, app.height//2+75, size = 25, fill = "white")

    drawLabel("Press 'i' for instructions.", 100, 20, size = 16, fill = "yellow")

    if app.instructions == True:        #show instructions is true
        drawRect(app.width//8, 190, 960, 500)       
        drawInstructions(app, instructionText)  #instruction text is below

def menu_onKeyPress(app, key):
    if key == "right":      #changes photo index for user
        app.photoIndexUser += 1
    if key == "left":       #changes photo index for user
        app.photoIndexUser -= 1
    if key == "up":         #changes photo index for comp
        app.photoIndexComp += 1
    if key == "down":       #changes photo index for comp
        app.photoIndexComp -= 1
    if key == "enter":      #starts gameplay
        onGameStart(app)
        setActiveScreen('game')
    if key == "i":
        app.instructions = not app.instructions     #oscillates between true and false for instruction variable 

instructionText = """ You're controlling the player on the left\n
first to 21 wins\n
use the left right arrow keys to move the player\n
use the "s" button to shoot\n
the shot power bar indicates how long you should hold the key depending on where your player is standing on the court\n
the shot power only applies to jump shots, layups only require pressing the "s" button once\n
use the "d" button to dribble past your opponent\n
you will only succeed to dribble past your opponent occasionally depending on your player's dribbling rating\n
use the "c" button to steal the ball from your opponent\n
you will only succeed to steal the ball occasionally depending on your player's steal rating\n
you may leave the game at any point by pressing "esc"\n
or you may pause the game by pressing "i"
"""

def drawInstructions(app, instructionText):
    height = 200
    for line in instructionText.splitlines():       #splits text into diff lines
        height += 20
        drawLabel(line, app.width//2, height, size = 16, fill = "white")
        
#------------------------------------------------------------------------------------------------------------------------------   

def onGameStart(app):
    ###User
    app.userX = app.width//2 - 300
    app.userY = app.height//2 + 240
    app.user = User(app.userX, app.userY, playerDict, app.userName)     #initializes user which is indexed into the selected player

    ###Comp
    app.compX = app.width//2 + 300
    app.compY = app.height//2 + 240
    app.comp = Comp(app.compX, app.compY, app.user, playerDict, app.compName)        #initializes comp which is indexed into the selected player

    ###Ball
    app.ballX = app.width//2 - 290
    app.ballY = app.height//2 + 190
    app.ball = Ball(app.ballX, app.ballY, app.user, app.comp, app)

    ###background
    app.backg = Image.open(os.path.join(pathlib.Path(__file__).parent,"basketball-court.jpg"))      #basketball court 
    app.backgW, app.backgH = app.backg.width/1.5, app.backg.height/1.5
    app.backg = CMUImage(app.backg)
    app.backgroundX = app.width//2
    app.backgroundY = app.height//2

    ###Gameplay
    app.game = Game()

    app.counter = 1     #for various timed events (e.g. comp movement, comp stealing move, comp dribbling moves, changing the frame of the players)

    app.message = ""    #for the message board

def game_redrawAll(app):
    drawImage(app.backg, app.backgroundX, app.backgroundY, width = app.backgW, height = app.backgH, align = 'center')
    app.comp.drawComp()
    app.user.drawUser()
    app.ball.drawBall()
    
    #drawCircle(app.width*0.875, app.height*0.43, 20, fill = 'red')  #indicates right basket
    #drawCircle(app.width*0.125, app.height*0.43, 20, fill = 'red')  #indicates left basket

    #drawPolygon(1120, 200, 1170, 240, 1170, 340, 1120, 280, fill = "blue")  #indicates right board
    #drawPolygon(160, 200, 110, 240, 110, 340, 160, 280, fill = "blue")        #indicates left board

    drawLabel(app.ball.scoreUser, 590, 110, size = 30, fill = "white")  #score for user
    drawLabel(app.ball.scoreComp, 690, 110, size = 30, fill = "white")  #score for comp

    drawRect(900, 670, 260, 40, fill = "turquoise", border = "cyan", borderWidth = 5)   #shooting indicator bar's border and filling
    if app.ball.chargeUp == True:
        drawRect(905, 675, app.indicatorBar, 30, fill = "limeGreen")       #shooting indicator bar's power
    drawLine(1095, 675, 1095, 705, fill = "black", lineWidth = 2)           #width of green rect is ~190 when app.ball.dy is 32, which is the 3 point "shot power"
    drawLabel("3 point", 1095, 660, size = 12, fill = "black", bold = True, align = "center")

    drawLine(1045, 675, 1045, 705, fill = "black", lineWidth = 2)           #width of green rect is ~145 when app.ball.dy is 23, which is the free-throw line "shot power"
    drawLabel("free-throw", 1045, 660, size = 12, fill = "black", bold = True, align = "center")

    if app.ball.outOfBound == True:
        drawLabel("Out Of Bounds!", app.width//2, app.height//2 - 100, size = 45, bold = True, fill = "red")    #out of bounds message
    

    drawLabel(app.message, app.width//2, app.height//2 - 180, size = 30, fill = "lawnGreen")

    if app.game.gamePaused == True:
        drawRect(0, 0, 1280, 720, fill = "grey", opacity = 55)  #paused screen
        drawLabel(f"PAUSED", app.width//2, app.height//2, size = 30, bold = True, fill = "white")   #paused messsage
        

    if app.game.gameOver == True:   
        if app.ball.scoreUser >= 21:    #determining winner
            winner = "You"
        elif app.ball.scoreComp >= 21:
            winner = "AI"
        drawRect(0, 0, 1280, 720, fill = "grey", opacity = 55)  #gameoverscreen
        drawLabel(f"Game Over! {winner} won!", app.width//2, app.height//2 + 75, size = 30, bold = True, fill = "white")    #game over messages
        drawLabel(f"Press 'esc' to leave game.", app.width//2, app.height//2 + 110, size = 30, bold = True, fill = "white")

def game_onStep(app):
    app.counter += 1

    if app.ball.scoreUser >= 21 or app.ball.scoreComp >= 21:    #game over detection
        app.game.gameOver = True

    if app.game.gameOver == False and app.game.gamePaused == False:   #continuation of game
        if app.ball.possession == 1:    #messsage for user
            app.message = "attack"
        if app.ball.possession == -1:   #messsage for user
            app.message = "defend" 
        
        app.ball.ballRotate -= 10   #change ball's angle of rotation

        if app.ball.goal == True:       #if player scores, message changes
            app.message = "swish!"
        #AI implementation from lines 730 - 780 and helper functions used in these lines (algorthimic complexity)
        if app.ball.possession == +1:   #if user has ball
            compStealProb = random.random()
            if app.counter % 30 == 0 and compStealProb < app.comp.steal * 0.015:    #if 1.5% of the steal rating is greater than the random number, (the counter is used to prevent the AI comp to spam the steal function, instead it will attempt to steal every second)
                app.ball.steal(-1, app)                                                  #then perform the steal function

        elif app.ball.possession == -1:     #AI comp has ball
            distPlayer = abs(app.comp.x - app.user.x)
            distFromBasket = abs(app.comp.x - 1280*0.125)
            #AI shooting from lines 739 - 773 and the helper functions used in the lines (algorithmic complexity) 
            if distFromBasket <= 80 and app.user.userShoot == False and app.ball.shoot == False and app.ball.free == False:    #so that AI will force-shoot a layup if it gets to the paint
                app.ball.forceShotLoc = app.ball.x      #determines force shot location 
                app.ball.dy = 10
                app.ball.shoot = True

            if app.ball.forceShotLoc <= 300:        #if shot location is within paint, then chuck up a layup shot automatically
                app.ball.collide = False
                app.ball.shoot = True   #turns true so that code will not run through the previous condition again, preventing the force shot location to change
                app.ball.free = True    #turns true so that code will not run through the previous condition again, preventing the force shot location to change
                app.ball.shootBallPhy(-1, app.ball.forceShotLoc, app.ball.defLocX)  #run shooting function specifically the layup ball phy isnide the shootballphy function
                app.ball.bounceBackboard()  #run the backboard function 
                app.ball.dribble = False
                app.ball.tmpdir = -1  #set the direciton of where the ball is going to -1 as ball is shot left
            else:       #or else if user and ball aren't in the paint, check whether there is enough distance for the comp to shoot "comfortably"
                if (app.user.userShoot == False and app.comp.x <= 500 and app.ball.shoot == False and app.ball.free == False):
                    app.ball.shotLocX = app.ball.x              #determines shooting location when the ball initially leaves comp's possession
                    app.ball.defLocX = app.user.x               #determines the defending player's location when the ball initially leaves the comp's possession
                    app.ball.shotPlayerDist = distPlayer
                    if distPlayer > 75:                     #reset ball.dy to 0 if ready to shoot which is when player distance is greater than 75 or else ball.dy will act normal
                        app.ball.dy = 0
                if (app.user.userShoot == False and app.ball.shotLocX <= 500 and app.ball.shotPlayerDist > 75):     #initalize the shooting motion at the shot location determined once in the previous conditional statement
                    if app.comp.shootI == 1:    #use index to determine distance from basket once, allowing shot power to be determined once by the shot power formula below
                        distFromBasket = abs(app.ball.shotLocX - 1280*0.125)
                        app.ball.y = 585    #reset the height of the ball when shot
                        if distFromBasket >= 230: #beyond three point line
                            app.ball.dy = distFromBasket/9.5  #comp shot power formula for 3pointers
                        else:
                            app.ball.dy = distFromBasket/8.5    #comp shot power formula for midrange
                    app.ball.shoot = True       #turns true so that code will not run through the previous condition again, preventing the shot location to be updated
                    app.ball.free = True        #turns true so that code will not run through the previous condition again, preventing the shot location to be updated
                    app.ball.shootBallPhy(-1, app.ball.shotLocX, app.ball.defLocX)
                    app.ball.bounceBackboard()
                    app.ball.dribble = False
                    app.ball.tmpdir = -1        #direction of ball will bounce to left when free bouncing after the shot lands on the ground
            
            if app.comp.collide == True and app.ball.shoot == False:  #comp dribbling past user
                compDribProb = random.random()
                if app.counter % 30 == 0 and compDribProb < app.comp.dribbling * 0.02: #if 2% of the drib rating is greater than the random number, (the counter is used to prevent the AI comp to spam the dribble past function, instead it will attempt to dribble past every second)
                    dribblePast(app, -1)

        app.comp.compMovement(app.ball.x, app.ball.possession, app.counter)  #AI movement (algorthimic complexity)
        if app.ball.dribble == False and app.ball.possession == 0 and app.ball.shoot == False and app.ball.free == True and app.user.userShoot == False:    #runs the pick up ball function for both players
            app.ball.pickUp()
        if app.ball.x > app.width * 0.92 or app.ball.x < app.width * 0.08: #runs the outOfBound function whenever ball is out of bound
            outOfBound(app, app.ball.lastTouch * -1, app.ball.scoreUser, app.ball.scoreComp)   #if user (player1) gets ball out of bound, then comp (player-1) get the next ball  

        if app.counter % (app.stepsPerSecond*5) == 0:     #for turning off the out of bound message after 5 seconds
            app.ball.outOfBound = False     

        if app.ball.shoot == True and app.user.userShoot == True:   #runs user's shot when these variables are turned True (they are turned true based on the built in key functions below)
            app.ball.shootBallPhy(1, app.ball.shotLocX, app.ball.defLocX)
            app.ball.bounceBackboard()
        
        if app.ball.dribble == False and app.ball.free == True and app.ball.shoot == False:     #run free bounce animation whenever these variables are changed
            if app.ball.tmpdir == 1:
                app.ball.freeBounce(+1)
            elif app.ball.tmpdir == -1:
                app.ball.freeBounce(-1)
            else:
                app.ball.freeBounce(0)
        else:       #else ball is being dribbled
            if app.ball.possession == +1:  #user is dribbling
                app.ball.ballPhy(0, +1)
            elif app.ball.possession == -1: #comp is dribbling 
                app.ball.ballPhy(0, -1)
            else:   
                app.ball.ballPhy(0, 0)
        
        if app.ball.scoreIUser >= 15 or app.ball.scoreIComp >= 15: #reset point whenver either score index is greater than arbirtrary 15 allowing game to wait a few moments before game is reset
            resetAfterPoint(app, app.ball.scorer, app.ball.scoreUser, app.ball.scoreComp)
            app.ball.scoreIUser, app.ball.scoreIComp = 0, 0 #reset score index
            app.ball.goal = False   
            app.ball.missed = False

def resetAfterPoint(app, player, userScore, compScore):
    onGameStart(app)
    app.ball.scoreUser = userScore  #update scores
    app.ball.scoreComp = compScore  #update scores
    app.ball.free = True        #let ball free so that the reset will move ball to the player who last scored
    app.ball.dribble = False    #stop ball dribbling so that the reset can move ball from the default dribbling-user player to player who last scored
    
    if player == 1:             #if player 1 (user) scored, ball will go to player 1
        app.ball.x = app.user.x
        app.ball.shotLocX = 0       #reset shot loc
    elif player == -1:          #if comp scored, ball will go to comp
        app.ball.x = app.comp.x
        app.ball.shotLocX = 1280    #reset shot loc
    app.ball.forceShotLoc = 1280    #reset shot loc

def game_onKeyHold(app, keys):
    if keys == ["right"] and app.user.cantGoRight == False:     
        if app.counter % 5 == 0:
            app.user.userSpriteI = (app.user.userSpriteI + 1) % 2       #flip frame of user while dribbling
        app.user.movePlayer(+1)     #move right
        if app.ball.dribble == True and app.ball.possession == +1:
            app.ball.ballPhy(+1, +1)    #dribbling animation
    elif keys == ["left"] and app.user.cantGoLeft == False:
        if app.counter % 5 == 0:
            app.user.userSpriteI = (app.user.userSpriteI + 1) % 2        #flip frame of user while dribbling
        app.user.movePlayer(-1)     #move left
        if app.ball.dribble == True and app.ball.possession == +1:
            app.ball.ballPhy(-1, +1)    #dribbling animation
    elif keys == ["s"] and app.ball.free == False and app.ball.possession == +1:# and app.ball.dribble == True:
        app.ball.dribble = False
        app.ball.tmpdir = 1     #direction of ball will bounce to right when free bouncing after ball lands on the ground
        if app.ball.shotLocX <= 980:
            app.ball.dy += 1.2      #charge up power to shoot
            app.indicatorBar = abs(int(app.ball.dy * 6)) #speed of indicator bar changes width
            if app.indicatorBar <= 0:
                app.indicatorBar = abs(app.indicatorBar) + 1
            if app.ball.dy > 40:    #max shot power
                app.ball.dy = 40    #max shot power
            if app.indicatorBar >= 250:     #max width of green bar
                app.indicatorBar = 250      #max width of green bar
        
def game_onKeyRelease(app, key):
    if key == "s" and app.ball.shoot == False and app.ball.possession == 1:
        app.ball.y = 580    #reset ball location when shot
        if app.ball.x >= 980 and app.ball.possession == 1:
            app.ball.dy = 5
        app.ball.shoot = True   #change variables to allow shot animation
        app.user.userShoot = True
        app.ball.free = True
        app.ball.dribble = False
        app.ball.possession = 0
        app.indicatorBar = 0.01

def game_onKeyPress(app, key):
    if key == "s" and app.ball.free == False and app.ball.shoot == False:
        app.ball.dy = 5   #resets ball.dy to 5 every time user starts shooting so it doesn't depend on the ball bounce's dy
        app.ball.shotLocX = app.ball.x  #determine shot location when ball is shot initially as player presses shoot
        app.ball.defLocX = app.comp.x   #determine defender location when ball is shot initially as player presses shoot
        app.ball.chargeUp = True
        app.indicatorBar = 10
        
    elif key == "d" and app.ball.dribble == True and app.ball.possession == 1:  #dribbling past animation for user
        userDribProb = random.random()
        if userDribProb < app.user.dribbling * 0.01:    #probability of dribbling past depends on attributes and randomness
            dribblePast(app, 1)
    elif key == "c"  and app.ball.free == False and app.ball.shoot == False and app.ball.chargeUp == False:    #stealing ball animation for user
        userStealProb = random.random()
        if userStealProb < app.user.steal * 0.01:   #probability of stealing depends on attributes and randomness
            app.ball.steal(1, app)
    elif key == "i":        #pausing game 
        app.game.gamePaused = not app.game.gamePaused   #oscillating pause variable
    elif key == "escape":   #leave game back to menu (wont save)
        setActiveScreen("menu")
        
def outOfBound(app, lastTouch, userScore, compScore):   #reset the players' position and ball's postion to the opposite player while keeping the same scores for both players
    resetAfterPoint(app, lastTouch, userScore, compScore)   
    app.ball.outOfBound = True

def dribblePast(app, player):
    if app.comp.collide == True:    #when players collide 
        if player == 1 and app.ball.possession == 1:    #if dribblePast function run by user then change location
            if app.user.x > app.comp.x:     #if user is on the right of comp
                app.user.x -= 110   #user "teleports" to the left
                app.ball.x = app.user.x #ball follows user
            elif app.user.x < app.comp.x:   #if user is on the left of comp
                app.user.x += 110   #user "teleports" to the right
                app.ball.x = app.user.x     #ball follows user
        elif player == -1 and app.ball.possession == -1:    #if dribblePast function run by comp then change location (same for comp but ball folows comp)
            if app.comp.x > app.user.x:
                app.comp.x -= 110
                app.ball.x = app.comp.x 
            elif app.comp.x < app.user.x:
                app.comp.x += 110 
                app.ball.x = app.comp.x 
        app.message = "nice move"   #message for dribbling past opposing player

    
def distance(x0, y0, x1, y1):
    return ((x1 - x0)**2 + (y1 - y0)**2)**0.5


runAppWithScreens(initialScreen="menu", height=720, width = 1280)

#Image Citations:
"""
basketball - https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.freeiconspng.com%2Fimages%2Fbasketball-png&psig=AOvVaw0iFEpIK97gntQgheX3pbPy&ust=1681851455344000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCNi08Irnsf4CFQAAAAAdAAAAABAD
stick figure - https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.clker.com%2Fclipart-boy-stick-figure.html&psig=AOvVaw1h5yAj_pWHbckyXGgs1b8b&ust=1681851522003000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCJjsyKbnsf4CFQAAAAAdAAAAABAD
basketball court - https://www.google.com/url?sa=i&url=https%3A%2F%2Fwallpapers.com%2Fpicture%2Fbasketball-court-pictures-so9uos00f5wbt0m4.html&psig=AOvVaw1PE062ivxGNCSaIqH_fw5w&ust=1681851542388000&source=images&cd=vfe&ved=0CBAQjRxqFwoTCOiv7bDnsf4CFQAAAAAdAAAAABAD
westbrook.png - https://www.previewsworld.com/SiteImage/MainImage/STL109222
james.png - https://funko.com/dw/image/v2/BGTS_PRD/on/demandware.static/-/Sites-funko-master-catalog/default/dw9ad54f44/images/funko/46549-1.png?sw=800&sh=800
durant.png - https://funko.com/dw/image/v2/BGTS_PRD/on/demandware.static/-/Sites-funko-master-catalog/default/dw28e2884d/images/funko/51014-1.png?sw=800&sh=800
curry.png - https://i5.walmartimages.com/asr/332d644a-99a4-4fa7-83f8-c338158c3133.15ab560288ec0a6ff89ed3c7782c63bb.png
harden.png - https://cdn10.bigcommerce.com/s-8v6b4hr6ku/products/8783/images/26722/2__11679.1645295785.1280.1280.png?c=2
leonard.png - https://s1.thcdn.com/productimg/960/960/12514970-1684788367004331.jpg
"""