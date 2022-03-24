import pygame
import time
import random
A = [[0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0]]
BLUE = 'blue.png'
RED = 'red.png'

def func(y,x, color):
    coor = (62*y+55, 63*x+35)
    myBall = pygame.image.load(color)
    screen.blit(myBall, coor)
    pygame.display.flip()
def start():
    global screen
    screen = pygame.display.set_mode((521, 491))
    screen.blit(pygame.image.load('screen4line.png'), (0, 0))
    pygame.display.set_caption("game")
    pygame.display.flip()
    pygame.init()
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render('turn of:', False, (0, 0, 0))
    screen.blit(textsurface, (190, 455))
    pygame.display.flip()
def printWinner():
    pygame.font.init()
    myfont = pygame.font.SysFont('Comic Sans MS', 20)
    textsurface = myfont.render('winner!', False, (0, 0, 0))
    screen.blit(textsurface, (312, 455))
    pygame.display.flip()
def trans(KEY):
    if KEY == pygame.K_0:
        return 0
    elif KEY == pygame.K_1:
        return 1
    elif KEY == pygame.K_2:
        return 2
    elif KEY == pygame.K_3:
        return 3
    elif KEY == pygame.K_4:
        return 4
    elif KEY == pygame.K_5:
        return 5
    elif KEY == pygame.K_6:
        return 6
    else:
        return -1
def findX(k):
    for i in range(6):
        if A[6-i-1][k] ==0:
            return 6-i-1
    return -1
def chooseColor(turn):
    if turn % 2 == 0:
        return BLUE
    else:
        return RED
def printTurn(turn):
    myColor = RED
    if turn % 2 == 1:
        myColor = RED
    else:
        myColor = BLUE
    coor = (268,455)
    myBall = pygame.image.load(myColor)
    screen.blit(myBall, coor)
    pygame.display.flip()
def equal(a,b,c,d):
    if a == b and a ==c and a == d and a != 0:
        return True
    return False
def check_win():
    for i in range(6):
        for j in range(4):
            if equal(A[i][j],A[i][j+1],A[i][j+2],A[i][j+3]):
                return A[i][j]
    for i in range(7):
        for j in range(3):
            if equal(A[j][i],A[j+1][i],A[j+2][i],A[j+3][i]):
                return A[j][i]
    for i in range(3):
        for j in range(4):
            if equal(A[i][j],A[i+1][j+1],A[i+2][j+2],A[i+3][j+3]):
                return A[i][j]
    for i in range(3,6):
        for j in range(4):
            if equal(A[i][j],A[i-1][j+1],A[i-2][j+2],A[i-3][j+3]):
                return A[i][j]

    return 0
def makeRand():
    x = 0
    while x < 100:
        x +=1
        myAnswer = random.randrange(7)
        if findX(myAnswer) != -1:
            return myAnswer
    return -1
def check_king(k):
    counter = 0
    for i in range(7):
        f = findX(i)
        if f > -1:
            A[f][i] = k
            if check_win():
                counter+=1
            A[f][i] = 0
    return counter
def first_respone(k):
    e = k % 2 + 1
    for i in range(7):
        f = findX(i)
        if f > -1:
            A[f][i] = k
            if check_win():
                A[f][i] = 0
                return (i, "win")
            A[f][i] = e
            if check_win():
                A[f][i] = 0
                return (i, "block")
            A[f][i] = 0
    return (-1, "default")

def second_respone(k):
    e = k % 2 + 1
    for i in range(7):
        f = findX(i)
        if f > -1:
            A[f][i] = e
            c = check_king(e)
            A[f][i] = 0
            if c > 1:
                return (i, "queen")
    return (-1, "default")
def find_dangers(k):
    e = k % 2 + 1
    danger = []
    for i in range(7):
        f = findX(i)
        if f > 0:
            A[f][i] = k
            A[f - 1][i] = e
            if check_win() == True:
                danger.append(i)
            A[f - 1][i] = 0
            A[f][i] = 0
    return danger
def smart(k):
    e = k%2 + 1
    for i in range(7):
        f = findX(i)
        if f > -1:
            A[f][i] = e
            (m , str) = first_respone(k)
            if str == "block" and findX(m) > -1 and m in find_dangers(k):
                    print("im smarter than u " , i)
                    A[f][i] = 0
                    return (i , "smart")
            A[f][i] = 0
    return (-1 , "default")

def robot2(k , timer):
    (myAnswer , str) = first_respone(k)
    if myAnswer != -1:
        return (myAnswer , str)
    (myAnswer, str) = smart(k)
    if myAnswer != -1:
        return (myAnswer, str)
    danger = find_dangers(k)
    (myAnswer, str) = second_respone(k)
    if myAnswer != -1 and myAnswer not in danger:
        print(myAnswer, "queen")
        return (myAnswer , str)
    m = makeRand()
    while m in danger:
        m = makeRand()
    return (m , "default")

start()
a=0
b=0
turn = 0
printTurn(turn)
finish = False
count=0
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
        k = -1
        newX = -1
        if turn % 2 == 1:
            (k , str) = robot2(turn % 2 + 1 , 0)
        else:
            if event.type == pygame.KEYDOWN:
                k = trans(event.key)
        if k >=0 and k<7:
            newX = findX(k)
            if newX == -1:
                break
            A[newX][k] = turn % 2 + 1
            func(k, newX, chooseColor(turn))
            if check_win():
                printWinner()
                while not finish:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            finish = True
                break
            turn += 1
            printTurn(turn)