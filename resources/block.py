import pygame
import random
from math import ceil

import config.default_config as config

# Safe and easiest way to load all pygame models.
pygame.init()

class BlockModel(object):
    """Block model.
    """
    def __init__(self, blockType, blockX=None, blockY=None, status='FALL',
                 width=config.BLOCKSIZE, height=config.BLOCKSIZE):
        """Generate new block of objects.

        Args:
            blockType - Type of the block, including 'REG', 'HEART', 'VACUM', and
                        'MOVEMENTBOOST'.
            blockX - X coordinate for the block.
            blockY - Y coordinate for the block.
            status - The status of the block. It can be either 'FALL' or 'VACUM'.
                     Default is 'FALL'.
            width - The width length of the block.
            height - The height of the block.

        Returns:
            A dictionary with block info.
        """
        self.followSpeed = config.FOLLOWSPEED
        self.fallSpeed = config.FALLSPEED
        self.W_WIDTH = config.W_WIDTH
        self.blockSize = config.BLOCKSIZE

        # Sets up block info.
        self.rect = \
            pygame.Rect(blockX, blockY, width, height) if blockX and blockY else \
            pygame.Rect(random.randint(10, self.W_WIDTH - self.blockSize), 0,
                        width, height)
        self.status = status
        self.type = blockType

    def followPlayer(self, player):
        """If the environment is under VACUM status, the cnady block will follow
        and get sucked to player.

        Args:
            player - The player object.
        """
        if self.rect.centerx < player.rect.centerx:
            if self.rect.centery <= player.rect.centery:
                self.rect.centerx += \
                    ceil((player.rect.centerx - self.rect.centerx) / \
                         self.followSpeed)
                self.rect.centery += \
                    ceil((player.rect.centery - self.rect.centery) / \
                         self.followSpeed)
            else:
                self.rect.centerx += \
                    ceil((player.rect.centerx - self.rect.centerx) / \
                         self.followSpeed) + 1
                self.rect.centery -= \
                    ceil((self.rect.centery - player.rect.centery) / \
                         self.followSpeed) + 1
        else:
            if self.rect.centery <= player.rect.centery:
                self.rect.centerx -= \
                    ceil((self.rect.centerx - player.rect.centerx) / \
                         self.followSpeed)
                self.rect.centery += \
                    ceil((player.rect.centery - self.rect.centery) / \
                         self.followSpeed)
            else:
                self.rect.centerx -= \
                    ceil((self.rect.centerx - player.rect.centerx) / \
                         self.followSpeed) + 1
                self.rect.centery -= \
                    ceil((self.rect.centery - player.rect.centery) / \
                         self.followSpeed) + 1

    def fallDown(self):
        shouldBeRemoved = False
        self.rect.top += self.fallSpeed
        if self.rect.top >= self.W_WIDTH:
            shouldBeRemoved = True

        return shouldBeRemoved
