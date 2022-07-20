#imports
#from typing_extensions import ParamSpecArgs
import pygame
import socket
import random
import math
import time
import threading
import select
import json
from pygame import constants
from pygame.constants import MOUSEBUTTONDOWN
import pygame_widgets as pgWidgets
import copy
import threading


#init
pygame.init()

debug = 0

board_pos=[
    [(362,65),(362+84*1,65),(362+84*2,65),(362+84*3,65),(362+84*4,65),(362+84*5,65),(362+84*6,65),(362+84*7,65)],
    [(362,65+84*1),(362+84*1,65+84*1),(362+84*2,65+84*1),(362+84*3,65+84*1),(362+84*4,65+84*1),(362+84*5,65+84*1),(362+84*6,65+84*1),(362+84*7,65+84*1)],
    [(362,65+84*2),(362+84*1,65+84*2),(362+84*2,65+84*2),(362+84*3,65+84*2),(362+84*4,65+84*2),(362+84*5,65+84*2),(362+84*6,65+84*2),(362+84*7,65+84*2)],
    [(362,65+84*3),(362+84*1,65+84*3),(362+84*2,65+84*3),(362+84*3,65+84*3),(362+84*4,65+84*3),(362+84*5,65+84*3),(362+84*6,65+84*3),(362+84*7,65+84*3)],
    [(362,65+84*4),(362+84*1,65+84*4),(362+84*2,65+84*4),(362+84*3,65+84*4),(362+84*4,65+84*4),(362+84*5,65+84*4),(362+84*6,65+84*4),(362+84*7,65+84*4)],
    [(362,65+84*5),(362+84*1,65+84*5),(362+84*2,65+84*5),(362+84*3,65+84*5),(362+84*4,65+84*5),(362+84*5,65+84*5),(362+84*6,65+84*5),(362+84*7,65+84*5)],
    [(362,65+84*6),(362+84*1,65+84*6),(362+84*2,65+84*6),(362+84*3,65+84*6),(362+84*4,65+84*6),(362+84*5,65+84*6),(362+84*6,65+84*6),(362+84*7,65+84*6)],
    [(362,65+84*7),(362+84*1,65+84*7),(362+84*2,65+84*7),(362+84*3,65+84*7),(362+84*4,65+84*7),(362+84*5,65+84*7),(362+84*6,65+84*7),(362+84*7,65+84*7)]
]
#


#font
font = pygame.font.Font('freesansbold.ttf',32)

#pictures
#board
board = pygame.image.load('board.jpg')
#black pawn
b_pawn = pygame.image.load('black_pawn.png')  

b_pawn_eat = pygame.transform.scale(b_pawn, (60, 60))

b_pawn_pos=board_pos[1]

b_pawn_condition = [True,True,True,True,True,True]
#white pawn
w_pawn = pygame.image.load('white_pawn.png')

w_pawn_eat = pygame.transform.scale(w_pawn, (60, 60))

w_pawn_pos=board_pos[6]
w_pawn_condition = [True,True,True,True,True,True]
#black knight
b_knight = pygame.image.load('black_knight.png')
b_knight_eat = pygame.transform.scale(b_knight, (60, 60))
b_knight_pos=[board_pos[0][1],board_pos[0][-2]]
b_knight_condition = [True,True]
#white knight
w_knight = pygame.image.load('white_knight.png')
w_knight_eat = pygame.transform.scale(w_knight, (60, 60))
w_knight_pos=[board_pos[-1][1],board_pos[-1][-2]]
w_knight_condition = [True,True]
#black bishop
b_bishop = pygame.image.load('black_bishop.png')
b_bishop_eat = pygame.transform.scale(b_bishop, (60, 60))
b_bishop_pos=[board_pos[0][2],board_pos[0][-3]]
b_bishop_condition = [True,True]
#white bishop
w_bishop = pygame.image.load('white_bishop.png')
w_bishop_eat = pygame.transform.scale(w_bishop, (60, 60))
w_bishop_pos=[board_pos[-1][2],board_pos[-1][-3]]
w_bishop_condition = [True,True]
#black rook
b_rook = pygame.image.load('black_rook.png')

b_rook_eat = pygame.transform.scale(b_rook, (60, 60))
b_rook_pos=[board_pos[0][0],board_pos[0][-1]]
b_rook_condition = [True,True]
#white rook
w_rook = pygame.image.load('white_rook.png')

w_rook_eat = pygame.transform.scale(w_rook, (60, 60))
w_rook_pos=[board_pos[-1][0],board_pos[-1][-1]]
w_rook_condition = [True,True]
#black queen
b_queen = pygame.image.load('black_queen.png')

b_queen_eat = pygame.transform.scale(b_queen, (60, 60))
b_queen_pos=board_pos[0][3]
b_queen_condition = True
#white queen
w_queen = pygame.image.load('white_queen.png')
w_queen_eat = pygame.transform.scale(w_queen, (60, 60))
w_queen_pos=board_pos[-1][3]
w_queen_condition = True
#black king
b_king = pygame.image.load('black_king.png')
b_king_eat = pygame.transform.scale(b_king, (60, 60))
b_king_pos=board_pos[0][4]
b_king_condition = True
#white king
w_king = pygame.image.load('white_king.png')
w_king_eat = pygame.transform.scale(w_king, (60, 60))
w_king_pos=board_pos[-1][4]
w_king_condition = True
#background
game_background = pygame.image.load('background.jpg')
# troops length
troops_length = (80,80)
screen_length = (1600,900)


screen = pygame.display.set_mode(screen_length)
pygame.display.set_caption("Chess")

first_press = False
white_pawn_mooved = [False,False,False,False,False,False,False,False]
black_pawn_mooved = [False,False,False,False,False,False,False,False]
square_bool_1 = [["black rook","black knight","black bishop","black queen","black king","black bishop","black knight","black rook"],
    ["black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn"],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    ["white pawn","white pawn","white pawn","white pawn","white pawn","white pawn","white pawn","white pawn"],
    ["white rook","white knight","white bishop","white queen","white king","white bishop","white knight","white rook"]
]

square_bool = [["black rook",None,"black bishop","black queen","black king","black bishop","black knight","black rook"],
    ["black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn"],
    [None,None,"black knight",None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,"white pawn",None,None,None,None],
    [None,None,None,None,"white pawn",None,None,None],
    ["white pawn","white pawn","white pawn",None,None,"white pawn","white pawn","white pawn"],
    ["white rook","white knight","white bishop","white queen","white king","white bishop","white knight","white rook"]
]
   #game points and other


