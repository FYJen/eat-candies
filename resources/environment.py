import pygame
import sys

import config.default_config as config
from block import BlockModel

# Safe way to load pygame models.
pygame.init()

class EnvModle(object):
    """Environment Model.
    """
    def __init__(self):
        """
        """
        self.isVacum = config.VACUM
        self.blockSize = config.blockSize
        self.W_WIDTH = config.W_WIDTH
        self.mainClock = pygame.time.Clock()

        # An array that holds a list of blocks. Initialize the first block.
        self.blocks = []
        self.blocks.append(BlockModel('REG'))

        # Initialize score matrixs.
        self.scoreFile = config.SCORE_FILE
        self.regScore = config.REG_SCORE
        self.vacumScore = config.VACUM_SCORE
        self.boostScore = config.BOOST_SCORE
        self.heartScore = config.HEART_SCORE
        self.curScore = 0
        self.topScore = 0

    def loadWindow(self):
        """Loads app's windows.
        """
        self.windowSurface = pygame.display.set_mode(
                                (config.W_WIDTH, config.W_HEIGHT), 0, 32)
        pygame.display.set_caption(config.CAPTION)

    def loadImgs(self):
        """Loads up images.
        """
        # Load normal player images.
        self.playerImg = pygame.image.load('img/player.png')
        self.normalPlayerImg = pygame.transform.scale(self.playerImg, (60, 50))
        self.lifeIcon = pygame.transform.scale(self.playerImg, (30,20))

        # Load player image with vacuum effect.
        self.playerVaccumImg = pygame.transform.scale(
                                pygame.image.load('img/player_vac.png'), (60, 50))

        # Load player image with nitro boots effect.
        self.playerBootsImg = pygame.transform.scale(
                                pygame.image.load('img/player_boost.png'),
                                (60, 50))

        # Load candy images.
        self.candyImg = pygame.image.load('img/Candy.png')
        self.normalCandyImg = pygame.transform.scale(
                                self.candyImg, (self.blockSize, self.blockSize))
        self.endingCandyImg = pygame.transform.scale(self.candyImg, (80, 80))

        # Load vacuum cleaner image.
        self.vacuumImg = pygame.image.load('img/vacuum.png')
        self.normalVacuumImg = pygame.transform.scale(self.vacuumImg,
                                    (self.blockSize + 5, self.blockSize + 5))

        # Load nitro boots image.
        self.moveboostImg = pygame.image.load("img/boots.png")
        self.normalMoveBoostImg = pygame.transform.scale(self.moveboostImg,
                                        (self.blockSize + 5, self.blockSize + 5))

        # Load brick image.
        self.brickImg = pygame.transform.scale(pygame.image.load('img/brick.jpeg'),
                            (self.blockSize + 5, self.blockSize + 5))

        # Load heart image.
        self.heartImg = pygame.transform.scale(pygame.image.load('img/heart.png'),
                                          (self.blockSize, self.blockSize))

        # Load grass image.
        self.grassImg = pygame.transform.scale(pygame.image.load('img/grass.png'),
                            (self.W_WIDTH - 60, 50))

        # Load arrow keys image.
        self.arrowImg = pygame.transform.scale(pygame.image.load('img/arrow_key.png'),
                                          (40, 30))

        # Load player image for the ending scene.
        self.endingPlayerImg = pygame.transform.scale(
                                    pygame.image.load('img/let_me_eat.png'),
                                    (120, 100))

    def loadSounds(self):
        """Loads up sound effects.
        """
        # Add sound effect for picking up candies.
        self.pickUpSound = pygame.mixer.Sound('sound/pickup.wav')
        self.pickUpSound.set_volume(0.05)

        # Add sound effect for being hit by the bricks.
        self.uhohSound = pygame.mixer.Sound('sound/uh_oh.wav')
        self.uhohSound.set_volume(1.0)

        # Add sound effect for picking up extra life (heart).
        self.loveyouSouond = pygame.mixer.Sound("sound/love_you.wav")
        self.loveyouSouond.set_volume(1.0)

        # Add back group music.
        self.pygame.mixer.music.load('sound/background.wav')
        self.pygame.mixer.music.set_volume(0.08)

    def loadFonts(self):
        """Loads up fonts.
        """
        # Set font
        self.font = pygame.font.SysFont(None, 48)
        self.fontScore = pygame.font.SysFont(None, 25)
        self.fontFinal = pygame.font.SysFont(None, 35)
        self.fontInstruct = pygame.font.SysFont(None, 20)

    def loadEvents(self):
        """Sets recursive events.
        """
        # Set up events for different items.
        self.MODNEW_BLOCK = pygame.USEREVENT
        self.BRICK_BLOCK = pygame.USEREVENT + 1
        self.HEART_BLOCK = pygame.USEREVENT + 2
        self.VACUM_BLOCK = pygame.USEREVENT + 3
        self.BOOST_BLOCK = pygame.USEREVENT + 4

        # Set up timer for repeated events
        pygame.time.set_timer(self.MODNEW_BLOCK, 25000)
        pygame.time.set_timer(self.VACUM_BLOCK, 13100)
        pygame.time.set_timer(self.BOOST_BLOCK, 23050)
        pygame.time.set_timer(self.BRICK_BLOCK, 1000)
        pygame.time.set_timer(self.HEART_BLOCK, 40000)

    def addScore(self, scoreType):
        """Increment score.

        Args:
            scoreType - The score type.
        """
        if scoreType == 'REG':
            self.curScore += self.regScore
        elif scoreType == 'VACUM':
            self.curScore += self.vacumScore
        elif scoreType == 'BOOST':
            self.curScore += self.boostScore
        elif scoreType == 'heartScore':
            self.curScore += self.heartScore

    def loadScore(self):
        """Read the higest score from file.

        Args:
            scoreFile - The score file.

        Returns:
            The higest score in int.
        """
        try:
            with open(self.scoreFile, "r") as f:
                scoreFromFile = int(f.readline().strip())
            self.topScore = scoreFromFile
        except IOError:
            print "no such file, return 0"
            self.topScore = 0

    def terminateGame(self):
        """Terminate the game.
        """
        try:
            with open(self.scoreFile, "r+") as f:
                if self.curScore > self.topScore:
                    f.write(str(self.curScore))
        except IOError:
            with open(self.scoreFile, "w") as f:
                f.write(str(self.curScore))
        pygame.quit()
        sys.exit()

    def waitForPlayerReply(self):
        """Helper function that will wait for user replay.
        """
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.terminate()
                    elif event.key == K_RETURN:
                        return
