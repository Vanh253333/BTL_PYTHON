import random, time, pygame, sys
from pygame.locals import *

screenWidth = 640 # chiều rộng của cửa sổ
screenHeight = 480 # chiều cao của cửa sổ
blockSize = 20 # kích thước của một ô gạch
boardWidth = 10 # chiều rộng của cấu trúc bảng
boardHeight = 20 # chiều cao của cấu trúc bảng
tetrominoLength = 5 # độ dài ma trận shape

x_margin = int((screenWidth - boardWidth * blockSize) / 2)
y_margin = screenHeight - (boardHeight * blockSize) - 10

white = (255, 255, 255)
gray = (155, 155, 155)
black = (0, 0, 0)
light_red = (255, 0, 0)
red = (200, 50, 50)
light_green = (0, 255, 0)
green = (20, 185, 20)
light_blue = (0, 0, 255)
blue = (20, 20, 200)
light_yellow = (255, 255, 0)
yellow = (200, 200, 20)
light_purple = (162, 0, 124)
purple = (120, 0, 98)
light_pink = (223, 53, 57)
pink = (200, 46, 49)

colors = (blue, green, red, yellow, purple, pink, gray)
light_colors = (light_blue, light_green, light_red, light_yellow, light_purple, light_pink, white)

S_shape = [['.....',
            '.....',
            '..OO.',
            '.OO..',
            '.....'],
           ['.....',
            '..O..',
            '..OO.',
            '...O.',
            '.....']]
Z_shape = [['.....',
            '.....',
            '.OO..',
            '..OO.',
            '.....'],
           ['.....',
            '..O..',
            '.OO..',
            '.O...',
            '.....']]
I_shape = [['..O..',
            '..O..',
            '..O..',
            '..O..',
            '.....'],
           ['.....',
            '.....',
            'OOOO.',
            '.....',
            '.....']]
O_shape = [['.....',
            '.....',
            '.OO..',
            '.OO..',
            '.....']]
