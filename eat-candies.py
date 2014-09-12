#!/usr/bin/python

#
# Version 1.0
# Creator: AJ
# Email: fei.yang.jen@gmail.com
#

import sys
import pygame
import random
import time

from math import floor
from math import ceil
from pygame.locals import *

# Init
pygame.init()
mainClock = pygame.time.Clock()

# Window
W_WIDTH = 500
W_HEIGHT = 400
windowSurface = pygame.display.set_mode((W_WIDTH, W_HEIGHT), 0, 32)
pygame.display.set_caption('Eat Me All')

# Set up movement variables
FOLLOWSPEED = 15
MOVESPEED = 10
FALLSPEED = 4

# Colors
BLACK = (0,0,0)
GREEN = (0, 255, 0)
WHITE = (255,255,255)

# Set up block info
MODNEWBLOCK = pygame.USEREVENT
blockCounter = 0
blockSize = 20
newBlock = 25 

# Images
BRICK = pygame.USEREVENT+1
HEART = pygame.USEREVENT+2
""" player """
playerImg = pygame.image.load('player.png')
n_p_img = pygame.transform.scale(playerImg, (60, 50))
i_img = pygame.transform.scale(playerImg, (30,20))
""" Player with vaccum """
effect_vac_Img = pygame.image.load('player_vac.png')
e_v_img = pygame.transform.scale(effect_vac_Img, (60, 50))
""" PLayer with nitro boots """
effect_boost_Img = pygame.image.load('player_boost.png')
e_b_img = pygame.transform.scale(effect_boost_Img, (60, 50))
""" Candy """
blockImage = pygame.image.load('Candy.png')
b_img = pygame.transform.scale(blockImage, (blockSize, blockSize))
end_img2 = pygame.transform.scale(blockImage, (80,80))
""" Vaccum Cleaner """
vacuumImg = pygame.image.load('vacuum.png')
v_img = pygame.transform.scale(vacuumImg, (blockSize+5, blockSize+5))
""" Nitro boots """
moveboostImg = pygame.image.load("boots.png")
m_img = pygame.transform.scale(moveboostImg, (blockSize+5, blockSize+5))
""" Brick """
brickImg = pygame.image.load('brick.jpeg')
brick_img = pygame.transform.scale(brickImg, (blockSize+5,blockSize+5))
""" Heart """
heartImg = pygame.image.load('heart.png')
h_img = pygame.transform.scale(heartImg,(blockSize,blockSize))
""" Grass """
grassImg = pygame.image.load('grass.png')
g_img = pygame.transform.scale(grassImg,(W_WIDTH-60,50))
""" Arrow Keys """
arrowImg = pygame.image.load('arrow_key.png')
a_img = pygame.transform.scale(arrowImg, (40, 30))
""" End Game Img"""
endImg = pygame.image.load('let_me_eat.png')
end_img1 = pygame.transform.scale(endImg, (120,100))

# Set font
font = pygame.font.SysFont(None, 48)
fontScore = pygame.font.SysFont(None, 25)
fontFinal = pygame.font.SysFont(None, 35)
fontInstruct = pygame.font.SysFont(None, 20)

# Musics
pickUpSound = pygame.mixer.Sound('pickup.wav')
pickUpSound.set_volume(0.05)
uhohSound = pygame.mixer.Sound('uh_oh.wav')
uhohSound.set_volume(1.0)
loveyouSouond = pygame.mixer.Sound("love_you.wav")
loveyouSouond.set_volume(1.0)
pygame.mixer.music.load('background.wav')
pygame.mixer.music.set_volume(0.08)

# Special candaies
VACUM_BLOCK = pygame.USEREVENT+3
BOOST_BLOCK = pygame.USEREVENT+4
VACUM_SCORE = 100
BOOST_SCORE = 100
REG_SCORE = 10
cur_Effect = {"Effect": None, "time": 0}
EFFECTTIME = 8
VACUM = False
ORIMOVESPEED = MOVESPEED
MOVEMENTBOOST = ORIMOVESPEED * 1.3