w_eaten=[]
# מה שנאכל בצבע לבן
b_eaten=[]
# מה שנאכל בצבע שחור
pawn_worth = 1
knight_worth = 3
bishop_worth = 3
rook_worth = 5
queen_worth = 8
max_points = pawn_worth+knight_worth+bishop_worth+rook_worth+queen_worth
w_points = 0
b_points = 0
sum_points = 0
w_lost = False
b_lost = False
w_king_placement = (7,4)
b_king_placement = (0,4)
b_on_check = False
w_on_check = False
w_mooved_king = False
b_mooved_king = False

w_mooved_left_rook = False
b_mooved_left_rook = False
w_mooved_right_rook = False
b_mooved_right_rook = False

w_able_to_small_castle = False
w_able_to_big_castle = False
b_able_to_small_castle = False
b_able_to_big_castle = False

w_small_clear = False
w_big_clear = False
b_small_clear = False
b_big_clear = False

b_castled = False
w_castled = False
w_time = 300
b_time = 300
startTime=time.time()
mate = False
tie = False
turn = 0

global_move=None
moves=[]
ii,jj=0,0
act=False
########
squares=[]
openning = True
running = True
game_mode =  ""
static_evaluation = 0
b_eaten_IMG = []
w_eaten_IMG = []
pawns_pos = []
pawn_reach_edge_pos = (-1,-1)
chose = False
level = 0
screen.blit(game_background, (0,0))


def check_pawn_reach_edge(color,row):
    if color == "white":
        if row == 0:
            return True
    else:
        if row == 7:
            return True
    return False
     

def calculate_board(board):
    sum_points = 0
    for i,line in enumerate(board):
        for j,player in enumerate(line):
            if board[i][j] != None:
                if "black" in board[i][j]:
                    if "pawn" in board[i][j]:
                        sum_points-= pawn_worth
                    elif "knight" in board[i][j]:
                        sum_points-= knight_worth
                    elif "bishop" in board[i][j]:
                        sum_points-= bishop_worth
                    elif "rook" in board[i][j]:
                        sum_points-= rook_worth
                    elif "queen" in board[i][j]:
                        sum_points-= queen_worth
                if "white" in board[i][j]:
                    if "pawn" in board[i][j]:
                        sum_points+= pawn_worth
                    elif "knight" in board[i][j]:
                        sum_points+= knight_worth
                    elif "bishop" in board[i][j]:
                        sum_points+= bishop_worth
                    elif "rook" in board[i][j]:
                        sum_points+= rook_worth
                    elif "queen" in board[i][j]:
                        sum_points+= queen_worth
    # if check_mate():
    #     if debug:
    #         print("calculate_board:sum_points: ",sum_points)  
    #     if turn%2==0:
    #         sum_points+=100
    #     else:
    #         sum_points-=100
    return sum_points          


def draw_image(x,y,image):
    screen.blit(image, (x,y))


def write(x,y,subject):
    something = font.render(subject,True,(0,0,175))
    screen.blit(something,(x,y))

 
def init_screen():
    screen.blit(game_background, (0,0))
    screen.blit(board,(300,0))
    for i,square in enumerate(square_bool):
        for j,value in enumerate(square):
            draw=None
            if value =="white pawn":
                draw=w_pawn
            elif value=="black pawn":
                draw=b_pawn
            elif value =="white rook":
                draw=w_rook
            elif value=="black rook":
                draw=b_rook
            elif value =="white bishop":
                draw=w_bishop
            elif value=="black bishop":
                draw=b_bishop
            elif value =="white knight":
                draw=w_knight
            elif value=="black knight":
                draw=b_knight
            elif value =="white king":
                draw=w_king
            elif value=="black king":
                draw=b_king
            elif value =="white queen":
                draw=w_queen
            elif value=="black queen":
                draw=b_queen
            if draw!=None:
                screen.blit(draw,board_pos[i][j])   


def OnClickBt1():
    global openning
    global game_mode
    game_mode = "player versus player offline"
    openning = False


def OnClickBt2():
    global openning
    global game_mode
    game_mode = "player versus computer1"
    openning = False


def OnClickBt3():
    global openning
    global game_mode
    game_mode = "player versus computer2"
    openning = False


def OnClickBt4():
    global openning
    global game_mode
    game_mode = "player versus computer3"
    openning = False


def OnClickBt5():
    global openning
    global game_mode
    game_mode = "player versus computer4"
    openning = False


def OnClickBt6():
    global openning
    global game_mode
    game_mode = "player versus player online"
    openning = False


def on_click_knight():
    global chose
    global pawn_reach_edge_pos
    global square_bool
    i,j = pawn_reach_edge_pos
    #if i != -1 and j!= -1:
    if turn%2==0:
        square_bool[i][j] = "white knight"
    else:
        square_bool[i][j] = "black knight"
    pawn_reach_edge_pos = (-1,-1)
    init_screen()
    chose = True


def on_click_queen(): 
    global  chose
    global pawn_reach_edge_pos
    i,j = pawn_reach_edge_pos
    global square_bool
    if i != -1 and j!= -1:
        if turn%2==0:
            square_bool[i][j] = "white queen"
        else:
            square_bool[i][j] = "black queen"
        pawn_reach_edge_pos = -1
        init_screen()   
        chose = True 


def opening_screen():    
    global openning
    global running
    openning = True
    pvpon_BT=pgWidgets.Button(screen,x=550,y=0,height=100,width=500,text="player vs player online",fontSize=50,onClick=OnClickBt6)
    pvpoff_BT=pgWidgets.Button(screen,x=550,y=150,height=100,width=500,text="player vs player offline",fontSize=50,onClick=OnClickBt1)
    pvc1_BT=pgWidgets.Button(screen,x=550,y=300,height=100,width=500,text="player vs computer1",fontSize=50,onClick=OnClickBt2)
    pvc2_BT=pgWidgets.Button(screen,x=550,y=450,height=100,width=500,text="player vs computer2",fontSize=50,onClick=OnClickBt3)
    pvc3_BT=pgWidgets.Button(screen,x=550,y=600,height=100,width=500,text="player vs computer3",fontSize=50,onClick=OnClickBt4)
    pvc4_BT=pgWidgets.Button(screen,x=550,y=750,height=100,width=500,text="player vs computer4",fontSize=50,onClick=OnClickBt5)
    screen.blit(board,(300,0))
    screen.blit(game_background, (0,0))
    
    while(openning):
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                openning = False
                running = False
        pvpon_BT.listen(events)
        pvpon_BT.draw()
        pvpoff_BT.listen(events)
        pvpoff_BT.draw()
        pvc1_BT.listen(events)
        pvc1_BT.draw()
        pvc2_BT.listen(events)
        pvc2_BT.draw()
        pvc3_BT.listen(events)
        pvc3_BT.draw()
        pvc4_BT.listen(events)
        pvc4_BT.draw()
        pygame.display.flip()