J_shape = [['.....',
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
L_shape = [['.....',
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
T_shape = [['.....',
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
shapes = {'S': S_shape,
          'Z': Z_shape,
          'J': J_shape,
          'L': L_shape,
          'I': I_shape,
          'O': O_shape,
          'T': T_shape}

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

def mainMenu():
    global surface, smallFont, bigFont
    pygame.init()
    surface = pygame.display.set_mode((screenWidth, screenHeight))
    smallFont = pygame.font.SysFont('comicsans', 17)
    bigFont = pygame.font.SysFont('comicsans', 100)
    pygame.display.set_caption('Tetromino')
    drawTextScreen('Tetromino')

    icon = pygame.image.load('tetris.png')
    pygame.display.set_icon(icon)

    while True:  # game loop
        pygame.mixer.music.load('tetris_BGMUSIC.mp3')
        pygame.mixer.music.play(-1, 0.0)
        mainRun()
        pygame.mixer.music.stop()
        drawTextScreen('Game Over')

def mainRun():
    # thiết lập các biến bắt đầu game
    background = pygame.image.load('tetris_bg.jpg')
    board = createBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingLeft = False
    movingRight = False
    score = 0
    combo = 0
    level, fallTime = cal_LevelAndFallTime(score)
    fallingPiece = createNewPiece()
    nextPiece1 = createNewPiece()
    nextPiece2 = createNewPiece()
    while True:  # main game loop
        if fallingPiece == None:
            # khi ko có piece nào rơi xuống, bắt đầu một piece khác
            fallingPiece = nextPiece1
            nextPiece1 = nextPiece2
            nextPiece2 = createNewPiece()
            lastFallTime = time.time()  # đặt lại lastFallTime
            if not checkValidPos(board, fallingPiece):
                return  #game kết thúc khi ko còn chỗ chứa piece tiếp theo

        checkQuitEvent()
        updateScore(score)
        for event in pygame.event.get():  # vòng lặp xl sự kiện
            if event.type == KEYUP:
                if (event.key == K_p):
                    pygame.mixer.music.stop()
                    drawTextScreen('Paused')
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
                if (event.key == K_LEFT) and checkValidPos(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_RIGHT) and checkValidPos(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()

                # xoay các piece ~
                elif (event.key == K_UP):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(shapes[fallingPiece['shape']])
                    if not checkValidPos(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(shapes[fallingPiece['shape']])

                # Nhấn phím xuống để di chuyển nhanh hơn
                elif (event.key == K_DOWN):
                    movingDown = True
                    if checkValidPos(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                # Nhấn space để piece di chuyển luôn xuống đáy
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, boardHeight):
                        if not checkValidPos(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        # di chuyển sang hai bên bằng nhấn giữ phím
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > 0.15:
            if movingLeft and checkValidPos(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and checkValidPos(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()
        # di chuyển xuống dưới bằng nhấn giữ phím
        if movingDown and time.time()-lastMoveDownTime > 0.1 and checkValidPos(board,fallingPiece,adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        # để rơi tự nhiên
        if time.time() - lastFallTime > fallTime:
            if not checkValidPos(board, fallingPiece, adjY=1):
                # nếu fallingPiece đã rơi xuống đáy, cập nhật vào board
                updateToBoard(board, fallingPiece)
                lines = removeFullLines(board)
                score += lines
                if lines > 1:
                    combo += 1
                level, fallTime = cal_LevelAndFallTime(score)
                fallingPiece = None
            else: # nếu ko tiếp tục di chuyển xuống
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        # vẽ mọi thứ lên cửa sổ
        surface.blit(background, (0, 0))
        drawBoard(board)
        drawGrid()
        lastScore = maxScore()
        drawStatus(score, level, lastScore, combo)
        drawNextPiece(nextPiece1, nextPiece2)
        if fallingPiece != None:
            tmp = fallingPiece['y']
            drawPiece(fallingPiece)
            drawShadowPiece(findShadowPos(fallingPiece, board))
            fallingPiece['y'] = tmp
        pygame.display.update()

def checkKeyPressEvent():
    checkQuitEvent()
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None

def drawTextScreen(text):
    # vẽ bóng đổ cho chữ to owr center
    titleSurf = bigFont.render(text, True, gray)
    titleRect = titleSurf.get_rect()
    titleRect.center = (int(screenWidth / 2), int(screenHeight / 2))
    surface.blit(titleSurf, titleRect)
    # vẽ dòng chữ to ở center
    titleSurf = bigFont.render(text, True, white)
    titleRect = titleSurf.get_rect()
    titleRect.center = (int(screenWidth / 2)-3, int(screenHeight / 2)-3)
    surface.blit(titleSurf, titleRect)
    #  vẽ dòng chữ phía dưới
    mediumFont = pygame.font.SysFont('comicsans', 40)
    titleSurf = mediumFont.render('Press Any Key To Play.', True, white)
    surface.blit(titleSurf, (int(screenWidth / 5), int(screenHeight / 2) + 100))

    while checkKeyPressEvent() == None:
        pygame.display.update()

def checkQuitEvent():
    for event in pygame.event.get(QUIT): #thoát game khi bấm  chọn tắt
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP): #thoát game khi nhấn phím esc
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)

def cal_LevelAndFallTime(score):
    level = int(score / 10) + 1
    fallTime = 0.27 - (level * 0.01)
    return level, fallTime

def createNewPiece():
    shape = random.choice(list(shapes.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(shapes[shape]) - 1),
                'x': int(boardWidth / 2) - int(5 / 2),
                'y': -2,  # xuất hiện trên giữa đầu board
                'color': random.randint(0, len(colors) - 1)}
    return newPiece

def updateToBoard(board, piece):
    for x in range(tetrominoLength):
        for y in range(tetrominoLength):
            if shapes[piece['shape']][piece['rotation']][y][x] != '.':
                board[x + piece['x']][y + piece['y']] = piece['color']

def createBoard():
    board = []
    for i in range(boardWidth):
        board.append(['.'] * boardHeight)
    return board

def checkOnBoard(x, y):
    return x >= 0 and x < boardWidth and y < boardHeight

def checkValidPos(board, piece, adjX=0, adjY=0):
    for x in range(tetrominoLength):
        for y in range(tetrominoLength):
            if y + piece['y'] + adjY < 0 or shapes[piece['shape']][piece['rotation']][y][x] == '.':
                continue
            if not checkOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != '.':
                return False
    return True

def checkFullLine(board, y):
    for x in range(boardWidth):
        if board[x][y] == '.':
            return False
    return True

def removeFullLines(board):
    lines = 0 # số hàng phải xóa
    y = boardHeight - 1
    while y >= 0:
        if checkFullLine(board, y):
            # xóa hàng và sao chép các giá trị phía trên xuống
            for pushDownY in range(y, 0, -1):
                for x in range(boardWidth):
                    board[x][pushDownY] = board[x][pushDownY - 1]
                board[x][0] = '.'
            lines += 1
        else:
            y -= 1
    return lines

def drawBox(block_x, block_y, color, coord_x=None, coord_y=None):
    if color == '.':
        return
    if coord_x == None and coord_y == None:
        coord_x, coord_y = (x_margin + (block_x * blockSize)), (y_margin + (block_y * blockSize))
    pygame.draw.rect(surface, colors[color], (coord_x + 1, coord_y + 1, blockSize - 1, blockSize - 1))
    pygame.draw.rect(surface, light_colors[color], (coord_x +3, coord_y +3, blockSize - 5, blockSize - 5))

def findShadowPos(fallingPiece, board):
    shadow = fallingPiece
    for i in range(1, boardHeight):
        if not checkValidPos(board, shadow, adjY=i):
            break
    shadow['y'] += i-1
    return shadow

def drawShadowPiece(shadow):
    shapeToDraw = shapes[shadow['shape']][shadow['rotation']]
    coord_x, coord_y = (x_margin + (shadow['x'] * blockSize)), (y_margin + (shadow['y'] * blockSize))
    for x in range(tetrominoLength):
        for y in range(tetrominoLength):
            if shapeToDraw[y][x] != '.':
                drawBoxShadow(shadow['color'], coord_x + (x * blockSize), coord_y + (y * blockSize))

def drawBoxShadow(color, coord_x, coord_y):
    if color == '.':
        return
    pygame.draw.rect(surface, colors[color], (coord_x, coord_y, blockSize, blockSize), 1)

def drawBoard(board):
    pygame.draw.rect(surface, white, (x_margin, y_margin, boardWidth * blockSize, boardHeight * blockSize), 10)
    pygame.draw.rect(surface, black, (x_margin, y_margin, boardWidth * blockSize, boardHeight * blockSize), 0)
    for x in range(boardWidth):
        for y in range(boardHeight):
            drawBox(x, y, board[x][y])

def drawStatus(score, level, lastScore, combo):
    pygame.draw.rect(surface, white, (15, 80, 150, 150), 5)
    pygame.draw.rect(surface, black, (15, 80, 150, 150))
    # score text
    scoreSurf = smallFont.render('Score: ' + str(score), True, white)
    surface.blit(scoreSurf, (30, 90))
    # level text
    levelSurf = smallFont.render('Level: ' + str(level), True, white)
    surface.blit(levelSurf, (30, 125))
    # highscore text
    highcoreSurf = smallFont.render('High Score: ' + lastScore, True, white)
    surface.blit(highcoreSurf, (30, 160))
    # combo text
    comboSurf = smallFont.render('Combo: ' + str(combo), True, white)
    surface.blit(comboSurf, (30, 195))

def drawPiece(piece, coord_x=None, coord_y=None):
    shapeToDraw = shapes[piece['shape']][piece['rotation']]
    if coord_x == None and coord_y == None:
        coord_x, coord_y = (x_margin + (piece['x'] * blockSize)), (y_margin + (piece['y'] * blockSize))
    for x in range(tetrominoLength):
        for y in range(tetrominoLength):
            if shapeToDraw[y][x] != '.':
                drawBox(None, None, piece['color'], coord_x + (x * blockSize), coord_y + (y * blockSize))

def drawNextPiece(piece1, piece2):
    pygame.draw.rect(surface, white, (475, 80, 150, 240), 5)
    pygame.draw.rect(surface, black, (475, 80, 150, 240))
    # chữ Next Shape
    nextSurf = smallFont.render('Next Shape:', True, white)
    surface.blit(nextSurf, (screenWidth - 150, 90))
    # vẽ next piece
    drawPiece(piece1, coord_x=screenWidth - 120, coord_y=120)
    drawPiece(piece2, coord_x=screenWidth - 120, coord_y=220)

def drawGrid():
    for i in range(boardHeight):
        pygame.draw.line(surface, (33, 21, 81), (x_margin, y_margin + i * blockSize),
                         (x_margin + 200, y_margin + i * blockSize))
        for j in range(boardWidth):
            pygame.draw.line(surface, (33, 21, 81), (x_margin + j * blockSize, y_margin),
                             (x_margin + j * blockSize, y_margin + 400))

if __name__ == '__main__':
    mainMenu()