# Set up timer for repeated events
pygame.time.set_timer(MODNEWBLOCK, 25000)
pygame.time.set_timer(VACUM_BLOCK, 13100)
pygame.time.set_timer(BOOST_BLOCK, 23050)	
pygame.time.set_timer(BRICK,1000)
pygame.time.set_timer(HEART,40000)



def read_score(scoreFile):
	try:
		with open(scoreFile, "r") as f:
			cur_max_score = int(f.readline().strip())
		return cur_max_score
	except IOError:
		print "no such file, return 0"
		return 0


def terminate(scoreFile,maxScore):
	try:
		with open(scoreFile, "r+") as f:
			cur_max_score = read_score(scoreFile)
			if maxScore > cur_max_score:
				f.write(str(maxScore))
	except IOError:
		with open(scoreFile, "w") as f:
			f.write(str(maxScore))
	pygame.quit()
	sys.exit()

"""
Create new block:
	* Arg: need a string for block type
		- REG: a regular block. It can accumulate power.
		- HEART: It will give you a heart:)
		- VACUM: It will suck all the candy
		- BOMB: a bomb block. It will explode. Need to be defused.
		- MOVEMENTBOOST : increase movement speed
"""
def create_block(b_type, b_x=False, b_y=False, status="FALL", width=blockSize, height=blockSize):
	if b_x == False and b_y == False:
		return {'rect': pygame.Rect(random.randint(10, W_WIDTH - blockSize), 0, width, height),
				'type': b_type,
				'status': status }
	else:
		return {'rect': pygame.Rect(b_x, b_y, width, height),					
				'type': b_type,
				'status': status }
	

def follow(block, playerObj):
	if block.centerx < playerObj.centerx:
		if block.centery <= playerObj.centery:
			block.centerx += ceil((playerObj.centerx - block.centerx)/FOLLOWSPEED)
			block.centery += ceil((playerObj.centery - block.centery)/FOLLOWSPEED)
		else:
			#print "****", block.centerx, block.centery, playerObj.centerx, playerObj.centery
			block.centerx += ceil((playerObj.centerx - block.centerx)/FOLLOWSPEED)+1
			#print "****", ceil((block.centery - playerObj.centery)/FOLLOWSPEED)+1
			block.centery -= ceil((block.centery - playerObj.centery)/FOLLOWSPEED)+1
			#print "****", block.centery
	else:
		if block.centery <= playerObj.centery:
			block.centerx -= ceil((block.centerx - playerObj.centerx)/FOLLOWSPEED)
			block.centery += ceil((playerObj.centery - block.centery)/FOLLOWSPEED)
		else:
			#print "====", block.centerx, block.centery, playerObj.centerx, playerObj.centery
			block.centerx -= ceil((block.centerx - playerObj.centerx)/FOLLOWSPEED)+1
			block.centery -= ceil((block.centery - playerObj.centery)/FOLLOWSPEED)+1



def check_special_candies(accumulator):
	global VACUM
	global MOVESPEED
	global ORIMOVESPEED
	if accumulator['Effect'] == None:
		pass
	elif floor(pygame.time.get_ticks()/1000) > accumulator['time']:
		if accumulator['Effect'] == "VACUM":
			VACUM = False
		elif accumulator['Effect'] == "MOVEMENTBOOST":
			MOVESPEED = ORIMOVESPEED
		accumulator['Effect'] = None
		accumulator['time'] = 0

# only one effect can exist at a time
def replace_effect_if_exits(accumulator):
	global VACUM
	global MOVESPEED
	global ORIMOVESPEED
	if accumulator['Effect'] == None:
		pass
	else:
		if accumulator['Effect'] == "VACUM":
			VACUM = False
		elif accumulator['Effect'] == "MOVEMENTBOOST":
			MOVESPEED = ORIMOVESPEED
		accumulator['Effect'] = None
		accumulator['time'] = 0

