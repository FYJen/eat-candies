import pygame

# Safe way to load pygame models.
pygame.init()

# Add sound effect for picking up candies.
pickUpSound = pygame.mixer.Sound('sound/pickup.wav')
pickUpSound.set_volume(0.05)

# Add sound effect for being hit by the bricks.
uhohSound = pygame.mixer.Sound('sound/uh_oh.wav')
uhohSound.set_volume(1.0)

# Add sound effect for picking up extra life (heart).
loveyouSouond = pygame.mixer.Sound("sound/love_you.wav")
loveyouSouond.set_volume(1.0)

# Add back group music.
pygame.mixer.music.load('sound/background.wav')
pygame.mixer.music.set_volume(0.08)
