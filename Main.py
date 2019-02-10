# kmj0205 - https://github.com/kmj0205
# kmj0205 - SnakeGame

import os 
import sys
import pygame as pythonGameEngine
import random

Caption = "Kmj0205 Snake Game"
ScreenSize = (492, 492)

Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
White = (255, 255, 255)
Gray = (128, 128, 128)
Black = (0, 0, 0)
Yellow = (225, 225, 0)
PresentlySnakeDir = 'RIGHT'
BackgroundColor = Black
EventColor = Black
pythonGameEngine.init()
os.environ["SDL_VIDEO_CENTERED"] = "TRUE"
pythonGameEngine.display.set_caption(Caption)
Screen = pythonGameEngine.display.set_mode(ScreenSize)
Clock = pythonGameEngine.time.Clock()
Fps = 60.0
GameSpeed = 30
Done = False
Run = True
Points = []
Matrix = []
SnakeCoor = []
Rows = 12
Cols = 12
Score = 0 
SnakeHeadY = 0
SnakeHeadX = 0
SoundVolume = 0.05 #[ 뮤트 = 0.00 / 원레 볼륨 = 0.05 ]
AppleX = 5
AppleY = 5
DirC, DirR = 1, 0
CellSize = 40
CellMargin = 1
SnakeHeadDetectionApple = 0
AdminMode = 0
GameOverCheck = 0
GameBackgroundAudio = pythonGameEngine.mixer.Sound("./resource/audio/BackgroundAudio.wav")
EatAppleAudio = pythonGameEngine.mixer.Sound("./resource/audio/EatAppleAudio.wav")
if SoundVolume > 0:
    GameBackgroundAudio.set_volume(SoundVolume)
    EatAppleAudio.set_volume(SoundVolume + 0.2)
else:
    GameBackgroundAudio.set_volume(SoundVolume)
    EatAppleAudio.set_volume(SoundVolume)
GameBackgroundAudio.play()

def ScorePrint(ScoreInput, x, y):
    font = pythonGameEngine.font.Font(None, 24)
    text = font.render("Score: " + str(ScoreInput).zfill(1), True, (Red))
    textRect = text.get_rect()
    textRect.centery = x
    textRect.centery = y
    Screen.blit(text, textRect)

def AdminModePrint(FpsInput, GameSpeedInput, SnakeHeadXInput, SnakeHeadYInput, AppleXInput, AppleYInput, x, y):
    font = pythonGameEngine.font.Font(None, 24)
    text = font.render("Fps(" + str(FpsInput).zfill(1) + ") / GameSpeed(" + str(GameSpeedInput).zfill(1) + ") / Snake(" + str(SnakeHeadXInput).zfill(1) + "," + str(SnakeHeadYInput).zfill(1) + ") / Apple(" + str(AppleXInput).zfill(1) + "," + str(AppleYInput).zfill(1) + ")", True, (White))
    textRect = text.get_rect()
    textRect.centery = x
    textRect.centery = y
    Screen.blit(text, textRect)

def BoardInit():
    global Matrix
    Matrix = []
    Onerow = []
    for x in range(0, Rows):
        for y in range(0, Cols):
            Onerow.append(9) if y == 0 or y == (Cols - 1) or x == 0 or x == (Rows - 1) else Onerow.append(0)
        Matrix.append(Onerow)
        Onerow = []

def GameDataInit():
    BoardInit()
    SnakeCoor.append([1, 1])
    
def Forward():
    R, C = SnakeCoor[0]
    R += DirR
    C += DirC
    SnakeCoor.insert(0, (R, C))
    SnakeCoor.pop(-1)

def SetDir(c, r):
    global DirC, DirR
    DirC = c
    DirR = r

def EventLoop():
    global Run  
    for Event in pythonGameEngine.event.get():
        Keys = pythonGameEngine.key.get_pressed()
        if Event.type == pythonGameEngine.QUIT or Keys[pythonGameEngine.K_ESCAPE]:
            Run = False
        elif Event.type == pythonGameEngine.MOUSEBUTTONDOWN and Event.button == 1:
            pass
        elif Event.type == pythonGameEngine.MOUSEBUTTONUP and Event.button == 1:
            Pos = pythonGameEngine.mouse.get_pos()
            Points.append(Pos)
            print("Mouse Clicked:{}, {}".format(Pos[0], Pos[1]))
        elif Event.type == pythonGameEngine.KEYDOWN:
            Key = Event.unicode
            print('Key Pressed :{}'.format(Key))
            ProcessKey(Event.key)