def back_to_menu():
    global openning
    openning = True
    restart()
    opening_screen()
    init_screen()  


def init_squares():
    global squares
    squares = []
    for i,line in enumerate(board_pos):
        squares.append([])
        for j,square in enumerate(line):
            bt=pgWidgets.Button(screen,x=square[0],y=square[1],width=84,height=84,inactiveColor=(0,220,0),pressedColour=(0, 220, 0),hoverColour=(0, 220, 0))
            #bt.draw()
            squares[i].append((bt,square_bool[i][j]))

    for i in range(len(squares)):
        for j in range(len(squares[i])):
            pos = (i,j)
            squares[i][j][0].setOnClick(OnClick,params = (pos,))


def restart():
    global square_bool
    global w_time
    global b_time
    global turn
    global squares
    global tie
    global mate
    global b_castled
    global w_castled
    global white_pawn_mooved
    global black_pawn_mooved
    global b_eaten_IMG
    global w_eaten_IMG
    global w_eaten
    global b_eaten
    mate = False
    tie = False
    b_castled = False
    w_castled = False
    w_time = 300
    b_time = 300
    turn = 0
    white_pawn_mooved = [False,False,False,False,False,False,False,False]
    black_pawn_mooved = [False,False,False,False,False,False,False,False]
    square_bool = [["black rook","black knight","black bishop","black queen","black king","black bishop","black knight","black rook"],
    ["black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn","black pawn"],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    [None,None,None,None,None,None,None,None],
    ["white pawn","white pawn","white pawn","white pawn","white pawn","white pawn","white pawn","white pawn"],
    ["white rook","white knight","white bishop","white queen","white king","white bishop","white knight","white rook"]
    ]
    w_eatenIMG=[]
    b_eatenIMG=[]
    b_eaten = []
    w_eaten = []
    init_squares()
    init_screen() 


def Timer():
    global w_time, b_time,tie,mate
    while running:
        if not openning and not check_mate():
            screen.blit(game_background, (0,0))
            screen.blit(board,(300,0))
            for i,square in enumerate(square_bool):
                for j,value in enumerate(square):
                    draw=None
                    if value =="white pawn":
                        draw=w_pawn
                    elif value=="black pawn":
                        draw=b_pawn
                    elif value =="white rook":
                        draw=w_rook
                    elif value=="black rook":
                        draw=b_rook
                    elif value =="white bishop":
                        draw=w_bishop
                    elif value=="black bishop":
                        draw=b_bishop
                    elif value =="white knight":
                        draw=w_knight
                    elif value=="black knight":
                        draw=b_knight
                    elif value =="white king":
                        draw=w_king
                    elif value=="black king":
                        draw=b_king
                    elif value =="white queen":
                        draw=w_queen
                    elif value=="black queen":
                        draw=b_queen
                    
                    if draw!=None:
                        screen.blit(draw,board_pos[i][j])   
            if not act:
                if (squares[ii][jj][1]!=None):
                    ChangeColor((150,0,0))
                    squares[ii][jj][0].draw()
                    ChangeColor((0,150, 0))   
                    for k in moves:
                        squares[k[0]][k[1]][0].draw()
            time.sleep(1)
            if turn%2==0: #white turn
                w_time-=1
            else:
                b_time -=1       


def check_casteling():
    global b_able_to_big_castle
    global b_able_to_small_castle
    global w_able_to_big_castle
    global w_able_to_small_castle
    global w_small_clear
    global w_big_clear
    global b_small_clear
    global b_big_clear
    if not w_castled:
        if square_bool[7][1] == None and square_bool[7][2] == None and square_bool[7][3] == None:
            w_big_clear = True
        else: 
            w_big_clear = False
        if square_bool[7][6] == None and square_bool[7][5] == None:
            w_small_clear = True
        else: 
            w_small_clear = False

        if w_small_clear and not w_mooved_right_rook and check(square_bool)==False and not w_mooved_king:
            w_able_to_small_castle = True
        else:
            w_able_to_small_castle = False

        if w_big_clear and not w_mooved_left_rook and check(square_bool)==False and not w_mooved_king:
            w_able_to_big_castle = True
        else:
            w_able_to_big_castle = False
    else:
        w_able_to_big_castle = False
        w_able_to_small_castle = False
    if not b_castled:
        if square_bool[0][1] == None and square_bool[0][2] == None and square_bool[0][3] == None:
            b_big_clear = True 
        else: 
            b_big_clear = False
        if square_bool[0][6] == None and square_bool[0][5] == None:
            b_small_clear = True
        else: 
            b_small_clear = False

        if b_small_clear and not b_mooved_right_rook and check(square_bool)==False and not b_mooved_king:
            b_able_to_small_castle = True
        else:
            b_able_to_small_castle = False

        if b_big_clear and not b_mooved_left_rook and check(square_bool)==False and not b_mooved_king:
            b_able_to_big_castle = True
        else:
            b_able_to_big_castle = False
    else:
        b_able_to_big_castle = False
        b_able_to_small_castle = False


def check_white_pawn(i,j,moves):
    global square_bool,turn
    if(i-1>=0 and square_bool[i-1][j]==None):
        #squares[i-1][j][0].draw() 
        moves.append((i-1,j))
        if white_pawn_mooved[j] == False and i-2>=0 and square_bool[i-2][j]==None:
            #squares[i-2][j][0].draw()
            moves.append((i-2,j))
    if i-1>=0:
        if j-1>=0 and square_bool[i-1][j-1]!=None:
            if i-1>=0 and "black" in square_bool[i-1][j-1]:
                moves.append((i-1,j-1))
        if j+1<=7 and square_bool[i-1][j+1]!=None:
            if i-1>=0 and "black" in square_bool[i-1][j+1]:
                moves.append((i-1,j+1))
    return moves


