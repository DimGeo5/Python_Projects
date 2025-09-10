print("Welcome to tic tac toe game!")
print("Choose where to put your X or O by pressing the number as shown below")
print("""
            1 | 2 | 3
          ____|___|____
            4 | 5 | 6   
          ____|___|____
            7 | 8 | 9  
""")

bs = [" ", " ", " ", " ", " ", " ", " ", " ", " "]  # board spaces list
am = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]  # available moves list
board = f"""
            {bs[0]} | {bs[1]} | {bs[2]}
          ____|___|____
            {bs[3]} | {bs[4]} | {bs[5]}   
          ____|___|____
            {bs[6]} | {bs[7]} | {bs[8]}    
"""


def win_check():  # checks if there is a winner after certain number of rounds
    global bs
    if bs[0] == bs[1] == bs[2] == "X":
        print("Player 1 wins")
        return False
    elif bs[0] == bs[1] == bs[2] == "O":
        print("Player 2 wins")
        return False
    elif bs[3] == bs[4] == bs[5] == "X":
        print("Player 1 wins")
        return False
    elif bs[3] == bs[4] == bs[5] == "O":
        print("Player 2 wins")
        return False
    elif bs[6] == bs[7] == bs[8] == "X":
        print("Player 1 wins")
        return False
    elif bs[6] == bs[7] == bs[8] == "O":
        print("Player 2 wins")
        return False
    elif bs[0] == bs[3] == bs[6] == "X":
        print("Player 1 wins")
        return False
    elif bs[0] == bs[3] == bs[6] == "O":
        print("Player 2 wins")
        return False
    elif bs[1] == bs[4] == bs[7] == "X":
        print("Player 1 wins")
        return False
    elif bs[1] == bs[4] == bs[7] == "O":
        print("Player 2 wins")
        return False
    elif bs[2] == bs[5] == bs[8] == "X":
        print("Player 1 wins")
        return False
    elif bs[2] == bs[5] == bs[8] == "O":
        print("Player 2 wins")
        return False
    elif bs[0] == bs[4] == bs[8] == "X":
        print("Player 1 wins")
        return False
    elif bs[0] == bs[4] == bs[8] == "O":
        print("Player 2 wins")
        return False
    elif bs[2] == bs[4] == bs[6] == "X":
        print("Player 1 wins")
        return False
    elif bs[2] == bs[4] == bs[6] == "O":
        print("Player 2 wins")
        return False
    else:
        return True


def move(player, fmove):  # checks whose turn is, witch space is chosen and put the proper sign on board
    global board, am, bs
    if player == 1:
        for i in range(1, 10):
            if fmove == str(i):
                bs[i - 1] = "X"  # changes bs (board spaces) list position according to player's choice
                am[i - 1] = "0"  # changes am (available moves) list, so the same number(board position) could not be,
                                    #  chosen again
    elif player == 2:
        for i in range(1, 10):
            if fmove == str(i):
                bs[i - 1] = "O"
                am[i - 1] = "0"

    board = f"""
                {bs[0]} | {bs[1]} | {bs[2]}
              ____|___|____
                {bs[3]} | {bs[4]} | {bs[5]}   
              ____|___|____
                {bs[6]} | {bs[7]} | {bs[8]}    
    """


game_is_on = True
tround = 1      # counts the rounds
while game_is_on:
    player1_turn = True
    player2_turn = True
    while player1_turn:
        player1_move = input("Player 1: ")
        if player1_move in am:         # am(available moves list)
            move(1, player1_move)
            print(board)
            if tround >= 3:          # after round 3 could be a possible winner
                game_is_on = win_check()
            player1_turn = False
        else:
            print("Not available move, try again!")   # in case an already used space is chosen
    while player2_turn and tround != 5 and game_is_on:
        player2_move = input("Player 2: ")
        if player2_move in am:          # am(available moves list)
            move(2, player2_move)
            print(board)
            player2_turn = False
        else:
            print("Not available move, tyry again!")
    if tround >= 3 and game_is_on:
        game_is_on = win_check()   # even player 2 can win sometimes
    if tround == 5 and game_is_on:
        print("It is a draw!")     # board is full, but no winner, it is a draw
        break
    tround += 1
