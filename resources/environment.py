import pygame
from pygame.locals import *
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
        # Initialize world states.
        self.isVacum = config.VACUM
        self.mainClock = pygame.time.Clock()

        # Initialize window and block size.
        self.blockSize = config.BLOCKSIZE
        self.W_WIDTH = config.W_WIDTH
        self.W_HEIGHT = config.W_HEIGHT

        # Initialize font color.
        self.WHITE = config.WHITE
        self.BLACK = config.BLACK

        # Initialize block array that holds a list of blocks.
        self.blocks = []

        # Initialize block delay.
        self.blockDelay = config.BLOCKDELAY
        self.blockDelayCounter = 0

        # Initialize score matrixs.
        self.scoreFile = config.SCORE_FILE
        self.candyScore = config.CANDY_SCORE
        self.vacumScore = config.VACUM_SCORE
        self.boostScore = config.BOOST_SCORE
        self.heartScore = config.HEART_SCORE
        self.curScore = 0
        self.topScore = 0

    def loadWindow(self):
        """Loads app's windows.
        """
        self.windowSurface = pygame.display.set_mode(
                                (self.W_WIDTH, self.W_HEIGHT), 0, 32)
        pygame.display.set_caption(config.CAPTION)

    def loadImgs(self):
        """Loads up images.
        """
        # Load normal player images.
        self.playerImg = pygame.image.load('img/player.png')
        self.normalPlayerImg = pygame.transform.scale(self.playerImg, (60, 50))
        self.lifeIcon = pygame.transform.scale(self.playerImg, (30,20))

        # Load player image with vacuum effect.
        self.playerVacumImg = pygame.transform.scale(
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
        pygame.mixer.music.load('sound/background.wav')
        pygame.mixer.music.set_volume(0.08)

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
        self.PROGRESSION_BLOCK = pygame.USEREVENT
        self.BRICK_BLOCK = pygame.USEREVENT + 1
        self.HEART_BLOCK = pygame.USEREVENT + 2
        self.VACUM_BLOCK = pygame.USEREVENT + 3
        self.BOOST_BLOCK = pygame.USEREVENT + 4
        self.CANDY_BLOCK = pygame.USEREVENT + 5

        # Set up timer for repeated events
        pygame.time.set_timer(self.PROGRESSION_BLOCK, 25000)
        pygame.time.set_timer(self.VACUM_BLOCK, 13100)
        pygame.time.set_timer(self.BOOST_BLOCK, 23050)
        pygame.time.set_timer(self.BRICK_BLOCK, 1000)
        pygame.time.set_timer(self.HEART_BLOCK, 40000)
        pygame.time.set_timer(self.CANDY_BLOCK, 800)

    def load(self):
        """Loads windows, images, sounds, fonts, recursive events and scores.
        """
        self.loadWindow()
        self.loadImgs()
        self.loadSounds()
        self.loadFonts()
        self.loadEvents()
        self.loadScore()

    def drawText(self, text, font, surface, x, y):
        """Helper function to draw text onto the screen (surface).

        Args:
            test - A string.
            font - Font style.
            surface - A pygame window surface.
            x - x coordinate on the surface.
            y - y coordinate on the surface.
        """
        textObj = font.render(text, 1, self.WHITE)
        textrect = textObj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textObj, textrect)

    def printInstruction(self):
        """Helper function to print instructions.
        """
        quarterWidth = self.W_WIDTH / 4
        halfHeight = self.W_HEIGHT / 2

        # Print headers.
        self.drawText('Eat All the Candy ', self.font, self.windowSurface,
                      quarterWidth - 25, (self.W_HEIGHT / 3) - 110)
        self.drawText('Press Enter key to start.', self.font, self.windowSurface,
                      quarterWidth - 65, (self.W_HEIGHT / 3) - 65)
        
        # Print grass.
        grass_icon = pygame.Rect(28, (self.W_HEIGHT / 4) - 15, self.W_WIDTH - 60, 50)
        self.windowSurface.blit(self.grassImg, grass_icon)
        
        # First instruction.
        arrowkey_icon = pygame.Rect(quarterWidth - 55, halfHeight - 53, 40, 30)
        self.windowSurface.blit(self.arrowImg, arrowkey_icon)
        self.drawText(":  Use arrow keys to control your minion", self.fontInstruct,
                      self.windowSurface, quarterWidth - 9, halfHeight - 40)
        
        # Second instruction.
        candy_icon = pygame.Rect(quarterWidth - 43, halfHeight - 10, self.blockSize,
                                 self.blockSize)
        self.windowSurface.blit(self.normalCandyImg, candy_icon)
        self.drawText(":  When you see candies, go nuts! Eat them all", self.fontInstruct,
                      self.windowSurface, quarterWidth - 9, halfHeight - 7)
        
        # Third instruction.
        brick_icon = pygame.Rect(quarterWidth - 43, halfHeight + 30, self.blockSize,
                                 self.blockSize)
        self.windowSurface.blit(self.brickImg, brick_icon)
        self.drawText(":  Opps! You have to dodge me", self.fontInstruct,
                      self.windowSurface, quarterWidth - 7, halfHeight + 35)
        
        # Forth instruction.
        heart_icon = pygame.Rect(quarterWidth - 43, halfHeight + 70, self.blockSize,
                                 self.blockSize)
        self.windowSurface.blit(self.heartImg, heart_icon)
        self.drawText(":  I am the heart! I can revive you", self.fontInstruct,
                      self.windowSurface, quarterWidth - 7, halfHeight + 72)
        
        # Fifth instruction.
        vacum_icon = pygame.Rect(quarterWidth - 43, halfHeight + 110, self.blockSize,
                                 self.blockSize)
        self.windowSurface.blit(self.normalVacuumImg, vacum_icon)
        self.drawText(":  I am a vaccum cleaner. I love candies. Num Num Num",
                      self.fontInstruct, self.windowSurface, quarterWidth - 7,
                      halfHeight + 114)
        
        # Sixth instruction.
        boost_icon = pygame.Rect(quarterWidth - 43, halfHeight + 150, self.blockSize,
                                 self.blockSize)
        self.windowSurface.blit(self.normalMoveBoostImg, boost_icon)
        self.drawText(":  I am nitro boots. I grant you mobility", self.fontInstruct,
                      self.windowSurface, quarterWidth - 6, halfHeight + 155)

    def printEnding(self):
        """Helper function to print ending when the game ends.
        """
        # Print headers.
        self.drawText('Opps! Try again', self.font, self.windowSurface,
                 (self.W_WIDTH / 8) + 55, (self.W_HEIGHT / 4) - 50)
        self.drawText('Press Enter key to restart', self.font, self.windowSurface,
                 (self.W_WIDTH / 10), (self.W_HEIGHT / 4))
        
        # Print grass.
        grass_icon = pygame.Rect(28, (self.W_HEIGHT / 3) - 20, self.W_WIDTH - 60, 50)
        self.windowSurface.blit(self.grassImg, grass_icon)
        
        # Print your current score and the top score.
        self.drawText('Your Score: %s' % self.curScore, self.fontFinal, self.windowSurface,
                      (self.W_WIDTH / 3) - 20, (self.W_HEIGHT / 2) - 10)
        self.drawText('Top Score: %s' % self.topScore, self.fontFinal, self.windowSurface,
                      (self.W_WIDTH / 3) - 20, (self.W_HEIGHT / 2) + 30)
        
        # Print two cute icons at the end.
        end_icon1 = pygame.Rect(self.W_WIDTH - 150, self.W_HEIGHT - 120, 120, 100)
        self.windowSurface.blit(self.endingPlayerImg, end_icon1)
        end_icon2 = pygame.Rect(30, self.W_HEIGHT - 100, 80, 80)
        self.windowSurface.blit(self.endingCandyImg, end_icon2)

    def printScore(self):
        self.drawText('Score: %s' % self.curScore, self.fontScore,
                      self.windowSurface, 10, 5)
        self.drawText('Top Score: %s' % self.topScore, self.fontScore,
                      self.windowSurface, 10, 25)

    def checkPlayerBlocksCollision(self, player):
        for block in self.blocks[:]:
            if player.rect.colliderect(block.rect):
                # Check to see if the player eats a special candy
                if block.type == 'VACUM':
                    player.addEffect('VACUM', self)
                    self.pickUpSound.play()
                    self.addScore('VACUM')
                elif block.type == 'MOVEMENTBOOST':
                    player.addEffect('MOVEMENTBOOST', self)
                    self.pickUpSound.play()
                    self.addScore('BOOST')
                elif block.type == 'BRICK':
                    player.loseLife()
                    self.uhohSound.play()
                elif block.type == 'HEART':
                    if len(player.life) < 5:
                        player.addLife()
                        self.loveyouSouond.play()
                    else:
                        self.addScore('HEART')
                else:
                    self.addScore('CANDY')
                    self.pickUpSound.play()
                
                # Remove block from the blocks list.
                self.removeBlock(block)
            elif (self.isVacum and block.type == 'CANDY') or \
                    (block.status == 'VACUM'):
                block.status = 'VACUM'
                block.followPlayer(player)

                # Check collision after moving
                if player.rect.colliderect(block.rect):
                    self.blocks.remove(block)
                    self.pickUpSound.play()
            else:
                remove = block.fallDown()
                if remove:
                    self.removeBlock(block)

    def isGameDone(self, player):
        gameEnd = False 
        if len(player.life) == 0:
            if self.curScore > self.topScore:
                self.topScore = self.curScore
            gameEnd = True

        return gameEnd

    def applyPlayerImage(self, player):
        if player.currentEffect is None:
            self.windowSurface.blit(self.normalPlayerImg, player.rect)
        elif player.currentEffect == 'VACUM':
            self.windowSurface.blit(self.playerVacumImg, player.rect)
        elif player.currentEffect == 'MOVEMENTBOOST':
            self.windowSurface.blit(self.playerBootsImg, player.rect)

    def applyBlocksImage(self):
        for block in self.blocks:
            if block.type == 'VACUM':
                self.windowSurface.blit(self.normalVacuumImg, block.rect)
            elif block.type  == 'MOVEMENTBOOST':
                self.windowSurface.blit(self.normalMoveBoostImg, block.rect)
            elif block.type  == 'BRICK':
                self.windowSurface.blit(self.brickImg, block.rect)
            elif block.type  == 'HEART':
                self.windowSurface.blit(self.heartImg, block.rect)
            else:
                self.windowSurface.blit(self.normalCandyImg, block.rect)

    def applyLifeImage(self, player):
        for block in player.life:
            self.windowSurface.blit(self.lifeIcon, block.rect)

    def fillScreenBackground(self):
        self.windowSurface.fill(self.BLACK)

    def increaseDifficulty(self):
        if self.blockDelay >= 21:
            self.blockDelay -= 4

    def updateDisplay(self):
        """Wrapper function around pygame's display.update()
        """
        pygame.display.update()

    def playBackgroundMusic(self):
        """Play the back ground 
        """
        pygame.mixer.music.play(-1, 0.0)

    def stopBackgroundMusic(self):
        pygame.mixer.music.stop()

    def addBlock(self, *args, **kwargs):
        self.blocks.append(BlockModel(*args, **kwargs))

    def removeBlock(self, block):
        self.blocks.remove(block)

    def flushBlockList(self):
        self.blocks = []

    def flushCurScore(self):
        self.curScore = 0

    def addScore(self, scoreType='NORM'):
        """Increment score.

        Args:
            scoreType - The score type.
        """
        if scoreType == 'CANDY':
            self.curScore += self.candyScore
        elif scoreType == 'VACUM':
            self.curScore += self.vacumScore
        elif scoreType == 'BOOST':
            self.curScore += self.boostScore
        elif scoreType == 'HEART':
            self.curScore += self.heartScore
        elif scoreType == 'NORM':
            self.curScore += 1

    def loadScore(self):
        """Read the higest score from file.

        Args:
            scoreFile - The score file.

        Returns:
            The higest score in int.
        """
        try:
            with open(self.scoreFile, 'r') as f:
                scoreFromFile = int(f.readline().strip())
            self.topScore = scoreFromFile
        except IOError:
            print 'no such file, topScore is 0'
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
                    self.terminateGame()
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.terminateGame()
                    elif event.key == K_RETURN:
                        return

    def tick(self, num):
        self.mainClock.tick(num)