def ProcessKey(Key):
    global AdminMode,GameSpeed,PresentlySnakeDir
    if Key == pythonGameEngine.K_LEFT:
        if PresentlySnakeDir != 'RIGHT':
            PresentlySnakeDir = 'LEFT'
            SetDir(-1, 0)
    elif Key == pythonGameEngine.K_RIGHT:
        if PresentlySnakeDir != 'LEFT':
            PresentlySnakeDir = 'RIGHT'
            SetDir(1, 0)
    elif Key == pythonGameEngine.K_UP:
        if PresentlySnakeDir != 'DOWN':
            PresentlySnakeDir = 'UP'
            SetDir(0, -1)
    elif Key == pythonGameEngine.K_DOWN:
        if PresentlySnakeDir != 'UP':
            PresentlySnakeDir = 'DOWN'
            SetDir(0, 1)
    elif Key == pythonGameEngine.K_a:
        if PresentlySnakeDir != 'RIGHT':
            PresentlySnakeDir = 'LEFT'
            SetDir(-1, 0)
    elif Key == pythonGameEngine.K_d:
        if PresentlySnakeDir != 'LEFT':
            PresentlySnakeDir = 'RIGHT'
            SetDir(1, 0)
    elif Key == pythonGameEngine.K_w:
        if PresentlySnakeDir != 'DOWN':
            PresentlySnakeDir = 'UP'
            SetDir(0, -1)
    elif Key == pythonGameEngine.K_s:
        if PresentlySnakeDir != 'UP':
            PresentlySnakeDir = 'DOWN'
            SetDir(0, 1)
    if AdminMode == 1:
        if Key == pythonGameEngine.K_MINUS:
            print("Minus GameSpeed")
            GameSpeed += 1
        elif Key == pythonGameEngine.K_EQUALS:
            print("Plus GameSpeed")
            if(GameSpeed > 6):
                GameSpeed -= 1
    if Key == pythonGameEngine.K_SLASH:
        if AdminMode == 0 :
            print('Trun On Admin System')
            AdminMode = 1
        elif AdminMode == 1 :
            print('Trun Off Admin System')
            AdminMode = 0
    else:
        pass

def SnakeEatApple():
    global SnakeCoor,EatAppleAudio,GameSpeed,EventColor,Fps,Score
    EatAppleAudio.play()
    EventColor = Yellow
    Score += 5000
    if GameSpeed > 6:
        GameSpeed -= 1
    X = SnakeCoor[-1][:] 
    SnakeCoor.append(X)

def ObjectDrawBoard():
    global EventColor
    for R in range(Rows):
        for C in range(Cols):
            Color = EventColor if Matrix[R][C] == 9 else Gray
            pythonGameEngine.draw.rect(Screen, Color, (C*(CellSize + CellMargin), R*(CellSize+CellMargin), CellSize, CellSize)) 
    if EventColor == Yellow:
        EventColor = Black

def ObjectDrawSnake():
    global AppleX,AppleY,SnakeHeadX,SnakeHeadY,SnakeHeadDetectionApple
    for Idx, Pos in enumerate(SnakeCoor):
        Color = Blue if Idx == 0 else Green
        SnakeX = Pos[1]
        SnakeY = Pos[0]
        if Idx == 0:
            SnakeHeadX = Pos[1]; SnakeHeadY = Pos[0]
            if AppleX == SnakeHeadX:
                if AppleY == SnakeHeadY:
                    SnakeHeadDetectionApple = 1
        pythonGameEngine.draw.rect(Screen, Color, (SnakeX*(CellSize + CellMargin), SnakeY*(CellSize + CellMargin), CellSize, CellSize))

def ObjectDrawApple():
    global AppleX,AppleY,SnakeHeadDetectionApple
    if SnakeHeadDetectionApple == 1:
        SnakeHeadDetectionApple = 0
        SnakeEatApple()
        Done = False
        while not Done:
            Done = True
            AppleX = random.randrange(1, 11)
            AppleY = random.randrange(1, 11)
            for Idx, Pos in enumerate(SnakeCoor):
                Color = Blue if Idx == 0 else Green
                SnakeX = Pos[1]; SnakeY = Pos[0]
                if Idx == 0:
                    SnakeHeadX = Pos[1]; SnakeHeadY = Pos[0]
                if AppleX == SnakeX:
                    if AppleY == SnakeY:
                        Done = False
    Color = Red
    pythonGameEngine.draw.rect(Screen, Color, (AppleX*(CellSize + CellMargin), AppleY*(CellSize + CellMargin), CellSize, CellSize))

def ShowString():
    global Score,SnakeHeadX,SnakeHeadY,AppleX,AppleY,SnakeHeadX,SnakeHeadY,GameSpeed,Fps,AdminMode
    Score += 1
    ScorePrint(Score, 10, 10)
    if AdminMode == 1:
        AdminModePrint(Fps, GameSpeed ,SnakeHeadX, SnakeHeadY, AppleX, AppleY, 10, 25)

def GameOver():
    global SnakeHeadX,SnakeHeadY,GameOverCheck,Run,DieAudio,AppleX,AppleY,SnakeHeadDetectionApple
    X = 0
    GameOverCheck=0
    if 1 > SnakeHeadX:
        GameOverCheck = 1
    elif 10 < SnakeHeadX:
        GameOverCheck = 1
    elif 1 > SnakeHeadY:
        GameOverCheck = 1
    elif 10 < SnakeHeadY:
        GameOverCheck = 1

    for Idx, Pos in enumerate(SnakeCoor):
        Color = Blue if Idx == 0 else Green
        SnakeX = Pos[1]; SnakeY = Pos[0]
        if Idx == 0:
            SnakeHeadX = Pos[1]; SnakeHeadY = Pos[0]
        if X > 3:
            if SnakeX == SnakeHeadX:
                if SnakeY == SnakeHeadY:
                    GameOverCheck = 1
        X += 1

    if GameOverCheck == 1:
        Run = False

def MainLoop():
    Count = 0
    while Run:
        EventLoop()
        if Count % GameSpeed == 0:
            Forward()
            Count = 0
        Screen.fill(BackgroundColor)
        ObjectDrawBoard()
        ObjectDrawSnake()
        ObjectDrawApple()
        ShowString()
        pythonGameEngine.display.update()
        Count += 1
        Clock.tick(Fps)
        GameOver()

def main():
    GameDataInit()
    MainLoop()
    pythonGameEngine.quit()
    #sys.exit()

if __name__ == "__main__":
    main()