def check_black_pawn(i,j,moves):
    global square_bool,turn
    if(i+1<=7 and square_bool[i+1][j]==None):
        #squares[i+1][j][0].draw()
        moves.append((i+1,j))
        if black_pawn_mooved[j] == False and i+2<=7 and square_bool[i+2][j]==None:
            #squares[i+2][j][0].draw()
            moves.append((i+2,j))
    if i+1<=7:
        if j-1>=0 and square_bool[i+1][j-1]!=None:
            if i+1<=7 and "white" in square_bool[i+1][j-1]:
                moves.append((i+1,j-1))
        if j+1<=7 and square_bool[i+1][j+1]!=None:
            if i+1<=7 and "white" in square_bool[i+1][j+1]:
                moves.append((i+1,j+1))
    return moves


def check_knight(i,j,moves,color):
    global square_bool,turn
    if i+2<=7:  
        if j+1<=7 and square_bool[i+2][j+1]==None: 
            #squares[i+2][j+1][0].draw()
            moves.append((i+2,j+1))
        if j+1<=7 and square_bool[i+2][j+1]!=None:
            if color=="white":
                if "black" in square_bool[i+2][j+1]:
                    moves.append((i+2,j+1))
            if color=="black":
                if "white" in square_bool[i+2][j+1]:
                    moves.append((i+2,j+1))

        if j-1>=0 and square_bool[i+2][j-1]==None:
            #squares[i+2][j-1][0].draw()
            moves.append((i+2,j-1))
        if j-1>=0 and square_bool[i+2][j-1]!=None:
            if color == "white":
                if "black" in square_bool[i+2][j-1]:
                    moves.append((i+2,j-1))
            if color == "black":
                if "white" in square_bool[i+2][j-1]:
                    moves.append((i+2,j-1))

    if i-2>=0:
        if j+1<=7 and square_bool[i-2][j+1]==None: 
            moves.append((i-2,j+1))
        if j+1<=7 and square_bool[i-2][j+1]!=None:
            if color == "white":
                if "black" in square_bool[i-2][j+1]:
                    moves.append((i-2,j+1))
            if color == "black":
                if "white" in square_bool[i-2][j+1]:
                    moves.append((i-2,j+1))

        if j-1>=0 and square_bool[i-2][j-1]==None:
            moves.append((i-2,j-1))
        if j-1>=0 and square_bool[i-2][j-1]!=None:
            if color == "white":
                if "black" in square_bool[i-2][j-1]:
                    moves.append((i-2,j-1))
            if color == "black":
                if "white" in square_bool[i-2][j-1]:
                    moves.append((i-2,j-1))

    if j+2<=7:
        if i+1<=7 and square_bool[i+1][j+2]==None:
            #squares[i+1][j+2][0].draw()
            moves.append((i+1,j+2))
        if i+1<=7 and square_bool[i+1][j+2]!=None:
            if color == "white":
                if "black" in square_bool[i+1][j+2]:
                    moves.append((i+1,j+2))
            if color == "black":
                if "white" in square_bool[i+1][j+2]:
                    moves.append((i+1,j+2))
        if i-1>=0 and square_bool[i-1][j+2]==None:
            #squares[i-1][j+2][0].draw()
            moves.append((i-1,j+2))
        if i-1>=0 and square_bool[i-1][j+2]!=None:
            if color =="white":
                if "black" in square_bool[i-1][j+2]:
                    moves.append((i-1,j+2))
            if color =="black":
                if "white" in square_bool[i-1][j+2]:
                    moves.append((i-1,j+2))
    if j-2>=0:
        if i+1<=7 and square_bool[i+1][j-2]==None: 
            #squares[i+1][j-2][0].draw()
            moves.append((i+1,j-2))
        if i+1<=7 and square_bool[i+1][j-2]!=None:
            if color =="white":
                if "black" in square_bool[i+1][j-2]:
                    moves.append((i+1,j-2))
            if color == "black":
                if "white" in square_bool[i+1][j-2]:
                    moves.append((i+1,j-2))
        if i-1>=0 and square_bool[i-1][j-2]==None:
            #squares[i-1][j-2][0].draw()
            moves.append((i-1,j-2))
        if i-1>=0 and square_bool[i-1][j-2]!=None:
            if color =="white":
                if "black" in square_bool[i-1][j-2]:
                    moves.append((i-1,j-2))
            if color =="black":
                if "white" in square_bool[i-1][j-2]:
                    moves.append((i-1,j-2))
    return moves


def check_king(i,j,moves,color):
    global b_able_to_big_castle
    global b_able_to_small_castle
    global w_able_to_big_castle
    global w_able_to_small_castle
    global black_moves
    global white_moves,square_bool,turn
    black_moves = []
    white_moves = []
    if i+1<=7: 
        if j+1<=7 and square_bool[i+1][j+1]==None:
            moves.append((i+1,j+1))
            #squares[i+1][j+1][0].draw()
        if j+1<=7 and square_bool[i+1][j+1]!=None:
            if color == "white":
                if "black" in square_bool[i+1][j+1]: 
                    moves.append((i+1,j+1))
            if color == "black":
                if "white" in square_bool[i+1][j+1]: 
                    moves.append((i+1,j+1))
        if j-1>=0 and square_bool[i+1][j-1]==None:
            moves.append((i+1,j-1))
            #squares[i+1][j-1][0].draw() 
        if j-1>=0 and square_bool[i+1][j-1]!=None:
            if color =="white":
                if "black" in square_bool[i+1][j-1]: 
                    moves.append((i+1,j-1))  
            if color == "black":
                if "white" in square_bool[i+1][j-1]: 
                    moves.append((i+1,j-1))  
    if i-1>=0:
        if j+1<=7 and square_bool[i-1][j+1]==None:
            moves.append((i-1,j+1))
            #squares[i-1][j+1][0].draw()
        if j+1<=7 and square_bool[i-1][j+1]!=None:
            if color == "white":
                if "black" in square_bool[i-1][j+1]: 
                    moves.append((i-1,j+1))   
            if color == "black":
                if "white" in square_bool[i-1][j+1]: 
                    moves.append((i-1,j+1))   
        if j-1>=0 and square_bool[i-1][j-1]==None:
            moves.append((i-1,j-1))
            #squares[i-1][j-1][0].draw()
        if j-1>=0 and square_bool[i-1][j-1]!=None:
            if color == "white":
                if "black" in square_bool[i-1][j-1]: 
                    moves.append((i-1,j-1)) 
            if color == "black":
                if "white" in square_bool[i-1][j-1]: 
                    moves.append((i-1,j-1))   
    if i+1<=7 and square_bool[i+1][j]==None:
        #squares[i+1][j][0].draw()
        moves.append((i+1,j))
    if i+1<=7 and square_bool[i+1][j]!=None:
        if color =="white":
            if "black" in square_bool[i+1][j]: 
                moves.append((i+1,j)) 
        if color =="black":
            if "white" in square_bool[i+1][j]: 
                moves.append((i+1,j)) 
    if i-1>=0 and square_bool[i-1][j]==None:
        moves.append((i-1,j))
        #squares[i-1][j][0].draw()
    if i-1>=0 and square_bool[i-1][j]!=None:
        if color == "white":
            if "black" in square_bool[i-1][j]: 
                moves.append((i-1,j)) 
        if color == "black":
            if "white" in square_bool[i-1][j]: 
                moves.append((i-1,j))
        
    if j+1<=7 and square_bool[i][j+1]==None:
        moves.append((i,j+1))
        #squares[i][j+1][0].draw()
    if j+1<=7 and square_bool[i][j+1]!=None:
        if color =="white":
            if "black" in square_bool[i][j+1]: 
                moves.append((i,j+1)) 
        if color == "black":
            if "white" in square_bool[i][j+1]: 
                moves.append((i,j+1)) 
    if j-1>=0 and square_bool[i][j-1]==None:
        #squares[i][j-1][0].draw()
        moves.append((i,j-1))
    if j-1>=0 and square_bool[i][j-1]!=None:
        if color == "white":
            if "black" in square_bool[i][j-1]: 
                moves.append((i,j-1))
        if color == "black":
            if "white" in square_bool[i][j-1]: 
                moves.append((i,j-1))
    return moves


