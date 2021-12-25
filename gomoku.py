import pygame
import sys
from pygame.locals import *
import myAI 


pygame.init()

player1 = 1
player2 = 2

# todo: add method of switching from human to ai in game
# todo: add a settings page that you access the game from and return the player to the settings page after game ends
# todo: highlight most recently placed piece

# change controls to 'computer' to play against AI
p1_controls = 'computer'
p2_controls = 'computer'

# board png source: https://commons.wikimedia.org/wiki/File:Blank_Go_board.png
img_board = pygame.image.load('./images/Blank_Go_board.png')
black_piece = pygame.image.load('./images/blackpiece.jpeg')
white_piece = pygame.image.load('./images/whitepiece.png')
img_panel = pygame.image.load('./images/panel.png')

ticks = 30

dispWidth = 900
dispHeight = 700

player_highlight_width = 5

board_size = 19

player_infobox_x = 20
player1_infobox_y = 110
player2_infobox_y = 386
infobox_width = 160
infobox_height = 120

player1_info = {'time': 0}
player2_info = {'time': 0}
            
#displays information for the two players            
#todo: add more to infobox, currently only displays time and highlights whose turn it is
def displayInfobox(info1, info2, player):

    #highlights current player in green    
    setDisplay.blit(img_panel, (0,0))
    if player == player1:
        pygame.draw.rect(setDisplay, (0,175,0), (player_infobox_x + 20, player1_infobox_y - 12, infobox_width - 40, infobox_height + 30), player_highlight_width)
    else:
        pygame.draw.rect(setDisplay, (0,175,0), (player_infobox_x + 20, player2_infobox_y - 12, infobox_width - 40, infobox_height + 30), player_highlight_width)


    font = pygame.font.SysFont('Times New Roman', 20)
    
    player_name1 = 'Player 1'
    player_time1 = 'Time: %.1f s' % info1['time']

    # display player 1 name
    name_surface = font.render(player_name1, True, (0,0,0))
    name_rect = name_surface.get_rect()
    name_rect.center = (int(player_infobox_x + infobox_width / 2), int(player1_infobox_y + infobox_height / 2) - 30)
    setDisplay.blit(name_surface, name_rect)

    #display player 1 time
    time_surface = font.render(player_time1, True, (0,0,0))
    time_rect = time_surface.get_rect()
    time_rect.center = (int(player_infobox_x + infobox_width / 2), int(player1_infobox_y + infobox_height / 2) + 26)
    setDisplay.blit(time_surface, time_rect)

    player_name2 = 'Player 2'
    player_time2 = 'Time: %.1f s' % info2['time']

    #displayer player 2 name
    name_surface = font.render(player_name2, True, (0,0,0))
    name_rect = name_surface.get_rect()
    name_rect.center = (int(player_infobox_x + infobox_width / 2), int(player2_infobox_y + infobox_height / 2) - 30)
    setDisplay.blit(name_surface, name_rect)

    #display player 2 time
    time_surface = font.render(player_time2, True, (0,0,0))
    time_rect = time_surface.get_rect()
    time_rect.center = (int(player_infobox_x + infobox_width / 2), int(player2_infobox_y + infobox_height / 2) + 26)
    setDisplay.blit(time_surface, time_rect)

def getEvent():
    for event in pygame.event.get([KEYDOWN, KEYUP, QUIT]):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            continue
        return event.key
    return None

def game():

    winner = 0
    currPlayer = player1

    setDisplay.blit(img_board, (200,0))
    displayInfobox(player1_info, player2_info, currPlayer)
    
    pygame.display.update()

    chessboard = [[0 for j in range(board_size)] for i in range(board_size)]
    agent1 = myAI.minimaxAgent()
    agent1.board = chessboard
    agent2 = myAI.minimaxAgent()
    agent2.board = chessboard

    while True:
        while not winner:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            start_time = pygame.time.get_ticks() #start turn timer

            if currPlayer == player1 and p1_controls == 'human':
                row, col = clickToPos()
                while not validatePos((row, col), chessboard):
                    row, col = clickToPos()

            elif currPlayer == player1 and p1_controls == 'computer':
                score, row, col = agent1.minimax(1, 2)
                    
            elif currPlayer == player2 and p2_controls == 'human':
                row, col = clickToPos()
                while not validatePos((row, col),chessboard):
                    row, col = clickToPos()
                    
            elif currPlayer == player2 and p2_controls == 'computer':
                score, row, col = agent2.minimax(2, 2)
                    
            end_time = pygame.time.get_ticks() #end turn timer
                
            chessboard[row][col] = currPlayer
            winner = checkWinner(chessboard, currPlayer)
            posToPiece((row, col), currPlayer)

            time_spent = end_time - start_time
            if currPlayer == player1:
                player1_info['time'] += time_spent / 1000.0
            else:
                player2_info['time'] += time_spent / 1000.0
            #todo: implement win/loss based on timer

            currPlayer = 3 - currPlayer

            displayInfobox(player1_info, player2_info, currPlayer)


            win_font = pygame.font.SysFont('Times New Roman', 60)
            if winner:
                text = 'Player ' + str(winner) + ' Wins!'    
                winner_surface = win_font.render(text, True, (0,175,0))
                winner_rect = winner_surface.get_rect()
                winner_rect.center = (int(dispWidth / 2), int(dispHeight / 2))
                pygame.draw.rect(setDisplay, (105, 105, 105), (180, 220, 550, 260))
                setDisplay.blit(winner_surface, winner_rect)   


            pygame.display.update()
            tick_rate.tick(ticks)
            if winner != 0:
                pygame.time.delay(1500)
                pygame.quit
                sys.exit()
            

def posToPiece(pos, player):
    x = 200 + (pos[1] + 0) * 36.5 + 20 - 24/2
    y = 0 + (pos[0] + 0) * 36.5 + 20 - 24/2

    # print(x, y) for testing
    if player == player1:
        setDisplay.blit(black_piece, (x,y))
    else:
        setDisplay.blit(white_piece, (x,y))

def clickToPos():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                row = int(round((y - 20) / 36.5))
                col = int(round((x - 220) / 36.5))
                # print(row, col) for testng
                return row, col

def validatePos(pos, board):
    row = pos[0]
    col = pos[1]
    return (not board[row][col]) and (not (row < 0 or row > board_size - 1)) and (not (col < 0 or col > board_size - 1))

def checkWinner(board, player):
    directions = ((1, 0), (0, 1), (1, 1), (1, -1))
    for i in range(19):
        for j in range(19):
            if board[i][j] != player:
                continue
            for dir in directions:
                c, r = i, j
                count = 0
                for k in range(5):
                    if c > 18 or c < 0 or r > 18 or r < 0 or board[c][r] != player:
                        break
                    c += dir[0]
                    r += dir[1]
                    count += 1
                if count == 5:
                    return player
    return 0    
  

while True:
    global tick_rate
    global setDisplay

    tick_rate = pygame.time.Clock()
    setDisplay = pygame.display.set_mode((dispWidth, dispHeight))
    pygame.display.set_caption('Gomoku')

    game()
