import pygame

# Safe way to load pygame models.
pygame.init()

# Set up events for different items.
MODNEW_BLOCK = pygame.USEREVENT
BRICK_BLOCK = pygame.USEREVENT + 1
HEART_BLOCK = pygame.USEREVENT + 2
VACUM_BLOCK = pygame.USEREVENT + 3
BOOST_BLOCK = pygame.USEREVENT + 4

# Set up timer for repeated events
pygame.time.set_timer(MODNEW_BLOCK, 25000)
pygame.time.set_timer(VACUM_BLOCK, 13100)
pygame.time.set_timer(BOOST_BLOCK, 23050)
pygame.time.set_timer(BRICK_BLOCK, 1000)
pygame.time.set_timer(HEART_BLOCK, 40000)
