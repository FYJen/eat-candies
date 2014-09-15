import pygame

from config.default_config import WHITE
from config.load_fonts import *
from config.load_imgs import *

# Safe way to load pygame models.
pygame.init()

def drawText(text, font, surface, x, y):
    """Helper function to draw text onto the screen (surface).

    Args:
        test - A string.
        font - Font style.
        surface - A pygame window surface.
        x - x coordinate on the surface.
        y - y coordinate on the surface.
    """
    textObj = font.render(text, 1, WHITE)
    textrect = textObj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textObj, textrect)

def printInstruction(windowSurface, windowWidth, windowHeight):
    """Helper function to print instructions.

    Args:
        windowSurface - A pygame window surface.
        windowWidth - The width of the window.
        windowHeight - The height of the window.
    """
    quarterWidth = windowWidth / 4
    halfHeight = windowHeight / 2

    drawText('Eat All the Candy ', font, windowSurface, quarterWidth - 25,
             (windowHeight / 3)-110)
    drawText('Press Enter key to start.', font, windowSurface, quarterWidth - 65,
             (windowHeight / 3)-65)
    
    grass_icon = pygame.Rect(28, (windowHeight / 4) - 15, windowWidth - 60, 50)
    windowSurface.blit(grassImg, grass_icon)
    
    arrowkey_icon = pygame.Rect(quarterWidth - 55, halfHeight - 53, 40, 30)
    windowSurface.blit(arrowImg, arrowkey_icon)
    drawText(":  Use arrow keys to control your minion", fontInstruct,
             windowSurface, quarterWidth - 9, halfHeight - 40)
    
    candy_icon = pygame.Rect(quarterWidth - 43, halfHeight - 10, blockSize,
                             blockSize)
    windowSurface.blit(normalCandyImg, candy_icon)
    drawText(":  When you see candies, go nuts! Eat them all", fontInstruct,
             windowSurface, quarterWidth - 9, halfHeight - 7)
    
    brick_icon = pygame.Rect(quarterWidth - 43, halfHeight + 30, blockSize,
                             blockSize)
    windowSurface.blit(brickImg, brick_icon)
    drawText(":  Opps! You have to dodge me", fontInstruct, windowSurface,
             quarterWidth - 7, halfHeight + 35)
    
    heart_icon = pygame.Rect(quarterWidth - 43, halfHeight + 70, blockSize,
                             blockSize)
    windowSurface.blit(heartImg, heart_icon)
    drawText(":  I am the heart! I can revive you", fontInstruct, windowSurface,
             quarterWidth - 7, halfHeight + 72)
    
    vacum_icon = pygame.Rect(quarterWidth - 43, halfHeight + 110, blockSize,
                             blockSize)
    windowSurface.blit(normalVacuumImg, vacum_icon)
    drawText(":  I am a vaccum cleaner. I love candies. Num Num Num", fontInstruct,
             windowSurface, quarterWidth - 7, halfHeight + 114)
    
    boost_icon = pygame.Rect(quarterWidth - 43, halfHeight + 150, blockSize,
                             blockSize)
    windowSurface.blit(normalMoveBoostImg, boost_icon)
    drawText(":  I am nitro boots. I grant you mobility", fontInstruct,
             windowSurface, quarterWidth - 6, halfHeight + 155)

def printEnding(windowSurface, windowWidth, windowHeight, score, topScore):
    """Helper function to print ending when the game ends.

    Args:
        windowSurface - A pygame window surface.
        windowWidth - The width of the window.
        windowHeight - The height of the window.
        score - Player's score.
        topScore - The highest score overall.
    """
    drawText('Opps! Try again', font, windowSurface, (windowWidth / 8) + 55,
             (windowHeight / 4) - 50)
    drawText('Press Enter key to restart', font, windowSurface, (windowWidth / 10),
             (windowHeight / 4))
    grass_icon = pygame.Rect(28, (windowHeight / 3) - 20, windowWidth - 60, 50)
    windowSurface.blit(grassImg, grass_icon)
    drawText('Your Score: %s' % score, fontFinal, windowSurface,
             (windowWidth / 3) - 20, (windowHeight / 2) - 10)
    drawText('Top Score: %s' % topScore, fontFinal, windowSurface,
             (windowWidth / 3) - 20, (windowHeight / 2) + 30)
    end_icon1 = pygame.Rect(windowWidth - 150, windowHeight - 120, 120, 100)
    windowSurface.blit(endingPlayerImg, end_icon1)
    end_icon2 = pygame.Rect(30, windowHeight - 100, 80, 80)
    windowSurface.blit(endingCandyImg, end_icon2)
