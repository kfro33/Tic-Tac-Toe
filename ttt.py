import pygame as pg, sys
from pygame.locals import *
import time

# init global variables
XO = 'x'
winner = None
draw = False
width = 400
height = 400
white = (255, 255, 255)
line_color = (10, 10, 10)

# Tic Tac Toe 3x3 Board
TTTB = [[None] * 3, [None] * 3, [None] * 3]

# init pygame window
pg.init()
fps = 30
clock = pg.time.Clock()
screen = pg.display.set_mode((width, height + 100), 0, 32)
pg.display.set_caption("Tic Tac Toe")

# load images
opening = pg.image.load('ttopen.png')
ximage = pg.image.load('X.png')
oimage = pg.image.load('O.png')

# resize image
opening = pg.transform.scale(opening, (width, height + 100))
ximage = pg.transform.scale(ximage, (80, 80))
oimage = pg.transform.scale(oimage, (80, 80))

def game_opening():
    screen.blit(opening, (0, 0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    # draw vert lines
    pg.draw.line(screen, line_color, (width/3, 0), (width/3, height), 7)
    pg.draw.line(screen, line_color, (width/3*2, 0), (width/3*2, height), 7)

    # draw horz lines
    pg.draw.line(screen, line_color, (0, height/3), (width, height/3), 7)
    pg.draw.line(screen, line_color, (0, height/3*2), (width, height/3*2), 7)
    draw_stat()

def draw_stat():
    global draw

    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + ' Won!'
    if draw:
        message = "Game Draw!"
    
    font = pg.font.Font(None, 30)
    text = font.render(message, 1, (255, 255, 255))

    # copy rendered message onto board
    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pg.display.update()

def check_win():
    global TTTB, winner, draw

    # check for win row
    for row in range(0, 3):
        if ((TTTB[row][0] == TTTB[row][1] == TTTB[row][2]) and (TTTB[row][0] is not None)):
            winner = TTTB[row][0]
            pg.draw.line(screen, (250, 0, 0), (0, (row + 1)*height/3 - height/6),\
                        (width, (row + 1) * height/3 - height/6), 4)
            break
    
    # check for win columns
    for col in range(0, 3):
        if((TTTB[0][col] == TTTB[1][col] == TTTB[2][col]) and (TTTB[0][col] is not None)):
            winner = TTTB[0][col]
            pg.draw.line (screen, (250,0,0),((col + 1)* width/3 - width/6, 0),\
                          ((col + 1)* width/3 - width/6, height), 4)
            break

    # check for diag win
    if(TTTB[0][0] == TTTB[1][1] == TTTB[2][2]) and (TTTB[0][0] is not None):
        winner = TTTB[0][0]
        pg.draw.line(screen, (250, 70, 70), (50, 50), (350, 350), 4)

    if (TTTB[0][2] == TTTB[1][1] == TTTB[2][0]) and (TTTB[0][2] is not None):
        # diag right to left
        winner = TTTB[0][2]
        pg.draw.line(screen, (250,70,70), (350, 50), (50, 350), 4)

    if(all([all(row) for row in TTTB]) and winner is None):
        draw = True
    draw_stat()

def drawXO(row, col):
    global TTTB, XO
    if row == 1:
        posx = 30
    if row == 2:
        posx = width/3 + 30
    if row == 3:
        posx = width/3*2 + 30
    
    if col == 1:
        posy = 30
    if col == 2:
        posy = height/3 + 30
    if col == 3:
        posy = height/3*2 + 30
    TTTB[row-1][col-1] = XO
    if(XO == 'x'):
        screen.blit(ximage, (posy, posx))
        XO = 'o'
    else:
        screen.blit(oimage, (posy, posx))
        XO = 'x'
    pg.display.update()

def userClick():
    # coords of mouse click
    x,y = pg.mouse.get_pos()

    # col of mouse click
    if(x < width/3):
        col = 1
    elif(x < width/3*2):
        col = 2
    elif(x < width):
        col = 3
    else:
        col = None

    # row of mouse click
    if(y < height/3):
        row = 1
    elif(y < height/3*2):
        row = 2
    elif(y < height):
        row = 3
    else:
        row = None

    if(row and col and TTTB[row-1][col-1] is None):
        global XO

        drawXO(row, col)
        check_win()
    
def reset_game():
    global TTTB, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    game_opening()
    winner = None
    TTTB = [[None]*3, [None]*3, [None]*3]

game_opening()

while(True):
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            userClick()
            if(winner or draw):
                reset_game()
    
    pg.display.update()
    clock.tick(fps)