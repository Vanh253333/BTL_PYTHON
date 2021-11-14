import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10
BOARDHEIGHT = 20
BLANK = '.'

XMARGIN = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE) / 2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGHT * BOXSIZE) - 5

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)
LIGHTRED = (255, 0, 0)
RED = (200, 20, 20)
LIGHTGREEN = (0, 255, 0)
GREEN = (20, 185, 20)
LIGHTBLUE = (0, 0, 255)
BLUE = (20, 20, 200)
LIGHTYELLOW = (255, 255, 0)
YELLOW = (200, 200, 20)
LIGHTPURPLE = (162, 0, 124)
PURPLE = (120, 0, 98)
LIGHTPINK = (223, 53, 57)
PINK = (200, 46, 49)

BORDERCOLOR = WHITE # màu viền khung
BGCOLOR = BLACK # màu nền khung
TEXTCOLOR = WHITE # màu chữ hiển thị trên màn hình
TEXTSHADOWCOLOR = GRAY # màu bóng chữ hiển thị
COLORS = (BLUE, GREEN, RED, YELLOW, PURPLE, PINK, GRAY)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTRED, LIGHTYELLOW, LIGHTPURPLE, LIGHTPINK, WHITE)
assert len(COLORS) == len(LIGHTCOLORS)  # mỗi một color phải có 1 light color
TEMPLATEWIDTH = 5
TEMPLATEHEIGHT = 5
S_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '..OO.',
                     '.OO..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '...O.',
                     '.....']]
Z_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '.O...',
                     '.....']]
I_SHAPE_TEMPLATE = [['..O..',
                     '..O..',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     'OOOO.',
                     '.....',
                     '.....']]
O_SHAPE_TEMPLATE = [['.....',
                     '.....',
                     '.OO..',
                     '.OO..',
                     '.....']]
J_SHAPE_TEMPLATE = [['.....',
                     '.O...',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..OO.',
                     '..O..',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '...O.',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '.OO..',
                     '.....']]
L_SHAPE_TEMPLATE = [['.....',
                     '...O.',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..O..',
                     '..OO.',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '.O...',
                     '.....'],
                    ['.....',
                     '.OO..',
                     '..O..',
                     '..O..',
                     '.....']]
T_SHAPE_TEMPLATE = [['.....',
                     '..O..',
                     '.OOO.',
                     '.....',
                     '.....'],
                    ['.....',
                     '..O..',
                     '..OO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '.....',
                     '.OOO.',
                     '..O..',
                     '.....'],
                    ['.....',
                     '..O..',
                     '.OO..',
                     '..O..',
                     '.....']]
SHAPES = {'S': S_SHAPE_TEMPLATE,
          'Z': Z_SHAPE_TEMPLATE,
          'J': J_SHAPE_TEMPLATE,
          'L': L_SHAPE_TEMPLATE,
          'I': I_SHAPE_TEMPLATE,
          'O': O_SHAPE_TEMPLATE,
          'T': T_SHAPE_TEMPLATE}

def updateScore(nscore):
    score = maxScore()
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def maxScore():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.SysFont('Cooper Black', 17)
    BIGFONT = pygame.font.SysFont('comicsans', 100)
    pygame.display.set_caption('Tetromino')
    showTextScreen('Tetromino')

    icon = pygame.image.load('tetris.png')
    pygame.display.set_icon(icon)

    while True:  # game loop
        pygame.mixer.music.load('tetris_BGMUSIC.mp3')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    # thiết lập các biến bắt đầu game ~
    background = pygame.image.load('tetris_bg.jpg')
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:  # main game loop
        if fallingPiece == None:
            # khi ko có piece nào rơi xuống, bắt đầu một piece khác
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()  # đặt lại lastFallTime
            if not isValidPosition(board, fallingPiece):
                return  #game kết thúc khi ko còn chỗ chứa piece tiếp theo

        checkForQuit()
        updateScore(score)
        for event in pygame.event.get():  # vòng lặp xl sự kiện
            if event.type == KEYUP:
                if (event.key == K_p):
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_LEFT):
                    movingLeft = False
                elif (event.key == K_RIGHT):
                    movingRight = False
                elif (event.key == K_DOWN):
                    movingDown = False

            elif event.type == KEYDOWN:
                if (event.key == K_LEFT) and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT) and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # xoay các piece ~
                elif (event.key == K_UP):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(SHAPES[fallingPiece['shape']])

                # Nhấn phím xuống để di chuyển nhanh hơn~
                elif (event.key == K_DOWN):
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                # Nhấn space để piece di chuyển luôn xuống đáy
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # di chuyển sang hai bên bằng nhấn giữ phím
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        # di chuyển xuống dưới bằng nhấn giữ phím
        if movingDown and time.time()-lastMoveDownTime>MOVEDOWNFREQ and isValidPosition(board,fallingPiece,adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # để rơi tự nhiên
        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY=1):
                # nếu fallingPiece đã rơi xuống đáy, cập nhật vào board
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else: # nếu ko tiếp tục di chuyển xuống
                fallingPiece['y'] += 1
                lastFallTime = time.time()
        # vẽ mọi thứ lên windown nào ~
        DISPLAYSURF.blit(background, (0, 0))
        drawBoard(board)
        drawGrid()
        lastScore = maxScore()
        drawStatus(score, level, lastScore)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def terminate():
    pygame.quit()
    sys.exit()