def wait_for_reply(scoreFile, maxScore):
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(scoreFile, maxScore)
			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					terminate(scoreFile, maxScore)
				elif event.key == K_RETURN:
					return

def drawText(text, font, surface, x ,y):
	textObj = font.render(text,1,WHITE)
	textrect = textObj.get_rect()
	textrect.topleft = (x,y)
	surface.blit(textObj, textrect)


def print_instruction():
	grass_icon = pygame.Rect(28, (W_HEIGHT/4)-15, W_WIDTH-60, 50)
	windowSurface.blit(g_img, grass_icon)
	arrowkey_icon = pygame.Rect((W_WIDTH/4)-55, (W_HEIGHT/2)-53, 40, 30)
	windowSurface.blit(a_img, arrowkey_icon)
	drawText(":  Use arrow keys to control your minion", fontInstruct, windowSurface, (W_WIDTH/4)-9, (W_HEIGHT/2)-40)
	candy_icon = pygame.Rect((W_WIDTH/4) - 43, (W_HEIGHT/2)-10, blockSize, blockSize)
	windowSurface.blit(b_img, candy_icon)
	drawText(":  When you see candies, go nuts! Eat them all", fontInstruct, windowSurface, (W_WIDTH/4)-9, (W_HEIGHT/2)-7)
	brick_icon = pygame.Rect((W_WIDTH/4) - 43, (W_HEIGHT/2)+30, blockSize, blockSize)
	windowSurface.blit(brick_img, brick_icon)
	drawText(":  Opps! You have to dodge me", fontInstruct, windowSurface, (W_WIDTH/4)-7, (W_HEIGHT/2)+35)
	heart_icon = pygame.Rect((W_WIDTH/4) - 43, (W_HEIGHT/2)+70, blockSize, blockSize)
	windowSurface.blit(h_img, heart_icon)
	drawText(":  I am the heart! I can revive you", fontInstruct, windowSurface, (W_WIDTH/4)-7, (W_HEIGHT/2)+72)
	vacum_icon = pygame.Rect((W_WIDTH/4) - 43, (W_HEIGHT/2)+110, blockSize, blockSize)
	windowSurface.blit(v_img, vacum_icon)
	drawText(":  I am a vaccum cleaner. I love candies. Num Num Num", fontInstruct, windowSurface, (W_WIDTH/4)-7, (W_HEIGHT/2)+114)
	boost_icon = pygame.Rect((W_WIDTH/4) - 43, (W_HEIGHT/2)+150, blockSize, blockSize)
	windowSurface.blit(m_img, boost_icon)
	drawText(":  I am nitro boots. I grant you mobility", fontInstruct, windowSurface, (W_WIDTH/4)-6, (W_HEIGHT/2)+155)


# High score file
FILE = ".score"
topScore = read_score(FILE)


# Load the Screen
drawText('Eat All the Candy ', font, windowSurface, (W_WIDTH / 4) - 25, (W_HEIGHT / 3)-110)
drawText('Press Enter key to start.', font, windowSurface, (W_WIDTH / 4) - 65, (W_HEIGHT / 3)-65)
print_instruction()
pygame.display.update()
wait_for_reply(FILE, topScore)


