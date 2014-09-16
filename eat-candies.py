#!/usr/bin/python

#
# Version 1.0
# Creator: AJ
# Email: fei.yang.jen@gmail.com
# Date: 2012.12.18
# Updated on: 2014.09.15
#

import pygame
from pygame.locals import *

from resources import *

def main():
    """
    """
    # Safe and easiest way to load all pygame models.
    pygame.init()

    # Set up game environment.
    gameEnv = EnvModle()
    gameEnv.load()
    gameEnv.printInstruction()
    gameEnv.updateDisplay()
    gameEnv.waitForPlayerReply()

    # Game starts.
    while True:
        # Play music.
        gameEnv.playBackgroundMusic()

        # Set up player.
        player = PlayerModel()

        # Initiate the first block and reset curScore.
        gameEnv.flushCurScore()
        gameEnv.addBlock('CANDY')

        while not gameEnv.isGameDone(player):
            gameEnv.addScore()
            player.checkEffect(gameEnv)

            for event in pygame.event.get():
                if event.type == QUIT:
                    gameEnv.terminateGame()
                elif event.type == KEYDOWN:
                    if event.key == K_LEFT or event.key == ord('a'):
                            player.moveLeft = True
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        player.moveRight = True
                    elif event.key == K_UP or event.key == ord('w'):
                        player.moveUp = True
                    elif event.key == K_DOWN or event.key == ord('s'):
                        player.moveDown = True
                elif event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        gameEnv.terminateGame()
                    elif event.key == K_LEFT or event.key == ord('a'):
                        player.moveLeft = False
                    elif event.key == K_RIGHT or event.key == ord('d'):
                        player.moveRight = False
                    elif event.key == K_UP or event.key == ord('w'):
                        player.moveUp = False
                    elif event.key == K_DOWN or event.key == ord('s'):
                        player.moveDown = False
                    elif event.key == ord('t'):
                        player.teleport()
                    elif event.key == ord('m'):
                        player.increaseSpeed(1)
                    elif event.key == ord('n'):
                        player.decreaseSpeed(1)
                elif event.type == MOUSEBUTTONUP:
                    if gameEnv.isVacum:
                        gameEnv.addBlock('CANDY', blockX=event.pos[0],
                                         blockY=event.pos[1], status='VACUM')
                    else:
                        gameEnv.addBlock('CANDY', blockX=event.pos[0],
                                         blockY=event.pos[1])
                elif event.type == gameEnv.VACUM_BLOCK:
                    gameEnv.addBlock('VACUM')
                elif event.type == gameEnv.BOOST_BLOCK:
                    gameEnv.addBlock('MOVEMENTBOOST')
                elif event.type == gameEnv.BRICK_BLOCK:
                    gameEnv.addBlock('BRICK')
                elif event.type == gameEnv.HEART_BLOCK:
                    gameEnv.addBlock('HEART')
                elif event.type == gameEnv.CANDY_BLOCK:
                    gameEnv.addBlock('CANDY')
                elif event.type == gameEnv.PROGRESSION_BLOCK:
                    gameEnv.increaseDifficulty()

            # Move player.
            player.move()

            # Check player and blocks collision.
            gameEnv.checkPlayerBlocksCollision(player)

            # Apply background.
            gameEnv.fillScreenBackground()

            # Apply images to player, player's life points and blocks.
            gameEnv.applyPlayerImage(player)
            gameEnv.applyLifeImage(player)
            gameEnv.applyBlocksImage()

            # Refresh score
            gameEnv.printScore()

            # Update display and set FPS.
            gameEnv.updateDisplay()
            gameEnv.tick(40)

        # Game ends. Reset player effect and flush block list buffer.
        player.resetEffect(gameEnv)
        gameEnv.flushBlockList()
        gameEnv.stopBackgroundMusic()

        # Refill the background and print ending texts.
        gameEnv.fillScreenBackground()
        gameEnv.printEnding()

        # Update display and see if player wants to play it again.
        gameEnv.updateDisplay()
        gameEnv.waitForPlayerReply()

if __name__ == '__main__':
    main()