def check_bishop(i,j,moves,color):
    global square_bool,turn

    k = 1
    up_up = True
    down_up = True
    up_down = True
    down_down = True 
    while k<=7:
        if i+k<=7:
            if j+k<=7 and square_bool[i+k][j+k]==None and up_up:
                moves.append((i+k,j+k))
                #squares[i+k][j+k][0].draw()
            if j+k<=7 and square_bool[i+k][j+k]!=None and up_up:
                if color == "white":
                    if "black" in square_bool[i+k][j+k]: 
                        moves.append((i+k,j+k))
                        up_up = False
                    if "white" in square_bool[i+k][j+k]: 
                        up_up = False

                if color == "black":
                    if "white" in square_bool[i+k][j+k]: 
                        moves.append((i+k,j+k))
                        up_up = False
                    if "black" in square_bool[i+k][j+k]: 
                        up_up = False
            if j-k>=0 and square_bool[i+k][j-k]==None and up_down:
                moves.append((i+k,j-k))
                #squares[i+k][j-k][0].draw()
            if j-k>=0 and square_bool[i+k][j-k]!=None and up_down:
                if color == "white":
                    if "black" in square_bool[i+k][j-k]: 
                        moves.append((i+k,j-k))
                        up_down = False
                    if "white" in square_bool[i+k][j-k]: 
                        up_down = False
                if color == "black":
                    if "white" in square_bool[i+k][j-k]: 
                        moves.append((i+k,j-k))
                        up_down = False
                    if "black" in square_bool[i+k][j-k]: 
                        up_down = False
        if i-k>=0:
            if j+k<=7 and square_bool[i-k][j+k]==None and down_up:
                moves.append((i-k,j+k))
                #squares[i-k][j+k][0].draw()
            if j+k<=7 and square_bool[i-k][j+k]!=None and down_up:
                if color == "white":
                    if "black" in square_bool[i-k][j+k]: 
                        moves.append((i-k,j+k))
                        down_up = False
                    if "white" in square_bool[i-k][j+k]: 
                        down_up = False
                if color == "black":
                    if "white" in square_bool[i-k][j+k]: 
                        moves.append((i-k,j+k))
                        down_up = False
                    if "black" in square_bool[i-k][j+k]: 
                        down_up = False
            if j-k>=0 and square_bool[i-k][j-k]==None and down_down:
                moves.append((i-k,j-k))
                #squares[i-k][j-k][0].draw()
            if j-k>=0 and square_bool[i-k][j-k]!=None and down_down:
                if color == "white":
                    if "black" in square_bool[i-k][j-k]: 
                        moves.append((i-k,j-k))
                        down_down = False
                    if "white" in square_bool[i-k][j-k]: 
                        down_down = False
                if color == "black":
                    if "white" in square_bool[i-k][j-k]: 
                        moves.append((i-k,j-k))
                        down_down = False
                    if "black" in square_bool[i-k][j-k]: 
                        down_down = False
        k = k+1
    return moves


def check_rook(i,j,moves,color):
    global square_bool,turn
    k = 1
    up = True
    down = True
    left = True
    right = True 
    while k<=7:
        if i+k<=7 and square_bool[i+k][j]==None and up:
            #squares[i+k][j][0].draw()
            moves.append((i+k,j))
        if i+k<=7 and square_bool[i+k][j]!=None and up:
            if color == "white":
                if "black" in square_bool[i+k][j]: 
                    moves.append((i+k,j))
                    up = False
                if "white" in square_bool[i+k][j]: 
                    up = False
            if color == "black":
                if "white" in square_bool[i+k][j]: 
                    moves.append((i+k,j))
                    up = False
                if "black" in square_bool[i+k][j]: 
                    up = False

        if i-k>=0 and square_bool[i-k][j]==None and down:
            #squares[i-k][j][0].draw()
            moves.append((i-k,j))
        if i-k>=0 and square_bool[i-k][j]!=None and down:
            if color == "white":
                if "black" in square_bool[i-k][j]: 
                    moves.append((i-k,j))
                    down = False
                if "white" in square_bool[i-k][j]: 
                    down = False
            if color == "black":
                if "white" in square_bool[i-k][j]: 
                    moves.append((i-k,j))
                    down = False
                if "black" in square_bool[i-k][j]: 
                    down = False

        if j+k<=7 and square_bool[i][j+k]==None and right:
            #squares[i][j+k][0].draw()
            moves.append((i,j+k))
        if j+k<=7 and square_bool[i][j+k]!=None and right:
            if color == "white":
                if "black" in square_bool[i][j+k]: 
                    moves.append((i,j+k))
                    right = False
                if "white" in square_bool[i][j+k]: 
                    right = False
            if color == "black":
                if "white" in square_bool[i][j+k]: 
                    moves.append((i,j+k))
                    right = False
                if "black" in square_bool[i][j+k]: 
                    right = False

        if j-k>=0 and square_bool[i][j-k]==None and left:
            #squares[i][j-k][0].draw()
            moves.append((i,j-k))
        if j-k>=0 and square_bool[i][j-k]!=None and left:
            if color == "white":
                if "black" in square_bool[i][j-k]: 
                    moves.append((i,j-k))
                    left = False
                if "white" in square_bool[i][j-k]: 
                    left = False
            if color == "black":
                if "white" in square_bool[i][j-k]: 
                    moves.append((i,j-k))
                    left = False
                if "black" in square_bool[i][j-k]: 
                    left = False
        k = k+1
    return moves


