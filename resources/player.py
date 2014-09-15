import pygame
from math import floor

import config.default_config as config
from block import BlockModel

# Safe and easiest way to load all pygame models.
pygame.init()

class PlayerModle(object):
    """Player class.
    """
    def __init__(self):
        """
        """
        # Initialize player's object.
        self.rect = pygame.Rect((config.W_WIDTH - 60) / 2,
                                 config.W_HEIGHT - 52, 60, 50)
        
        # Initialize effect applied onto the player.
        self.currentEffect = None
        self.effectTimeEnd = 0
        self.effectDuration = config.EFFECTDURATION # default is 8 second.
        
        # Initialize movement speeds.
        self.regMovementSpeed = config.MOVESPEED
        self.curMovementSpeed = config.MOVESPEED
        self.boostMovementSpeed = self.regMovementSpeed * 2
        
        # Initialize player's life.
        self.life = []
        for i in range(config.LIFE):
            life_x = (i * 25) + 10
            self.life.append(BlockModel("REG", blockX=life_x, blockY=45, width=20,
                                        height=20))

    def loseLife(self):
        self.life.pop()

    def addLife(self):
        life_x = (len(self.life) * 25) + 10
        self.life.append(BlockModel("REG", blockX=life_x, blockY=45, width=20,
                                    height=20))

    def checkEffect(self):
        """
        """
        pass

    def resetEffect(self, EnvModle):
        """
        """
        self.currentEffect = None
        self.effectTimeEnd = 0
        self.curMovementSpeed = self.regMovementSpeed
        EnvModle.isVacum = False

    def addEffect(self, effectType, EnvModle):
        """Add effect to player.

        Args:
            effectType - The name of the effect's name. Currently there are only
                         two effects, including
                            - 'VACUM'
                            - 'MOVEMENTBOOST'
            EnvModle - EnvModle object.
        """
        self.currentEffect = effectType
        self.effectTimeEnd = floor(pygame.time.get_ticks() / 1000) + \
                             self.effectDuration

        if effectType == 'VACUM':
            EnvModle.isVacum = True

        if effectType == 'MOVEMENTBOOST':
            self.curMovementSpeed = self.boostMovementSpeed