def checkForKeyPress():
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def showTextScreen(text):
    # vẽ bóng đổ cho chữ to
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)
    # vẽ dòng chữ to ở center
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, WHITE)
    titleRect.center = (int(WINDOWWIDTH / 2) - 3, int(WINDOWHEIGHT / 2) - 3)
    DISPLAYSURF.blit(titleSurf, titleRect)
    #  vẽ dòng chữp hía dưới
    font = pygame.font.SysFont('comicsans', 40)
    pressKeySurf, pressKeyRect = makeTextObjs('Press Any Key To Play.', font, LIGHTYELLOW)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick()

def checkForQuit():
    for event in pygame.event.get(QUIT): #thoát game khi bấm  chọn tắt
        terminate()
    for event in pygame.event.get(KEYUP): #thoát game khi nhấn phím esc
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def calculateLevelAndFallFreq(score):
    level = int(score / 10) + 1
    fallFreq = 0.27 - (level * 0.01)
    return level, fallFreq

def getNewPiece():
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(SHAPES[shape]) - 1),
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),
                'y': -2,  # xuất hiện trên giữa đầu board
                'color': random.randint(0, len(COLORS) - 1)}
    return newPiece

def addToBoard(board, piece):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

def getBlankBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)
    return board

def isOnBoard(x, y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:
                return False
    return True

def isCompleteLine(board, y):
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:
            return False
    return True

def removeCompleteLines(board):
    numLinesRemoved = 0 # số hàng phải xóa
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):
            # xóa hàng và di chuyển các box xuống
            for pullDownY in range(y, 0, -1):
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY - 1]
                board[x][0] = BLANK
            numLinesRemoved += 1
        else:
            y -= 1
    return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(boxx, boxy, color, pixelx=None, pixely=None):
    if color == BLANK:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(board):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN, TOPMARGIN, (BOARDWIDTH * BOXSIZE), (BOARDHEIGHT * BOXSIZE)),10)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(x, y, board[x][y])

def drawStatus(score, level, lastScore):
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (475, 10, 150, 225), 5)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (475, 10, 150, 225))
    # score text
    scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    # evel text
    levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)
    # highscore
    highcoreSurf = BASICFONT.render('High Score: ' + lastScore, True, TEXTCOLOR)
    highcorect = highcoreSurf.get_rect()
    highcorect.topleft = (WINDOWWIDTH - 150, 200)
    DISPLAYSURF.blit(highcoreSurf, highcorect)

def drawPiece(piece, pixelx=None, pixely=None):
    shapeToDraw = SHAPES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(piece):
    # chữ Next Shape
    nextSurf = BASICFONT.render('Next Shape:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 150, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    # vẽ next piece
    drawPiece(piece, pixelx=WINDOWWIDTH - 120, pixely=100)

def drawGrid():
    for i in range(BOARDHEIGHT):
        pygame.draw.line(DISPLAYSURF, (33, 21, 81), (XMARGIN, TOPMARGIN + i * BOXSIZE),
                         (XMARGIN + 200, TOPMARGIN + i * BOXSIZE))
        for j in range(BOARDWIDTH):
            pygame.draw.line(DISPLAYSURF, (33, 21, 81), (XMARGIN + j * BOXSIZE, TOPMARGIN),
                             (XMARGIN + j * BOXSIZE, TOPMARGIN + 400))

if __name__ == '__main__':
    main()
