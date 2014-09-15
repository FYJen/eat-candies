import pygame
import random

import config.default_config as config

# Safe and easiest way to load all pygame models.
pygame.init()

class BlockModel(object):
    """Block model.
    """
    def __init__(self, blockType, blockX=False, blockY=False, status='FALL',
                 width=config.blockSize, height=config.blockSize):
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
        if blockX == False and blockY == False:
            self.rect = pygame.Rect(
                            random.randint(10, config.W_WIDTH - config.blockSize),
                            0, width, height)
            self.type = blockType
            self.status = status

