from numpy.core.numeric import array_equal
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

# image of the player that will be in the screen
playerImage = pygame.image.load("spaceship.png")

# initial positions of the player
playerX, playerY = 370, 480
playerDx = [0, 0, 0]    # for the 3 levels

velocities = [1, 1, 1.5]
enemies_velocities = [0.3, 0.6, 1]

# bullet
bulletImage = pygame.image.load("bullet.png")
bulletX, bulletY = 0, playerY 
bulletDx, bulletDy = 0, 1
bulletState = "ready"            # to keep the state of the bullet to be shoot

# enemy lists
enemyImage = []
enemyX, enemyY = [], []
enemyDx, enemyDy = [], []
numEnemies = [8, 10, 15]             # 10 enemies will be created

def resetEnemies():
	global enemyImage, enemyX, enemyY, enemyDx, enemyDy, scoreValue
	enemyImage = []
	enemyX, enemyY = [], []
	enemyDx, enemyDy = [], []

def resetPlayer():
	global playerX, playerY, playerDx
	playerX, playerY = 370, 480
	playerDx = [0, 0, 0]   


skullEasiestImage = pygame.image.load("skull_easiest.png")
skullMediumImage = pygame.image.load("skull_medium.png")
skullHarderImage = pygame.image.load("skull_harder.png")

def enemiesCreationByLevel(level:int):
	heights = [height/3, height/3, height/2]
	if level==0:  #level 1
		enemiesCreation(level, skullEasiestImage, heights[0], 0.3)
	elif level==1:
		enemiesCreation(level, skullMediumImage, heights[1], 0.6)
	elif level==2:	
		enemiesCreation(level, skullHarderImage, heights[2], 1)
	return heights[level]

def enemiesCreation(level:int, skullImg, heightFrac, velocity):
	for i in range(numEnemies[level]):
		enemyImage.append(skullImg)
		enemyX.append(random.randint(0, width-64))
		enemyY.append(random.randint(50, heightFrac))
		enemyDx.append(velocity)   # 0.3 is the velocity
		enemyDy.append(30)

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
	window.blit(gameOver, (160, 250))

def finalWinText()->None:
	finalWinFont = pygame.font.Font("SuperMario256.ttf", 50)
	finalWin = finalWinFont.render("YOU WON THE GAME!", True, (255, 255, 255))
	window.blit(finalWin, (100, 250))	

def winnerText()->None:
	winnerFont = pygame.font.Font("SuperMario256.ttf", 50)
	winner = winnerFont.render("YOU WON THE LEVEL!", True, (255, 255, 255))
	window.blit(winner, (100, 250))	

def nextLevelText()->None:
	nextLevelFont = pygame.font.Font("SuperMario256.ttf", 30)
	nextLevel = nextLevelFont.render("Wanna go to the next level?", True, (255, 255, 255))
	nextLevelOptions = nextLevelFont.render("Press y if true, n to exit.", True, (255, 255,255))
	window.blit(nextLevel, (80, 350))	
	window.blit(nextLevelOptions, (100, 400))
	
