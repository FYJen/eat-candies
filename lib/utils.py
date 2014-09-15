import pygame
import sys

# Safe and easiest way to load all pygame models.
pygame.init()

def terminate(scoreFile, maxScore):
    """Terminate the game.

    Args:
        scoreFile - The score file.
        maxScore - The current higest score.
    """
    try:
        with open(scoreFile, "r+") as f:
            cur_max_score = read_score(scoreFile)
            if maxScore > cur_max_score:
                f.write(str(maxScore))
    except IOError:
        with open(scoreFile, "w") as f:
            f.write(str(maxScore))
    pygame.quit()
    sys.exit()

def waitForReply(scoreFile, maxScore):
    """Helper function that will wait for user replay.

    Args:
        scoreFile - The score file.
        maxScore - The current higest score.
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate(scoreFile, maxScore)
            elif event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate(scoreFile, maxScore)
                elif event.key == K_RETURN:
                    return
