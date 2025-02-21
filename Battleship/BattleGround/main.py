from itertools import chain
import time
from ..utils import RenderInterface as animation
import random
from ..utils import RenderTest as animation

from ..example_submission import team1
from ..example_submission import team2

dim = 10 ## dimension of board

def update_hit(board, x, y):
    info = -1
    if x > len(board) or y > len(board[0]) or x < -(len(board)) or y < -(len(board[0])):
            print("FIRED OUT OF BATTLEZONE")

    elif board[x][y] == 1:
            info = 0
            board[x][y] = info
            print("HIT !!") 
    else:
        print("MISS !!")
        info = 1 ## MISS

    return (board, info)



def game_over(board):
    if all(x == 0 for x in chain(*board)) : 
        return True

    return False


def hawkeye_attack(board, x, y):
    for i in range(dim):
        if board[x][i] == 1:
            board[x][i] = 0
        if board[i][y] == 1:
            board[i][y] = 0

    return board




## Loading both Bot Programs as modules
team1_module = team1.BattleShip()
team2_module = team2.BattleShip()


## Setting both BattleFields !!
team1_ships = team1_module.set_ships()
team2_ships = team2_module.set_ships()

# Orientation of the ships
for ship in team1_ships:
    if ship[4] == 0:
        ship[4] = ship[3]
        ship[4] = 1
for ship in team2_ships:
    if ship[4] == 0:
        ship[4] = ship[3]
        ship[4] = 1


empty_board = [
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
        [0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0],
    ]

# converting to the board to matrix format
team1_board = [[]]
team2_board = [[]]

for ship in team1_ships:
    row = ship[0]
    col = ship[1]
    length = ship[3]
    orientation = ship[4]
    
    if orientation == 0:
        for i in range(length):
            team1_board[row+i][col] = 1
    elif orientation == 1:
        for i in range(length):
            team1_board[row][col+i] = 1

for ship in team2_ships:
    row = ship[0]
    col = ship[1]
    length = ship[3]
    orientation = ship[4]
    team2_board = empty_board

    if orientation == 0:
        for i in range(length):
            team2_board[row+i][col] = 1
    elif orientation == 1:
        for i in range(length):
            team2_board[row][col+i] = 1

## For Pygame initialisation
animation.board1 = team1_board
animation.board2 = team2_board
animation.initialize()



## Randomly putting two special spots in two ships for triggering special attack !!
special_spots = []
for i in range(dim):
    for j in range(dim):
        if team1_board[i][j] == 1:
            special_spots.append((i,j))
team1_special_spot = random.sample(set(special_spots), 2)
special_spots = []
for i in range(dim):
    for j in range(dim):
        if team2_board[i][j] == 1:
            special_spots.append((i,j))
team2_special_spot = random.sample(set(special_spots), 2)
# print("TEAM 1 SPL SPOT : " , team1_special_spot)
# print("TEAM 2 SPL SPOT : " , team2_special_spot)

team1_hawkeye_activated = False
team2_hawkeye_activated = False
## index 0 is for skipping opponent's chance and index 1 is for Missile Hawkeye!

# Player1 driver function
def player1():
    global team2_board, team2_special_spot, team1_hawkeye_activated
    x, y = team1_module.attack()
    print("Team 1 attacked at  : " + str((x,y)))
    team2_board, info = update_hit(team2_board, x, y) ## Updates the board as well as returns hit/miss
    if team1_hawkeye_activated:
        team1_hawkeye_activated = False
        team2_board = hawkeye_attack(team2_board, x, y)
    if (x,y) in team2_special_spot:
        if team2_special_spot.index((x,y)) == 0:
            info = 2
            print("NULLIFY")

        elif team2_special_spot.index((x,y)) == 1:
            info = 3
            team1_hawkeye_activated = True
            print("HAWKEYE ACTIVATED !! ")

        team2_special_spot[team2_special_spot.index((x,y))] = None

    team1_module.hit_or_miss(x, y, info)  ## info = 0 for only hit , 1 for miss, and -1 for out of range shooting, info = 2 for skipping opponent's chance, and info = 3 for Hawkeye Missile Activation

    animation.update(team1_board, team2_board)     ## Update Animation board

    time.sleep(1)
    if game_over(team2_board):
        print("Team 1 has won !!!")
        exit()

    if info == 2:
        player1()


## Player 2 driver function
def player2():
    global team1_board, team2_board, team1_special_spot, team2_hawkeye_activated
    x, y = team2_module.attack()
    print("Team 2 attacked at  : " + str((x,y)))
    team1_board, info = update_hit(team1_board, x, y)
    if team2_hawkeye_activated:
        team2_hawkeye_activated = False
        team1_board = hawkeye_attack(team1_board, x, y)

    if (x,y) in team1_special_spot:
        if team1_special_spot.index((x,y)) == 0:
            info = 2
            print("NULLIFY")
            time.sleep(5)

        elif team1_special_spot.index((x,y)) == 1:
            info = 3
            team2_hawkeye_activated = True
            print("HAWKEYE ACTIVATED !! ")
            time.sleep(5)

        team1_special_spot[team1_special_spot.index((x,y))] = None

    team2_module.hit_or_miss(x, y, info)

    animation.update(team1_board, team2_board)     ## Update Animation board
    
    time.sleep(1)
    if game_over(team1_board):
        print("Team 2 has won !!!")
        exit()
    if info == 2:
        player2()




while True:
    player1()
    player2()