def ChangeColor(color):
    for i in squares:
        for square in i:
            square[0].colour=color


def make_move(board,dst,src):
    board[dst[0]][dst[1]]=square_bool[src[0]][src[1]]
    board[src[0]][src[1]]=None


def undo_move(board,dst,src,old_piece):
    board[src[0]][src[1]]=square_bool[dst[0]][dst[1]]
    board[dst[0]][dst[1]]=old_piece


def CanMove(pos,TurnCheck=True,Check=True):
    global black_moves
    global white_moves,square_bool,turn
    i,j=pos
    moves=[]
    white_moves=[]
    black_moves=[]
    if square_bool[i][j]==None:
        return []
    if TurnCheck:
        if "white" in square_bool[i][j] and turn%2!=0:
            return []
        if "black" in square_bool[i][j] and turn%2==0:
            return []

    if(square_bool[i][j]=="white pawn"):
        moves = copy.deepcopy(check_white_pawn(i,j,moves))
    elif(square_bool[i][j]=="black pawn"):
        moves = copy.deepcopy(check_black_pawn(i,j,moves))
    elif(square_bool[i][j]=="white knight"):
        moves = copy.deepcopy(check_knight(i,j,moves,"white"))
    elif(square_bool[i][j]=="black knight"):
        moves = copy.deepcopy(check_knight(i,j,moves,"black"))
    elif(square_bool[i][j]=="white king"):
        moves = copy.deepcopy(check_king(i,j,moves,"white"))
    elif(square_bool[i][j]=="black king"):
        moves = copy.deepcopy(check_king(i,j,moves,"black"))
    elif(square_bool[i][j]=="white bishop"):
        moves = copy.deepcopy(check_bishop(i,j,moves,"white"))
    elif(square_bool[i][j]=="black bishop"):
        moves = copy.deepcopy(check_bishop(i,j,moves,"black"))
    elif(square_bool[i][j]=="white rook"):
        moves = copy.deepcopy(check_rook(i,j,moves,"white"))
    elif(square_bool[i][j]=="black rook"):
        moves = copy.deepcopy(check_rook(i,j,moves,"black"))
    elif(square_bool[i][j]=="white queen"):
        moves = copy.deepcopy(check_rook(i,j,moves,"white"))
        moves = copy.deepcopy(check_bishop(i,j,moves,"white"))
    elif(square_bool[i][j]=="black queen"):
        moves = copy.deepcopy(check_rook(i,j,moves,"black"))
        moves = copy.deepcopy(check_bishop(i,j,moves,"black"))
    if Check:
        real_moves = []
        #board=copy.copy(square_bool)
        for move in moves:
            old_piece = square_bool[move[0]][move[1]]
            make_move(square_bool,move,pos)
            if (not check(square_bool)):
                real_moves.append(move)
            undo_move(square_bool,move,pos,old_piece)
        return real_moves
    else:
        return moves


def GetPos(name):
    for i,line in enumerate(square_bool):
        for j,player in enumerate(line):
            if name ==player:
                return (i,j)


def check(board):
    global w_on_check
    global b_on_check
    global w_king_placement
    global b_king_placement
    global black_moves
    global white_moves
    king_pos=None
    t=""
    #black turn
    if turn%2!=0:
        #check if white is challenging
        t="white"
        king_pos=GetPos("black king")
    else:
        t="black"
        king_pos=GetPos("white king")
    for i,line in enumerate(board):
        for j,player in enumerate(line):
            if player!=None and t in player:
                moves=CanMove((i,j),TurnCheck=False,Check=False)
                if king_pos in moves:
                    
                    return True

    return False


def get_all_moves():
    all_moves = []
    for i,line in enumerate(square_bool):
        for j,value in enumerate(line):
            tmp = CanMove((i,j))
            if len(tmp):
                all_moves.append(((i,j),tmp))
    return all_moves


def check_mate():
    all_moves = []
    mate_or_tie = True
    global mate
    global tie
    for i,line in enumerate(square_bool):
        for j,value in enumerate(line):
            all_moves=CanMove((i,j))
            if len(all_moves)>0:
                mate_or_tie = False

    if mate_or_tie:
        if check(square_bool):
            if turn%2==0: 
                write(1155,80,"check mate black wins")
            else: 
                write(1155,80,"check mate white wins")
            mate = True
        else:
            write(1155,80,"tie")
            tie = True
        return True
    if b_time <= 0:
        write(1155,80,"time is up white wins")
        return True
    if w_time <= 0:
        write(1155,80,"time is up black wins")
        return True
    return False


def add_points(piece_eaten):
    points = 0
    if "pawn" in piece_eaten:
            points = pawn_worth
    elif "knight" in piece_eaten:
            points = knight_worth
    elif "bishop" in piece_eaten:
            points = bishop_worth
    elif "rook" in piece_eaten:
            points = rook_worth
    elif "queen" in piece_eaten:
            points = queen_worth
    return points


def computers_turn():
    global turn
    if debug:
        print("computers_turn:")
    if "1" in game_mode:
        level = 1  
    elif "2" in game_mode:
        level = 2
    elif "3" in game_mode:
        level = 3
    else:
        level = 4
    if debug:
        print("computers_turn:level: ",level)  
    ai_move = minmax_wrap(level,False)
    if ai_move != None:
        OnClick(ai_move[0])
        OnClick(ai_move[1])
    else:
        events=pygame.event.get()        
        restart_BT.draw()
        restart_BT.listen(events)
        backMenuBT.draw()
        backMenuBT.listen(events)
        print("hello")