while True:

	# Add player and initial block. Game is starting!!!
	pygame.mixer.music.play(-1, 0.0)
	life = []
	for i in range(3):
		life_x = (i*25)+10
		life.append(create_block("REG", b_x=life_x, b_y=45, width=20, height=20))
	blocks = []
	blocks.append(create_block("REG"))
	player = pygame.Rect((W_WIDTH-60)/2,W_HEIGHT - 52,60,50)
	score = 0
	LIVES = 3
	newBlock = 25 
	moveLeft = False
	moveRight = False
	moveUp = False
	moveDown = False
	cur_Effect = {"Effect": None, "time": 0}
	VACUM = False
	MOVESPEED = 10
	ORIMOVESPEED = MOVESPEED
	MOVEMENTBOOST = ORIMOVESPEED * 1.5

	# Game loop
	while True:
		
		check_special_candies(cur_Effect)
		score += 1

		for event in pygame.event.get():
			if event.type == QUIT:
				terminate(FILE, topScore)
			elif event.type == KEYDOWN:
				if event.key == K_LEFT or event.key == ord('a'):
						moveLeft = True
				elif event.key == K_RIGHT or event.key == ord('d'):
					moveRight = True
				elif event.key == K_UP or event.key == ord('w'):
					moveUp = True	
				elif event.key == K_DOWN or event.key == ord('s'):
					moveDown = True
			elif event.type == KEYUP:
				if event.key == K_ESCAPE:
					terminate(FILE, topScore)
				elif event.key == K_LEFT or event.key == ord('a'):
					moveLeft = False
				elif event.key == K_RIGHT or event.key == ord('d'):
					moveRight = False
				elif event.key == K_UP or event.key == ord('w'):
					moveUp = False	
				elif event.key == K_DOWN or event.key == ord('s'):
					moveDown = False
				elif event.key == ord('t'):
					player.left = random.randint(0, W_WIDTH - blockSize)
					player.top = random.randint(0, W_HEIGHT - blockSize)
				elif event.key == ord('m'):
					MOVESPEED += 1
				elif event.key == ord('n'):
					MOVESPEED -= 1
			elif event.type == MOUSEBUTTONUP:
				if VACUM:
					blocks.append(create_block("REG", b_x=event.pos[0], b_y=event.pos[1], status="VACUM"))
				else:
					blocks.append(create_block("REG", b_x=event.pos[0], b_y=event.pos[1]))
			elif event.type == VACUM_BLOCK:
				blocks.append(create_block("VACUM"))
			elif event.type == BOOST_BLOCK:
				blocks.append(create_block("MOVEMENTBOOST"))
			elif event.type == BRICK:
				blocks.append(create_block("BRICK"))
			elif event.type == HEART:
				blocks.append(create_block("HEART"))
			elif event.type == MODNEWBLOCK:
				if newBlock >= 21:
					newBlock -= 4

		# Add a new block
		blockCounter += 1
		if blockCounter >= newBlock:
			blockCounter = 0
			if VACUM:
				blocks.append(create_block("REG", status="VACUM"))
			else:
				blocks.append(create_block("REG"))

		windowSurface.fill(BLACK)

		# Move the player. Use all 'if' cases to simulate multi directions.
		if moveLeft and player.left > 0:
			if player.left - MOVESPEED > 0:
				player.left -= MOVESPEED
			else:
				player.left = 0
		if moveRight and player.right < W_WIDTH:
			if player.right + MOVESPEED < W_WIDTH:
				player.right += MOVESPEED
			else:
				player.right = W_WIDTH
		if moveUp and player.top > 0:
			if player.top - MOVESPEED > 0:
				player.top -= MOVESPEED
			else:
				player.top = 0
		if moveDown and player.bottom < W_HEIGHT:
			if player.bottom + MOVESPEED < W_HEIGHT:
				player.bottom += MOVESPEED
			else:
				player.bottom = W_HEIGHT

		# Update every block
		for b in blocks[:]:
			# Check collision
			if player.colliderect(b['rect']):
				# Check to see if the player eats a special candy
				if b['type'] == "VACUM":
					score += VACUM_SCORE
					replace_effect_if_exits(cur_Effect)
					VACUM = True
					cur_Effect['Effect'] = "VACUM"
					cur_Effect['time'] = floor(pygame.time.get_ticks()/1000)+EFFECTTIME
					pickUpSound.play()
				elif b['type'] == "MOVEMENTBOOST":
					score += BOOST_SCORE
					replace_effect_if_exits(cur_Effect)
					MOVESPEED = MOVEMENTBOOST
					cur_Effect['Effect'] = "MOVEMENTBOOST"
					cur_Effect['time'] = floor(pygame.time.get_ticks()/1000)+EFFECTTIME
					pickUpSound.play()
				elif b['type'] == "BRICK":
					LIVES -= 1
					life.pop()
					uhohSound.play()
				elif b['type'] == "HEART":
					if LIVES < 5:
						LIVES += 1
						life_x = (len(life)*25)+10
						life.append(create_block("REG", b_x=life_x, b_y=45, width=20, height=20))
						loveyouSouond.play()
					else:
						score += 1000
				else:
					score += REG_SCORE
					pickUpSound.play()
				blocks.remove(b)
			elif b['status'] == "VACUM":
				follow(b['rect'],player)
				# Check collision after moving
				if player.colliderect(b['rect']):
					blocks.remove(b)
					pickUpSound.play()
			else:
				if VACUM and b['type'] == "REG":
					b['status'] = "VACUM"
					follow(b['rect'],player)
					# Check collision after moving
					if player.colliderect(b['rect']):
						blocks.remove(b)
						pickUpSound.play()
				else:
					b['rect'].top += FALLSPEED
					if b['rect'].top >= W_HEIGHT:
						blocks.remove(b)

		# Apply img to player
		if cur_Effect['Effect'] == None:
			windowSurface.blit(n_p_img, player)
		elif cur_Effect['Effect'] == "VACUM":
			windowSurface.blit(e_v_img, player)
		elif cur_Effect['Effect'] == "MOVEMENTBOOST":
			windowSurface.blit(e_b_img, player)
		
		# Apply img to blocks
		for b in blocks:
			if b['type'] == "VACUM":
				windowSurface.blit(v_img, b['rect'])
			elif b['type'] == "MOVEMENTBOOST":
				windowSurface.blit(m_img, b['rect'])
			elif b['type'] == "BRICK":
				windowSurface.blit(brick_img, b['rect'])
			elif b['type'] == "HEART":
				windowSurface.blit(h_img, b['rect'])
			else:
				windowSurface.blit(b_img, b['rect'])

		# Print life icon
		for b in life:
			windowSurface.blit(i_img, b['rect'])

		drawText('Score: %s' % (score), fontScore, windowSurface, 10, 5)
		drawText('Top Score: %s' % (topScore), fontScore, windowSurface, 10, 25)

		# Check	is Game Over
		if LIVES == 0:
			if score > topScore:
				topScore = score
			break	

		pygame.display.update()
		mainClock.tick(40)

	pygame.mixer.music.stop()
	windowSurface.fill(BLACK)
	drawText('Opps! Try again', font, windowSurface, (W_WIDTH / 8)+10, (W_HEIGHT / 4)-50)
	drawText('Press Enter key to restart', font, windowSurface, (W_WIDTH / 10) , (W_HEIGHT / 4))
	grass_icon = pygame.Rect(28, (W_HEIGHT/3)-20, W_WIDTH-60, 50)
	windowSurface.blit(g_img, grass_icon)
	drawText('Your Score: %s' % (score), fontFinal, windowSurface, (W_WIDTH/3) - 20, (W_HEIGHT/2)-10)
	drawText('Top Score: %s' % (topScore), fontFinal, windowSurface, (W_WIDTH/3) - 20, (W_HEIGHT/2)+30)
	end_icon1 = pygame.Rect(W_WIDTH-150, W_HEIGHT-120, 120, 100)
	windowSurface.blit(end_img1,end_icon1)
	end_icon2 = pygame.Rect(30, W_HEIGHT-100, 80, 80)
	windowSurface.blit(end_img2,end_icon2)
	pygame.display.update()
	wait_for_reply(FILE, topScore)


