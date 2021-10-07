import pygame
import random
import math
from pygame import mixer
import button

# initialize pygame 
pygame.init()

# creates the game window  (width = 800, height= 600)
width, height = 800, 600
window = pygame.display.set_mode((width, height))

# title and icon image (32 pixels always)
pygame.display.set_caption("Skull Invaders!") 
icon = pygame.image.load("skull_icon.png")
pygame.display.set_icon(icon)

# add the background image
#backgroundImage = pygame.image.load("background.png")

# add background sound
mixer.music.load("background.wav")
mixer.music.play(-1)          # -1 to play on loop

# image of the player that will be in the screen
playerImage = pygame.image.load("spaceship.png")

# initial positions of the player
playerX, playerY = 370, 480
playerDx = 0

# enemy lists
enemyImage = []
enemyX, enemyY = [], []
enemyDx, enemyDy = [], []
numEnemies = 10              # 10 enemies will be created

for i in range(numEnemies):
	enemyImage.append(pygame.image.load("skull_easiest.png"))
	enemyX.append(random.randint(0, width-64))
	enemyY.append(random.randint(50, height/2))
	enemyDx.append(0.3)
	enemyDy.append(30)

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX, bulletY = 0, playerY 
bulletDx, bulletDy = 0, 1
bulletState = "ready"            # to keep the state of the bullet to be shoot

# keeps the score of the game
scoreValue = 0
font = pygame.font.Font("SuperMario256.ttf", 25)
textX, textY = 10, 10

def showScore(x:int, y:int)->None:
	score = font.render("Score: " + str(scoreValue) + "/20", True, (255, 255, 255))
	window.blit(score, (x, y))

def gameOverText()->None:
	gameOverFont = pygame.font.Font("SuperMario256.ttf", 70)
	gameOver = gameOverFont.render("GAME OVER", True, (255, 255, 255))
	window.blit(gameOver, (180, 250))

# function that creates the player
def player(x:int, y:int)->None:
	window.blit(playerImage, (x, y))       # blit(img, (x,y)):  draws the img in the coordinates (x,y)

# function that creates the enemy
def enemy(x:int, y:int, i:int)->None:
	window.blit(enemyImage[i], (x, y))	

# function that fires a bullet
def fireBullet(x:int, y:int)->None:
	global bulletState
	bulletState = "fire"         # now the state is fire
	window.blit(bulletImage, (x+16, y-10))

# detects a collision between the bullet and the enemy
def hasCollided(enemyX:int, enemyY:int, bulletX:int, bulletY:int)->bool:
	distance = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY-bulletY, 2))
	if distance < 27: collision = True
	else: collision = False	
	return collision

# to reuse code
def bulletInitialState():
	global bulletY, bulletState
	bulletY = 480
	bulletState = "ready"


# images of buttons
btnLevel1Image = pygame.image.load('btn_level1.png')
btnExitImage = pygame.image.load('btn_exit.png')

# button instances
level1Btn = button.Button(350, 200, btnLevel1Image, 0.5)
exitBtn = button.Button(360, 300, btnExitImage, 0.5)


	
# game loop for window not to close (and other events)
running = True
#level1BtnPressed, exitBtnPressed = False, False

while running:
	window.fill((0, 0, 0))		      # change the color of the background
	#window.blit(backgroundImage, (0,0))    # adds the background to all the window

	level1BtnPressed = level1Btn.draw(window)
	exitBtnPressed = exitBtn.draw(window)

	for event in pygame.event.get():          # pygame.event.get():  captures all the events ocurring
		if event.type == pygame.QUIT:        # if an event is close the window
			running = False

	pygame.display.update()

	# level 1 events
	while level1BtnPressed:   # the level 1 button was pressed
		#print('Level1')
		window.fill((0, 0, 0))

		for event in pygame.event.get():          # pygame.event.get():  captures all the events ocurring

			if event.type == pygame.QUIT:        # if an event is close the window
				level1BtnPressed = False
				running = False

			if event.type == pygame.KEYDOWN:      # if any key is pressed
				if event.key == pygame.K_LEFT:
					playerDx = -1
					print("left arrow is pressed")
				if event.key == pygame.K_RIGHT:	
					playerDx = 1
					print("right arrow is pressed")
				if event.key == pygame.K_SPACE:
					if bulletState == "ready":
						bulletX = playerX
						fireBullet(bulletX, bulletY)
						mixer.Sound("laser.wav").play()	

			if event.type == pygame.KEYUP:                                       # to release the keystroke
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					playerDx = 0
					print("keystroke has been released")

		# players boundary conditions and movement		
		if playerX <= 0:
			playerX = 0
		elif playerX >= width-64:    # 64 pixel = large and height of spacecraft
			playerX = width-64

		playerX += playerDx	

		# enemies boundary conditions and movement
		for i in range(numEnemies):
			if enemyY[i] > 440:
				for j in range(numEnemies):
					enemyY[j] = 2000
				gameOverText()
				break

			if enemyX[i] <= 0:
				enemyDx[i] = 0.3
				enemyY[i] += enemyDy[i] 
			elif enemyX[i] >= width-64:
				enemyDx[i] = -0.3
				enemyY[i] += enemyDy[i] 

			enemyX[i] += enemyDx[i]	

			# collision	
			if hasCollided(enemyX[i], enemyY[i], bulletX, bulletY):
				bulletInitialState()
				scoreValue += 1;
				enemyX[i], enemyY[i] = random.randint(0, width-64), random.randint(50, height/3)   # one enemy per collision appears in a random position again
				mixer.Sound("explosion.wav").play()
				
			enemy(enemyX[i], enemyY[i], i)
		

		# bullet boundary conditions and movement  
		if bulletState == "fire":
			#window.blit(bulletImage, (bulletX+16, bulletY-10))
			fireBullet(bulletX, bulletY)
			bulletY -= bulletDy

		if bulletY <= 0:
			bulletInitialState()

		player(playerX, playerY)                  # the player is drawn
		showScore(textX, textY)
		pygame.display.update()                   # update the screen


	if exitBtnPressed:   # the exit button was pressed
		print('Exit')
		running = False

pygame.quit()


# for more fonts go to: dafont.com
# images taken from: flaticon.com 
