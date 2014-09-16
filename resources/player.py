import pygame
import random
from math import floor

import config.default_config as config
from block import BlockModel

# Safe and easiest way to load all pygame models.
pygame.init()

class PlayerModel(object):
    """Player class.
    """
    def __init__(self):
        """Initialize player's variable.
        """
        #Initialize window and block size.
        self.W_WIDTH = config.W_WIDTH
        self.W_HEIGHT = config.W_HEIGHT
        self.blockSize = config.BLOCKSIZE

        # Initialize player's object.
        self.rect = pygame.Rect((self.W_WIDTH - 60) / 2, self.W_HEIGHT - 52, 60, 50)
        
        # Initialize movement attributes.
        self.moveLeft = False
        self.moveRight = False
        self.moveUp = False
        self.moveDown = False

        # Initialize effect applied onto the player.
        self.currentEffect = None
        self.effectTimeEnd = 0
        self.effectDuration = config.EFFECTDURATION # default is 8 second.
        
        # Initialize movement speeds.
        self.regMovementSpeed = config.MOVESPEED
        self.curMovementSpeed = config.MOVESPEED
        self.boostMovementSpeed = self.regMovementSpeed * 2
        
        # Initialize player's life points.
        self.life = []
        for i in range(config.LIFE):
            life_x = (i * 25) + 10
            self.life.append(BlockModel("LIFE", blockX=life_x, blockY=45, width=20,
                                        height=20))

    def increaseSpeed(self, num):
        """Increase current movement speed.

        Args:
            num - Number of speed to increase.
        """
        self.curMovementSpeed += num

    def decreaseSpeed(self, num):
        """Decrease current movement speed.
        """
        if self.curMovementSpeed > 0:
            self.curMovementSpeed -= num

    def teleport(self):
        """Speicial hotkey that will randomly move player around the screen.
        """
        self.rect.left = random.randint(0, self.W_WIDTH - self.blockSize)
        self.rect.top = random.randint(0, self.W_HEIGHT - self.blockSize)

    def moveToLeft(self):
        """Move the player left.
        """
        self.rect.left = \
            (self.rect.left - self.curMovementSpeed) if \
            (self.rect.left - self.curMovementSpeed) > 0 else 0

    def moveToRight(self):
        """Move the player right.
        """
        self.rect.right = \
            (self.rect.right + self.curMovementSpeed) if \
            (self.rect.right + self.curMovementSpeed) < self.W_WIDTH else \
            self.W_WIDTH

    def moveToUp(self):
        """Move the player up
        """
        self.rect.top = \
            (self.rect.top - self.curMovementSpeed) if \
            (self.rect.top - self.curMovementSpeed) > 0 else 0

    def moveToDown(self):
        """Move the player down.
        """
        self.rect.bottom = \
            (self.rect.bottom + self.curMovementSpeed) if \
            (self.rect.bottom + self.curMovementSpeed) < self.W_HEIGHT else \
            self.W_HEIGHT

    def move(self):
        """Decides which way the player should be moving to.
        """
        if self.moveLeft and self.rect.left > 0:
            self.moveToLeft()

        if self.moveRight and self.rect.right < self.W_WIDTH:
            self.moveToRight()

        if self.moveUp and self.rect.top > 0:
            self.moveToUp()

        if self.moveDown and self.rect.bottom < self.W_HEIGHT:
            self.moveToDown()

    def loseLife(self):
        """Gets hit by the brick, player loses a life point.
        """
        self.life.pop()

    def addLife(self):
        """Gains a life point.
        """
        life_x = (len(self.life) * 25) + 10
        self.life.append(BlockModel("LIFE", blockX=life_x, blockY=45, width=20,
                                    height=20))

    def checkEffect(self, EnvModle):
        """Checks if the effect applied to the player has expired.

        Args:
            EnvModle - The EnvModle object.
        """
        if self.currentEffect and \
                floor(pygame.time.get_ticks() / 1000) > self.effectTimeEnd:
            self.resetEffect(EnvModle)

    def resetEffect(self, EnvModle):
        """Reverts the effect applied to the player.

        Args:
            EnvModle - The EnvModle object.
        """
        self.currentEffect = None
        self.effectTimeEnd = 0
        self.curMovementSpeed = self.regMovementSpeed
        EnvModle.isVacum = False

    def addEffect(self, effectType, EnvModle):
        """Adds effect to player.

        Args:
            effectType - The name of the effect's name. Currently there are only
                         two effects, including
                            - 'VACUM'
                            - 'MOVEMENTBOOST'
            EnvModle - EnvModle object.
        """
        self.resetEffect(EnvModle)
        self.currentEffect = effectType
        self.effectTimeEnd = floor(pygame.time.get_ticks() / 1000) + \
                             self.effectDuration

        if effectType == 'VACUM':
            EnvModle.isVacum = True

        if effectType == 'MOVEMENTBOOST':
            self.curMovementSpeed = self.boostMovementSpeed
