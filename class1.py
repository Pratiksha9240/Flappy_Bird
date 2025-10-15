import random
import sys
import pygame
from pygame.locals import *

fps = 32
scrx = 289
scry = 511
scr = pygame.display.set_mode((scrx,scry))
grndy = scry * 0.8
gamesprites = {}
gamesounds = {}
play = "bird.png"
bg = "background.png"
pipe = "pipe.png"

def titlescr():
    playx = int(scrx/5)
    playy = int((scry - gamesprites["player"].get_height())/2)
    textx = int((scrx - gamesprites["text"].get_width())/2)
    texty = int(scry*0.13)
    grndx = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                scr.blit(gamesprites["background"], (0,0))
                scr.blit(gamesprites["player"], (playx,playy))
                scr.blit(gamesprites["text"], (textx,texty))
                scr.blit(gamesprites["base"], (grndx,grndy))
                pygame.display.update()
                FPSCLOCK.tick(fps)

def getRandomPipe():
    pipey = gamesprites["pipe"][0].get_height()
    offset = scry/3
    y2 = offset + random.randrange(0, int(scry - gamesprites['base'].get_height()  - 1.2 *offset))
    pipex = scrx + 10
    y1 = pipey - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2}
    ]
    return pipe

def mainGame():
    score = 0
    playx = int(scrx/5)
    playy = int(scry/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {"x": scrx+200, "y":newPipe1[0]["y"]},
        {"x": scrx+200+(scrx/2), "y":newPipe2[0]["y"]},
    ]

    lowerPipes = [
        {"x": scrx+200, "y":newPipe1[1]["y"]},
        {"x": scrx+200+(scrx/2), "y":newPipe2[1]["y"]},
    ]

    pipeVelX = -4
    playVelY = -9
    playMaxVelY = 10
    playMinVelY = -8
    playAccY = 1

    playFlapAccv = -8
    playFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                if playy > 0:
                    playVelY = playFlapAccv
                    playFlapped = True
                    gamesounds["wing"].play()

        crashTest = isCollide(playx,playy,upperPipes,lowerPipes)
        if crashTest:
            return

        playMidPos = playx + gamesprites["player"].get_width()/2
        for pipe in upperPipes:
            pipeMidpos = pipe["x"] + gamesprites["pipe"][0].get_width()/2
            if pipeMidpos<= playMidPos < pipeMidpos +4:
                score +=10
                print(f"Your score is {score}")
                gamesounds["point"].play()

        if playVelY <playMaxVelY and not playFlapped:
            playVelY += playAccY

        if playFlapped:
            playFlapped = False

        playY = gamesprites["player"].get_height()
        playy = playy + min(playVelY, grndy - playy - playY)

        for upperPipe,lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -gamesprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        scr.blit(gamesprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            scr.blit(gamesprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            scr.blit(gamesprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        scr.blit(gamesprites['base'], (basex, grndy))
        scr.blit(gamesprites['player'], (playx, playy))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += gamesprites['numbers'][digit].get_width()
        Xoffset = (scrx - width)/2
        for digit in myDigits:
            scr.blit(gamesprites['numbers'][digit], (Xoffset, scry*0.12))
            Xoffset += gamesprites['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(fps)


def isCollide(playx,playy,tpipe,bpipe):
    if playy>grndy - 25 or playy<0:
        gamesounds["hit"].play()
        return True
    
    for pipe in tpipe:
        pipey = gamesprites["pipe"][0].get_height()
        if(playy < pipey + pipe["y"] and abs(playx - pipe["x"]) < gamesprites["pipe"][0].get_width()):
            gamesounds["hit"].play()
            return True
        
    for pipe in bpipe:
        if(playy + gamesprites["player"].get_height() > pipe["y"]) and abs(playx - pipe["x"]) < gamesprites["pipe"][0].get_width():
            gamesounds["hit"].play()
            return True
    
    return False

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Flappy Bird")
    gamesprites["numbers"] = (
        pygame.image.load("zero.png").convert_alpha(),
        pygame.image.load("one.png").convert_alpha(),
        pygame.image.load("two.png").convert_alpha(),
        pygame.image.load("three.png").convert_alpha(),
        pygame.image.load("four.png").convert_alpha(),
        pygame.image.load("five.png").convert_alpha(),
        pygame.image.load("six.png").convert_alpha(),
        pygame.image.load("seven.png").convert_alpha(),
        pygame.image.load("eight.png").convert_alpha(),
        pygame.image.load("nine.png").convert_alpha(),
    )

    gamesprites["text"] =pygame.image.load("start.png").convert_alpha()
    gamesprites["base"] =pygame.image.load("wall.png").convert_alpha()
    gamesprites["pipe"] =(pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
    pygame.image.load(pipe).convert_alpha()
    )

    gamesounds["die"] = pygame.mixer.Sound("die.wav")
    gamesounds["hit"] = pygame.mixer.Sound("hit.wav")
    gamesounds["point"] = pygame.mixer.Sound("point.wav")
    gamesounds["swoosh"] = pygame.mixer.Sound("swoosh.wav")
    gamesounds["wing"] = pygame.mixer.Sound("wing.wav")

    gamesprites["background"] = pygame.image.load(bg).convert()
    gamesprites["player"] = pygame.image.load(play).convert_alpha()

    while True:
        titlescr()
        mainGame()