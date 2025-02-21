import PygameRenderer as pr
import time
time.sleep(3)

"""
for board matrix use the following convention:
0 - water
1 - ship
2 - destroyed ship
3 - special regions
"""

pr.max_board_dim = [800, 800]
pr.side_column_width = 100
pr.leaderboard_height = 0

# Can override margins/thickness here

# Internal Timer.
start_time = time.time()

#TimeLine
initial_skirting = 0.5



# Dummy Values for testing purposes

board1 = [ [ 0 for i in range(10) ] for j in range(10) ]
board2 = [ [ 0 for i in range(10) ] for j in range(10) ]

"""
board1[2][3] = 1
board1[2][4] = 1
board1[2][5] = 1

board1[5][2] = 1
board1[5][3] = 1
board1[5][4] = 1

board1[8][6] = 1
board1[8][7] = 1
board1[8][8] = 1

board2[4][4] = 1   
board2[4][5] = 1
board2[4][6] = 1

board2[7][6] = 1
board2[7][7] = 1
board2[7][8] = 1

board2[1][3] = 1
board2[1][4] = 1
board2[1][5] = 1
"""

def placeShips(board, ships):
    for ship in ships:
        for x in range(ship[3]):
            for y in range(ship[4]):
                #Assertions/If statements must be made here to avoid out-of-index errors.
                #Erroneous ship placement is the participants fault.
                board[ship[1]+y][ship[0]+x] = 1
    
    return board

def initialize():
    # Make sure ship lists are legal.
    pr.board1 = board1
    pr.board2 = board2
    pr.ships1 = [[0, 0, 0, 3, 1], # x, y, orientation, length
                 [2, 5, 0, 3, 1],
                 [6, 8, 0, 3, 1]]
    pr.ships2 = [[4, 4, 0, 3, 1],
                 [6, 7, 0, 3, 1],
                 [3, 1, 0, 3, 1]]
    pr.board1 = placeShips(pr.board1, pr.ships1)
    pr.board2 = placeShips(pr.board2, pr.ships2)
    pr.initialize()


initialize()
while pr.running:
    pr.draw_call([None, None])