def playAgainText()->None:
	playAgainFont = pygame.font.Font("SuperMario256.ttf", 30)
	playAgain = playAgainFont.render("Wanna play again?", True, (255, 255, 255))
	playAgainOptions = playAgainFont.render("Press y if true, n to exit.", True, (255, 255,255))
	window.blit(playAgain, (80, 350))	
	window.blit(playAgainOptions, (100, 400))

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
level = 0 
running = True
while running:
	window.fill((0, 0, 0))		      # change the color of the background
	#window.blit(backgroundImage, (0,0))    # adds the background to all the window

	level1BtnPressed = level1Btn.draw(window)
	exitBtnPressed = exitBtn.draw(window)

	for event in pygame.event.get():          # pygame.event.get():  captures all the events ocurring
		if event.type == pygame.QUIT:        # if an event is close the window
			running = False

	pygame.display.update()

	scoreValue = 0
	music = False
	playOnce = False

	# enemies creation
	enemies_height = enemiesCreationByLevel(level)

	# level 1 events
	while level1BtnPressed:   # the level 1 button was pressed
		#print('Level1')
		if music==False:   # hacerla funcion !
			mixer.music.load("background.wav")
			mixer.music.play(-1)          # -1 to play on loop
			music = True

		window.fill((0, 0, 0))

		for event in pygame.event.get():          # pygame.event.get():  captures all the events ocurring

			if event.type == pygame.QUIT:        # if an event is close the window
				level1BtnPressed = False
				running = False

			if event.type == pygame.KEYDOWN:      # if any key is pressed
				if event.key == pygame.K_LEFT:
					playerDx[level] = -1 * velocities[level]
					print("left arrow is pressed")
				if event.key == pygame.K_RIGHT:	
					playerDx[level] = velocities[level]
					print("right arrow is pressed")
				if event.key == pygame.K_SPACE:
					if bulletState == "ready":
						bulletX = playerX
						fireBullet(bulletX, bulletY)
						mixer.Sound("laser.wav").play()	

			if event.type == pygame.KEYUP:                                       # to release the keystroke
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					playerDx[level] = 0
					print("keystroke has been released")

		# players boundary conditions and movement		
		if playerX <= 0:
			playerX = 0
		elif playerX >= width-64:    # 64 pixel = large and height of spacecraft
			playerX = width-64

		playerX += playerDx[level]	

		# enemies boundary conditions and movement
		for i in range(numEnemies[level]):
			# is GAME OVER if the enemy y pos is the same as the player
			if enemyY[i] > 440:   
				for j in range(numEnemies[level]):
					enemyY[j] = 2000
				
				gameOverText()
				playAgainText()

				mixer.music.stop()   # to stop the bkg music
				if playOnce==False:	
					mixer.Sound("game-over.wav").play()
					playOnce=True	
				
				for event in pygame.event.get():
					if event.type == pygame.QUIT: 
						level1BtnPressed = False
						running = False

					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_y:
							level1BtnPressed=False# resetear todo    
							
						elif event.key == pygame.K_n:
							running = False
							level1BtnPressed = False
					
				break

			if enemyX[i] <= 0:
				enemyDx[i] = enemies_velocities[level]
				enemyY[i] += enemyDy[i] 
			elif enemyX[i] >= width-64:
				enemyDx[i] = -1* enemies_velocities[level]
				enemyY[i] += enemyDy[i] 

			enemyX[i] += enemyDx[i]	

			# collision	
			if hasCollided(enemyX[i], enemyY[i], bulletX, bulletY):
				bulletInitialState()
				scoreValue += 1
				enemyX[i], enemyY[i] = random.randint(0, width-64), enemies_height   # one enemy per collision appears in a random position again
				mixer.Sound("explosion.wav").play()
				
			enemy(enemyX[i], enemyY[i], i)
		

		# bullet boundary conditions and movement  
		if bulletState == "fire":
			#window.blit(bulletImage, (bulletX+16, bulletY-10))
			fireBullet(bulletX, bulletY)
			bulletY -= bulletDy

		if bulletY <= 0:
			bulletInitialState()

		# to finish the level (win):
		if scoreValue==2:
			for j in range(numEnemies[level]):
				enemyY[j] = -2000
			playerY=-2000

			mixer.music.stop()   # to stop the bkg music

			if level==2 and enemies_height == height/2:  # the final level
				finalWinText()   # no se me muestra o se visualiza en otro level
				playAgainText()
				#level = 0    # resets the level
				if playOnce==False:	
					mixer.Sound("game-win.wav").play()
					playOnce=True	

			else: 
				winnerText()
				nextLevelText()
				if playOnce==False:	
					mixer.Sound("level-completed.wav").play()
					level+=1   # inside playOnce if to upgrade the level just once
					playOnce=True	

			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					level1BtnPressed = False
					running = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_y:
						# PASAR AL SIGUIENTE NIVEL
						resetEnemies()
						resetPlayer()
						level1BtnPressed=False     
						
					elif event.key == pygame.K_n:
						running = False
						level1BtnPressed = False


		player(playerX, playerY)                  # the player is drawn
		showScore(textX, textY)
		pygame.display.update()                   # update the screen


	if exitBtnPressed:   # the exit button was pressed
		print('Exit')
		running = False

pygame.quit()


# for more fonts go to: dafont.com
# images taken from: flaticon.com 
# .wavs taken from: mixkit.co
