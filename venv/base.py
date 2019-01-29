import pygame, sys
from pygame.locals import *
from random import randint

pygame.init()
FPSCLOCK = pygame.time.Clock()
FPS = 15
SURF = pygame.display.set_mode((400,400))
pygame.display.set_caption("Worm")
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE = (  0,   0, 255)

HEADRIMAG = pygame.image.load('snakeR.png')
HEADDIMAG = pygame.image.load('snakeD.png')
HEADUIMAG = pygame.image.load('snakeU.png')
HEADLIMAG = pygame.image.load('snakeL.png')
CELLIMAGE = pygame.image.load('cell.png')
APPLEIMAGE = pygame.image.load('apple.png')

freeSpace = []
for x in range(0,40):
    for y in range(0,40):
        freeSpace.append((x,y))

global dir
global GameOver
GameOver = False
dir = 'right'
def gameOver(self):
    waitforKey()
    rungame()

def updateDir(tal,head):
    global dir
    testHead = pygame.Rect(head.x,head.y,10,10)
    for t in range(len(tal)-1,-1,-1):
        if t != 0:
            tal[t].x = tal[t-1].x
            tal[t].y = tal[t-1].y
        else:
            tal[0].x = head.x
            tal[0].y = head.y

    if dir == 'up':
        testHead.y -= 10
    elif dir == 'down':
        testHead.y += 10
    elif dir == 'right':
        testHead.x += 10
    elif dir == 'left':
        testHead.x -= 10
    if 390<testHead.x or testHead.x <0 or 390<testHead.y or testHead.y<0:
        gameOver(dir)
    for t in tal:
        if t.x == testHead.x and t.y == testHead.y:
            gameOver(dir)
    head.x = testHead.x
    head.y = testHead.y

def collidApple(apple ,head):
    if apple.x == head.x and apple.y == head.y:
        return True
    else:
        return False

def getApple(tail,head):
    freeSpaceCopy = freeSpace.copy()
    freeSpaceCopy.remove((head.x/10,head.y/10))
    for t in tail:
        if (t.x/10,t.y/10) in freeSpaceCopy:
            freeSpaceCopy.remove((t.x/10,t.y/10))
    randPos = freeSpaceCopy[randint(0,len(freeSpaceCopy)-1)]
    x = randint(0,39)
    applex = x * 10
    y = randint(0,39)
    appley = y *10
    return pygame.Rect(randPos[0]*10,randPos[1]*10,10,10)

def addHead(head):
    if dir =='right':
        SURF.blit(HEADRIMAG,head)
    elif dir == 'left':
        SURF.blit(HEADLIMAG, head)
    elif dir == 'up':
        SURF.blit(HEADUIMAG, head)
    elif dir == 'down':
        SURF.blit(HEADDIMAG, head)

def rungame():
    head = pygame.Rect(200, 200, 10, 10)
    tail = [pygame.Rect(190, 200, 10, 10), pygame.Rect(180, 200, 10, 10)]
    global dir
    dir = 'right'
    score = 0
    apple = True
    newApple = getApple(tail,head)
    while True:
        updated = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    if dir != 'down':
                        dir = 'up'
                elif event.key == K_DOWN:
                    if dir != 'up':
                        dir = 'down'
                elif event.key == K_RIGHT:
                    if dir != 'left':
                        dir = 'right'
                elif event.key == K_LEFT:
                    if dir != 'right':
                        dir = 'left'
        updateDir(tail,head)
        if collidApple(newApple,head):
            apple = False
            score += 1
            latest = tail[len(tail)-1]
            tail.append(pygame.Rect(latest.x,latest.y,10,10))
        if not apple:
            newApple = getApple(tail,head)
            apple = True
        SURF.fill(BLACK)
        addHead(head)
        SURF.blit(APPLEIMAGE, newApple)
        for t in tail:
            SURF.blit(CELLIMAGE, t)
        scoreLabel = BASICFONT.render('score : '+score.__str__(),True,WHITE)
        scoreRect = scoreLabel.get_rect()
        scoreRect.topleft = (310, 10)
        SURF.blit(scoreLabel,scoreRect)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def waitforKey():
    while True:
        updated = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return

        presskey = BASICFONT.render('press any key to start!', True, WHITE)
        presskeyRect = presskey.get_rect()
        presskeyRect.topleft = (100, 170)
        SURF.blit(presskey, presskeyRect)
        pygame.display.update()

waitforKey()
rungame()