def OnClick(pos):


    global ii,jj,act
    ii,jj=pos
    print("clicked",pos)
    global white_pawn_mooved
    global black_pawn_mooved
    global first_press,global_move
    global w_mooved_king
    global b_mooved_king
    global w_mooved_left_rook
    global b_mooved_left_rook
    global w_mooved_right_rook
    global b_mooved_right_rook
    global turn
    global b_time
    global w_time
    global moves
    global w_points
    global b_points
    global level
    if debug:
        print("OnClick,  pos: ", pos)
        print("OnClick,  turn: ", turn)
    ########################################################################
    moves=CanMove(pos)
    bt = squares[ii][jj][0]
    act=False
    if global_move==pos:#cancelation click
        act=True
        global_move=None
    elif (global_move==None and square_bool[ii][jj]!=None):#choose piece click   
        if debug:
            print("OnClick,  choose piece click")   
        if (squares[ii][jj][1]!=None):
            ChangeColor((150,0,0))
            bt.draw()
            first_press = True
        ChangeColor((0,150, 0))   
        for k in moves:
            squares[k[0]][k[1]][0].draw()
        global_move=pos
        act=False
    elif global_move!=None:#move piece click
        if debug:
            print("OnClick,  move piece click")
        act=False
        if debug:
            print("OnClick,  (ii,jj):",ii,jj)
            print("OnClick,  global_move:",global_move)
        if (ii,jj) in CanMove(global_move):
            # if debug:
            #     print("OnClick,  (ii,jj):",ii,jj)
            #     print("OnClick,  global_move:",global_move)
            name=squares[global_move[0]][global_move[1]]
            piece_eaten = square_bool[ii][jj]
            if piece_eaten!=None:
                if "black" in piece_eaten:
                    b_eaten.append(piece_eaten)
                    w_points += add_points(piece_eaten)
                    if piece_eaten == "black rook" and (ii==0 and jj==0):
                        b_mooved_left_rook = True
                    if piece_eaten == "black rook" and (ii==0 and jj==7):
                        b_mooved_right_rook = True
                if "white" in piece_eaten:
                    w_eaten.append(piece_eaten)
                    b_points += add_points(piece_eaten)
                    if piece_eaten == "white rook" or (ii==7 and jj==0):
                        w_mooved_left_rook = True
                    if piece_eaten == "white rook" or (ii==7 and jj==7):
                        w_mooved_right_rook = True
            square_bool[ii][jj]=squares[global_move[0]][global_move[1]][1]
            square_bool[global_move[0]][global_move[1]]=None
            squares[ii][jj]=(squares[ii][jj][0],square_bool[ii][jj])
            squares[global_move[0]][global_move[1]]=(squares[global_move[0]][global_move[1]][0],None)
            if "white pawn" in name:
                white_pawn_mooved[global_move[1]] = True
                if check_pawn_reach_edge("white",ii):
                    pawn_reach_edge_pos  = (ii,jj)
                    draw_pawn_reach_edge()
            if "black pawn" in name:
                black_pawn_mooved[global_move[1]] = True
                if check_pawn_reach_edge("black",ii):
                    pawn_reach_edge_pos  = (ii,jj)
                    draw_pawn_reach_edge()
            if "white king" in name:
                w_mooved_king = True

            if "black king" in name:
                b_mooved_king = True
                ######################
            if "black rook" in name:
                if (global_move[0]==0 and global_move[1]==0):
                    b_mooved_left_rook = True
                if (global_move[0]==0 and global_move[1]==7):
                    b_mooved_right_rook = True
            if "white rook" in name:
                if (global_move[0]==7 and global_move[1]==0):
                    w_mooved_left_rook = True
                if (global_move[0]==7 and global_move[1]==7):
                    w_mooved_right_rook = True
            global_move=None
            if (squares[ii][jj][1]!=None):
                ChangeColor((150,0,0))
                bt.draw()
                first_press = True
                ChangeColor((0,150, 0))   

            for k in moves:
                squares[k[0]][k[1]][0].draw()
            turn+=1
            #TIME increament
            if turn%2!=0:
                w_time+=2
            else:
                b_time+=2
            act=True
            if debug:
                print("OnClick,  turn:", turn)
            if "computer" in game_mode and turn%2!=0:
                if debug:
                    print("OnClick,  computer & white")
                pygame.event.set_blocked(pygame.MOUSEMOTION)                
                init_screen()
                computers_turn()
                init_screen()
    if act:    
        init_screen()


def small_CastleClick(): 
    global turn
    global squares
    check_casteling()
    color=""
    if turn%2==0:
        color = "white"
    else:
        color = "black"
    if color == "black":    
        if b_able_to_small_castle:    
                turn+=1
                square_bool[0][4] = None
                square_bool[0][7] = None
                square_bool[0][5]="black rook"
                square_bool[0][6]="black king"
                squares[0][4]=(squares[0][4][0],None)
                squares[0][7]=(squares[0][7][0],None)
                squares[0][5]=(squares[0][5][0],"black rook")
                squares[0][6]=(squares[0][6][0],"black king")
                init_screen()
    if color == "white":
        if w_able_to_small_castle:  
            turn+=1
            square_bool[7][4] = None
            square_bool[7][7] = None
            square_bool[7][5]="white rook"
            square_bool[7][6]="white king"
            squares[7][4]=(squares[7][4][0],None)
            squares[7][7]=(squares[7][7][0],None)
            squares[7][5]=(squares[7][5][0],"white rook")
            squares[7][6]=(squares[7][6][0],"white king")
            init_screen()
  

def big_CastleClick():
    global turn
    global squares
    check_casteling()
    color=""
    if turn%2==0:
        color = "white"
    else:
        color = "black"
    if color == "black":
        if b_able_to_big_castle:
            turn+=1
            square_bool[0][4] = None
            square_bool[0][0] = None
            square_bool[0][2]="black rook"
            square_bool[0][1]="black king"
            squares[0][4]=(squares[0][4][0],None)
            squares[0][0]=(squares[0][0][0],None)
            squares[0][2]=(squares[0][2][0],"black rook")
            squares[0][1]=(squares[0][1][0],"black king")
            init_screen()
    if color == "white":
        if w_able_to_big_castle:
            turn+=1
            square_bool[7][4] = None
            square_bool[7][0] = None
            square_bool[7][2]="white rook"
            square_bool[7][1]="white king"
            squares[7][4]=(squares[7][4][0],None)
            squares[7][0]=(squares[7][0][0],None)
            squares[7][2]=(squares[7][2][0],"white rook")
            squares[7][1]=(squares[7][1][0],"white king")
            init_screen()


