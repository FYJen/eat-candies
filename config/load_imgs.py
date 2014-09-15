import pygame

from default_config import *

# Safe way to load pygame models.
pygame.init()

# Load normal player images.
playerImg = pygame.image.load('img/player.png')
normalPlayerImg = pygame.transform.scale(playerImg, (60, 50))
lifeIcon = pygame.transform.scale(playerImg, (30,20))

# Load player image with vacuum effect.
playerVaccumImg = pygame.transform.scale(pygame.image.load('img/player_vac.png'),
                                         (60, 50))

# Load player image with nitro boots effect.
playerBootsImg = pygame.transform.scale(pygame.image.load('img/player_boost.png'),
                                        (60, 50))

# Load candy images.
candyImg = pygame.image.load('img/Candy.png')
normalCandyImg = pygame.transform.scale(candyImg, (blockSize, blockSize))
endingCandyImg = pygame.transform.scale(candyImg, (80, 80))

# Load vacuum cleaner image.
vacuumImg = pygame.image.load('img/vacuum.png')
normalVacuumImg = pygame.transform.scale(vacuumImg, (blockSize + 5, blockSize + 5))

# Load nitro boots image.
moveboostImg = pygame.image.load("img/boots.png")
normalMoveBoostImg = pygame.transform.scale(moveboostImg,
                                            (blockSize + 5, blockSize + 5))

# Load brick image.
brickImg = pygame.transform.scale(pygame.image.load('img/brick.jpeg'),
                                  (blockSize + 5, blockSize + 5))

# Load heart image.
heartImg = pygame.transform.scale(pygame.image.load('img/heart.png'),
                                  (blockSize, blockSize))

# Load grass image.
grassImg = pygame.transform.scale(pygame.image.load('img/grass.png'),
                                  (W_WIDTH - 60, 50))

# Load arrow keys image.
arrowImg = pygame.transform.scale(pygame.image.load('img/arrow_key.png'),
                                  (40, 30))

# Load player image for the ending scene.
endingPlayerImg = pygame.transform.scale(pygame.image.load('img/let_me_eat.png'),
                                         (120, 100))
