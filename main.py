import pygame
import random
import sys
from pygame.locals import *

# Game Spacific variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 591
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUND = SCREENHEIGHT * 0.7
GAME_SPRITS = {}
GAME_SOUND = {}
PLAYER = 'galarry/sprits/Bird.png'
PIPE = 'galarry/sprits/Pipes.png'
MASSAGE = 'galarry/sprits/0.png'
BACKGROUND = 'galarry/sprits/bg.png'


def welcomeScreen():
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITS['player'].get_height()) / 2)
    massagex = int((SCREENHEIGHT - GAME_SPRITS['message'].get_width()) / 5)
    massagey = int(SCREENHEIGHT * 0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITS['background'], (0, 0))
                SCREEN.blit(GAME_SPRITS['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITS['message'], (massagex, massagey))
                SCREEN.blit(GAME_SPRITS['base'], (basex, GROUND))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)
    basex = 0

    # Creating random generated pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipe = [
        {'x': SCREENWIDTH + 220, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 220 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}
    ]

    lowerPipe = [
        {'x': SCREENWIDTH + 220, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 220 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    pipeVelocityX = -4

    playerVelocityY = -9
    playerMaxVelocityY = 10
    playerMinVelocityY = -8
    playerAccY = 1

    playerFlapAcc = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelocityY = playerFlapAcc
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipe, lowerPipe)

        # Player is collished
        if crashTest:
            return

        # Check for scores
        playerMidPos = playerx + GAME_SPRITS['player'].get_width() / 2

        for pipe in upperPipe:
            pipeMidPos = pipe['x'] + GAME_SPRITS['pipe'][0].get_width() / 5

            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUND['point'].play()

        if playerVelocityY < playerMaxVelocityY and not playerFlapped:
            playerVelocityY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITS['player'].get_height()
        playery = playery + min(playerVelocityY, GROUND - playery - playerHeight)

        for upipe, lpipe in zip(upperPipe, lowerPipe):
            upipe['x'] += pipeVelocityX
            lpipe['x'] += pipeVelocityX

        if 0 < upperPipe[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipe.append(newpipe[0])
            lowerPipe.append(newpipe[1])

        if upperPipe[0]['x'] < -GAME_SPRITS['pipe'][0].get_width():
            upperPipe.pop(0)
            lowerPipe.pop(0)

        # lets blit our sprits now
        SCREEN.blit(GAME_SPRITS['background'], (0, 0))
        for upipe, lpipe in zip(upperPipe, lowerPipe):
            SCREEN.blit(GAME_SPRITS['pipe'][0], (upipe['x'], upipe['y']))
            SCREEN.blit(GAME_SPRITS['pipe'][1], (lpipe['x'], lpipe['y']))
        SCREEN.blit(GAME_SPRITS['base'], (basex, GROUND))
        SCREEN.blit(GAME_SPRITS['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITS['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITS['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITS['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUND - 20 or playery < 0:
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITS['pipe'][0].get_height()
        if playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITS['pipe'][0].get_width():
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITS['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITS['pipe'][0].get_width():
            return True

    return False


def getRandomPipe():
    """
    Generate positions of upper and lower pipes (tuples of x and y, top pipe is
    above bottom pipe)
    """
    pipeHeight = GAME_SPRITS['pipe'][0].get_height()
    offset = SCREENHEIGHT / 5
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITS['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 1
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x': pipeX, 'y': -y1},  # Upper pipe
        {'x': pipeX, 'y': y2}  # Lower pipe
    ]

    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy bird by Ashish")

    GAME_SPRITS['numbers'] = (
        pygame.transform.scale(pygame.image.load('galarry/sprits/0.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/1.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/2.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/3.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/4.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/5.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/6.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/7.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/8.png').convert_alpha(), (34, 50)),
        pygame.transform.scale(pygame.image.load('galarry/sprits/9.png').convert_alpha(), (34, 50)),
    )

    GAME_SPRITS['message'] = pygame.transform.scale(pygame.image.load(MASSAGE).convert_alpha(), (150, 200))

    GAME_SPRITS['pipe'] = (
        pygame.transform.scale(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),(35, 300)),
        pygame.transform.scale(pygame.image.load(PIPE).convert_alpha(),(35, 300))
    )

    GAME_SPRITS['base'] = pygame.transform.scale(pygame.image.load('galarry/sprits/ground copy.png').convert_alpha(), (350, 300))

    GAME_SPRITS['player'] = pygame.transform.scale(pygame.image.load(PLAYER).convert_alpha(), (38, 38))

    GAME_SPRITS['background'] = pygame.image.load(BACKGROUND).convert_alpha()

    GAME_SOUND['wing'] = pygame.mixer.Sound('galarry/sounds/wings.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('galarry/sounds/point.wav')

    while True:
        welcomeScreen()
        mainGame()