def minmax(depth,maximizing_player): 
    global turn
    turn+=1
    b = check_mate()
    if debug:
        print("minmax, b:",b)
    turn-=1
    if depth == 0 or b:
        score = calculate_board(square_bool)
        if b:
            if maximizing_player:#for zero we need to reverse the calculation because no move is made
                score-=100
            else:
                score+=100
                if debug:  
                    print("minmax, score-100",score)  
        return score

    if maximizing_player:
        max_evaluation = -1000
        all_moves = get_all_moves()
        for (src,destinations) in all_moves:
            for dst in destinations:
                old_piece = square_bool[dst[0]][dst[1]]
                make_move(square_bool,dst,src)
                score = minmax(depth-1,False)
                undo_move(square_bool,dst,src,old_piece)
                if score > max_evaluation:
                    max_evaluation = score
        return max_evaluation
    else:
        min_evaluation = 1000
        all_moves = get_all_moves()
        for (src,destinations) in all_moves:
            for dst in destinations:
                old_piece = square_bool[dst[0]][dst[1]]
                make_move(square_bool,dst,src)
                score = minmax(depth-1,True)
                undo_move(square_bool,dst,src,old_piece)
                if score < min_evaluation:
                    min_evaluation = score
        return min_evaluation


def minmax_wrap(depth, maximizing_player):
    if debug:
        print("minmax_wrap")
    all_moves = get_all_moves()
    best_move = None
    if maximizing_player:
        max_evaluation = -1000
        if len(all_moves):
            best_move = all_moves[0][0],all_moves[0][1][0]
        for (src,destinations) in all_moves:
            for dst in destinations:
                old_piece = square_bool[dst[0]][dst[1]]
                make_move(square_bool,dst,src)
                score = minmax(depth-1,False)
                undo_move(square_bool,dst,src,old_piece)
                if score > max_evaluation:
                    max_evaluation = score
                    best_move = src,dst
    else:
        min_evaluation = 1000
        all_moves = get_all_moves()
        if len(all_moves):
            best_move = all_moves[0][0],all_moves[0][1][0]
        for (src,destinations) in all_moves:
            for dst in destinations:
                old_piece = square_bool[dst[0]][dst[1]]
                make_move(square_bool,dst,src)
                score = minmax(depth-1,True)
                undo_move(square_bool,dst,src,old_piece)
                if score < min_evaluation:
                    min_evaluation = score
                    best_move = src,dst
        if debug:
            print("min_evaluation: ",min_evaluation)
    if debug:
        print("best_move: ",best_move[0][0],best_move[0][1],best_move[1][0],best_move[1][1])
    return best_move
    

def init_buttons():

    global restart_BT
    global backMenuBT
    global small_castleBT
    global big_castleBT
    global knight_BT
    global queen_BT

    restart_BT=pgWidgets.Button(screen,x=0,y=100,height=100,width=225,text="Restart",fontSize=50,onClick=restart)
    backMenuBT=pgWidgets.Button(screen,x=0,y=0,height=100,width=225,text="Back to menu",fontSize=50,onClick=back_to_menu)

    knight_BT=pgWidgets.Button(screen,x=300,y=600,height=150,width=500,text="Knight",fontSize=50,onClick=on_click_knight)
    queen_BT=pgWidgets.Button(screen,x=300,y=400,height=150,width=500,text="Queen",fontSize=50,onClick=on_click_queen)

    small_castleBT=pgWidgets.Button(screen,x=1100,y=750,height=100,width=230,text="Small Castle",fontSize=50,onClick=small_CastleClick)
    small_castleBT.draw()
    big_castleBT=pgWidgets.Button(screen,x=1100,y=650,height=100,width=230,text="Big Castle",fontSize=50,onClick=big_CastleClick)
    big_castleBT.draw()
    

def draw_pawn_reach_edge():
    global chose
    chose = False
    while chose:
        draw_image(0,0,game_background)
        knight_BT.draw()
        queen_BT.draw()
        events=pygame.event.get()
        queen_BT.listen(events)
        knight_BT.listen(events)
        pygame.display.flip()


def start_game():
    global restart_BT
    global backMenuBT
    global small_castleBT
    global big_castleBT
    global running
    init_buttons()
    init_squares()
    init_screen()

    first=10
    #time_thread=threading.Thread(target=Timer)
    #time_thread.start()

    while running:
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        if first>10:
            for i in squares:
                for j in i: 
                    j[0].listen(events)
            small_castleBT.listen(events)
            big_castleBT.listen(events)
        small_castleBT.draw()
        big_castleBT.draw()
    
        w_eatenIMG=[]
        b_eatenIMG=[]
        for i in w_eaten:
            if i!=None:
                if "pawn" in i:
                    w_eatenIMG.append(w_pawn_eat)
                if "bishop" in i:
                    w_eatenIMG.append(w_bishop_eat)
                if "knight" in i:
                    w_eatenIMG.append(w_knight_eat)
                if "rook" in i:
                    w_eatenIMG.append(w_rook_eat)
                if "queen" in i:
                    w_eatenIMG.append(w_queen_eat)
        for i in b_eaten:
            if i!=None:
                if "pawn" in i:
                    b_eatenIMG.append(b_pawn_eat)
                if "bishop" in i:
                    b_eatenIMG.append(b_bishop_eat)
                if "knight" in i:
                    b_eatenIMG.append(b_knight_eat)
                if "rook" in i:
                    b_eatenIMG.append(b_rook_eat)
                if "queen" in i:
                    b_eatenIMG.append(b_queen_eat)
        write(300,450,str(w_time))
        write(300,350,str(b_time))
        for i in range(len(w_eatenIMG)):
            if i<8:
                screen.blit(w_eatenIMG[i],(1100+(i*60),500))
            else:
                screen.blit(w_eatenIMG[i],(1100+((i-8)*60),570))
        for i in range(len(b_eatenIMG)):
            if i<8:
                screen.blit(b_eatenIMG[i],(1100+(i*60),300))
            else:
                screen.blit(b_eatenIMG[i],(1100+((i-8)*60),370))
        if check_mate():
            restart_BT.draw()
            restart_BT.listen(events)
            backMenuBT.draw()
            backMenuBT.listen(events)
        pygame.display.flip()
        first += 1


def main():
    global running
    opening_screen()
    if running:
        start_game()


main()

