import numpy as np
import random

board = np.zeros((6, 6), dtype=int)

# Takes in np Board and prints out put
def display_board(board):
    for row in board:
        print(' '.join(map(str, row)))
    pass
    
# Takes End turn board and check for victory
def check_victory(board,turn,rot):

    temp_board = board.copy()

    #Check Victory after rot
    post_rot_result = static_check_victory(temp_board)

    #rotate back
    temp_board = reverse_rotate(temp_board, rot)

    #Check Victory before rot
    pre_rot_results = static_check_victory(temp_board)

    if pre_rot_results != 0:
        return pre_rot_results
    else:
        if post_rot_result != 0:
            return post_rot_result
        else:
            pass

    #Else check for all filled = draw
    if temp_board.all() != 0:
        return 3

    #Else return 0
    return 0
    
# Takes static boards, return 1 and 2 if player wins, 3 for tie, 0 for none
def static_check_victory(board):

    winner = []

    for player in [1,2]:
        for i in range(6):
            if all(board[i, :+5] == player) or all(board[:+5, i] == player): #5 consecutive in a row/ col
                winner.append(player)
            elif all(board[i, 1:6] == player) or all(board[1:6, i] == player): #5 consecutive in a row/ col
                winner.append(player)
        else:
            if board[0,5]==board[1,4]==board[2,3]==board[3,2]==board[4,1]==player : 
                winner.append(player) 
            elif board[5,0]==board[1,4]==board[2,3]==board[3,2]==board[4,1]==player : 
                winner.append(player)     
            elif board[0,0]==board[1,1]==board[2,2]==board[3,3]==board[4,4]==player : 
                winner.append(player) 
            elif board[5,5]==board[1,1]==board[2,2]==board[3,3]==board[4,4]==player : 
                winner.append(player) 
            elif (np.sum(np.diag(board, 1) == player) >=5) or (np.sum(np.diag(np.fliplr(board), 1) == player) >=5) : #win for small diag 
                winner.append(player)
            elif (np.sum(np.diag(board, -1) == player)>=5) or (np.sum(np.diag(np.fliplr(board), -1) == player) >=5) : #win for small diag 
                winner.append(player)

    if 1 in winner and 2 in winner:
        return 3
    elif 1 in winner:
        return 1
    elif 2 in winner:
        return 2
    else:
        return 0
    
# Takes board and action and return actioned board
def put_pin(board, turn, row, col):
    temp_board = board.copy()
    temp_board[row][col] = turn
    return temp_board

# Takes board, rotate, and returns rotated board
def rotate(root_board, rot):
    board = root_board.copy()
    if rot == 1:
        selected_quadrant = board[0:3, 3:6] 
        rotated_quadrant = np.rot90(selected_quadrant, k=3)
        board[0:3, 3:6] = rotated_quadrant
      
    elif rot == 2:
        selected_quadrant = board[0:3, 3:6] 
        rotated_quadrant = np.rot90(selected_quadrant)
        board[0:3, 3:6] = rotated_quadrant

    elif rot == 3:
        selected_quadrant = board[3:6, 3:6] 
        rotated_quadrant = np.rot90(selected_quadrant, k=3)
        board[3:6, 3:6] = rotated_quadrant
        
    elif rot == 4:
        selected_quadrant = board[3:6, 3:6] 
        rotated_quadrant = np.rot90(selected_quadrant)
        board[3:6, 3:6] = rotated_quadrant

    elif rot == 5:
        selected_quadrant = board[3:6, 0:3] 
        rotated_quadrant = np.rot90(selected_quadrant, k=3)
        board[3:6, 0:3] = rotated_quadrant
        
    elif rot == 6:
        selected_quadrant = board[3:6, 0:3] 
        rotated_quadrant = np.rot90(selected_quadrant)
        board[3:6, 0:3] = rotated_quadrant
        
    elif rot == 7:
        selected_quadrant = board[0:3, 0:3] 
        rotated_quadrant = np.rot90(selected_quadrant, k=3)
        board[0:3, 0:3] = rotated_quadrant
        
    elif rot == 8:
        selected_quadrant = board[0:3, 0:3] 
        rotated_quadrant = np.rot90(selected_quadrant)
        board[0:3, 0:3] = rotated_quadrant
 # implement your function here
    return board

# Takes board and rot, reverses rot and returns board
def reverse_rotate(board, rot_to_reverse):
    reversal_dict = {
        "1": 2, "2": 1, 
        "3": 4, "4": 3,
        "5": 6, "6": 5,
        "7": 8, "8": 7
    }
    return rotate(board, reversal_dict[str(rot_to_reverse)])

# Takes board, applies move, and return end_board
def apply_move(board,turn,row,col,rot):
    temp_board = board.copy()
    temp_board = put_pin(temp_board, turn, row, col)
    temp_board = rotate(temp_board, rot)
    return temp_board

# Checks if current move can be applied   
def check_move(board,row,col):    
    if board[row][col] != 0:
        return False
    else:
        return True

# Checks current board state, returns all possible moves
def get_possible_moves(board):
    possible_moves = []
    for row in range(6):
        for col in range(6):
            if board[row][col] == 0:
                for rot in range(1,9):
                    possible_moves.append((row,col,rot))
    return possible_moves

#  Given board and action, return outcome (prioritise pre-rot outcome > post rot outcome) (Can return 1, 2, 3)
def simulate_outcome(board, row, col, rot, turn):
    temp_board = board.copy()
    #put pin
    temp_board = put_pin(temp_board, turn, row, col)

    #check win
    result = static_check_victory(temp_board)
    if result != 0:
        return result

    #rotate
    temp_board = rotate(temp_board, rot)

    #check win
    result = static_check_victory(temp_board)

    if result != 0:
        #if win or draw, return outcome
        return result
    
    return 0

# Given Board state and turn returns computer move in form of array [row, col, rot]
def computer_move(board,turn,level):
    root_temp_board = board.copy()
    opponent_turn = 3 - turn
    # get possible moves
    possible_moves = get_possible_moves(root_temp_board.copy())

    #Level 1 returns random 
    if level == 1:
        return random.choice(possible_moves)

    #Level 2

    #Find move that results in direct win
    for possible_move in possible_moves:
        # check outcome of given move
        outcome = simulate_outcome(root_temp_board, possible_move[0], possible_move[1], possible_move[2], turn)

        #Move results in win, return move
        if outcome == turn:
            return possible_move
        #Moves that lead to opponent win, remove move from possible moves
        elif outcome == opponent_turn:
            possible_moves.remove(possible_move)
    
    #No moves result in win, attempt to prevent opponent direct win
    for possible_move in possible_moves:
        temp_board = apply_move(root_temp_board, turn, possible_move[0], possible_move[1], possible_move[2])
        #Generate all opponent possible moves
        possible_opponent_moves = get_possible_moves(temp_board)
        can_opponent_win = False

        for possible_opponent_move in possible_opponent_moves:
            possible_opponent_outcome = simulate_outcome(temp_board, possible_opponent_move[0], possible_opponent_move[1], possible_opponent_move[2], opponent_turn)
            if possible_opponent_outcome == opponent_turn:
                #Opponent can win from this move
                can_opponent_win = True

            else:
                pass

        if can_opponent_win == False:
            return possible_move

    #No moves prevent opponent direct win
    return random.choice(possible_moves)

    return (0,0,0)

# ------------ Menu Functions -----------------

# Takes current board and turn, request validated player input, returns moves
def request_player_input(board, turn):
    display_board(board)
    print()
    print(f"Player {turn}'s turn:")
    print('-' * 18)

    # Range Validation
    row_invalidation = True
    col_invalidation = True
    rot_invalidation = True

    while row_invalidation:
        row = input('Enter your row (0-5): ')   
        if row.isdigit():
            row = int(row)
            if row in range(0,6):
                row_invalidation = False
            else:
                print('Row entered not valid\n')
        else:
            print('Row entered not valid\n')
    while col_invalidation:
        col = input('Enter your col (0-5): ')
        if col.isdigit():
            col = int(col)
            if col in range(0,6):
                col_invalidation = False
            else:
                print('Col entered not valid\n')
        else:
            print('Col entered not valid\n')
    while rot_invalidation:
        rot = input('Enter your Rot (1-8): ')
        if rot.isdigit():
            rot = int(rot)
            if rot in range(1,9):
                rot_invalidation = False
            else:
                print('Rot entered not valid\n')
        else:
            print('Rot entered not valid\n')
    print ('-' * 50)


    return [row, col, rot]

# Asks user if they would like to restart, returns 1 for start new game, 0 for end
def restart_procedure():
    invalid_input = True
    while invalid_input:
        restart = input('\nRestart? ')
        if restart == 'yes':
            print("Starting new game...")
            print('-' * 50)
            return 1
        elif restart == 'no':
            print("Thanks for playing. Goodbye!")
            print('-' * 50)
            return 0
        else:
            print("Invalid Input. Please write yes or no")

# Starts a new game
def start_game():
    #Start State
    board = np.zeros((6, 6), dtype=int)    

    turn = 1
    game_ongoing = True

    while game_ongoing:

        # Take and apply Valid move
        invalid_move = True
        while invalid_move:
            move_made = request_player_input(board, turn)
            row = move_made[0]
            col = move_made[1]
            rot = move_made[2]

            # Validates move
            if check_move(board, row, col):
                board = apply_move(board, turn, row, col, rot)
                invalid_move = False
                print(f'\nYou played move [Row: {row}, Col: {col}, Rot: {rot}]')
            else:
                print(f'Entered move: Row: {row}, Col: {col}, Rot: {rot} is not a valid move')

        # Checks for victory. If outcome is win or tie, game
        turn_outcome = check_victory(board, turn, rot)
        if turn_outcome == 1:
            display_board(board)
            print("Player 1 wins!")
            game_ongoing = False
        elif turn_outcome == 2:
            display_board(board)
            print("Player 2 wins!")
            game_ongoing = False
        elif turn_outcome == 3:
            display_board(board)
            print("Draw! Both players tie")
            game_ongoing = False

        #Change turn
        turn = 3 - turn

# Starts a new game with the computer
def start_game_computer(level):
    #Start State
    board = np.zeros((6, 6), dtype=int)    

    turn = 1
    game_ongoing = True

    while game_ongoing:
        
        if turn == 1:
            # Take and apply Valid move
            invalid_move = True
            while invalid_move:
                move_made = request_player_input(board, turn)
                row = move_made[0]
                col = move_made[1]
                rot = move_made[2]

                # Validates move
                if check_move(board, row, col):
                    board = apply_move(board, turn, row, col, rot)
                    invalid_move = False
                    print(f'\nYou played move [Row: {row}, Col: {col}, Rot: {rot}]')
                else:
                    print(f'Entered move: Row: {row}, Col: {col}, Rot: {rot} is not a valid move')
        elif turn == 2:
            display_board(board)
            move_made = computer_move(board, turn, level)
            row = move_made[0]
            col = move_made[1]
            rot = move_made[2]
            board = apply_move(board, turn, row, col, rot)
            print(f'\nBot played move [Row: {row}, Col: {col}, Rot: {rot}]')
            print('-' * 50)

        # Checks for victory. If outcome is win or tie, game
        turn_outcome = check_victory(board, turn, rot)
        if turn_outcome == 1:
            display_board(board)
            print("Player 1 wins!")
            game_ongoing = False
        elif turn_outcome == 2:
            display_board(board)
            print("Player 2 wins!")
            game_ongoing = False
        elif turn_outcome == 3:
            display_board(board)
            print("Draw! Both players tie")
            game_ongoing = False

        #Change turn
        turn = 3 - turn

# Prints menu UI and requests for choice (1,2,3)
def menu_input():
    print("\nMENU")
    print("1. Start Game")
    print("2. Instructions")
    print("3. Quit")
    print('-' * 50)

    invalid_input = True
    while invalid_input:
        choice = input("\nEnter your choice (1/2/3): ")
        if choice in ["1", "2", "3"]:
            invalid_input = False
        else:
            print("Invalid Input entered")
    print('-' * 50)
    return choice

# Prints player vs computer UI and request for choice (a, b)
def computer_input():
    print ('\nCHOOSE YOUR GAMEMODE')
    print ('a. Play with human')
    print ('b. Play with computer - Level 1')
    print ('c. Play with computer - Level 2')

    invalid_input = True
    while invalid_input:
        choice = input("\nEnter your choice (a/b/c): ")
        if choice in ["a", "b", "c"]:
            invalid_input = False
        else:
            print("Invalid Input entered")
    print('-' * 50)
    return choice

# Prints instructions
def instruction():
    print ("A player wins by getting five consecutive of their marbles in a vertical, horizontal or diagonal row.")
    print ("If all 36 spaces on the board are occupied without a row of five consecutive being formed then the gameis a draw.")
    print ()
    print ("Rows and colums are assigned with index (0-5).")
    print ()
    print ("Rotations are assigned with index (1-8).")
    print ()
    print ("1 = Upper Right Clockwise")
    print ("2 = Upper Right Anti-Clockwise")
    print ("3 = Lower Right Clockwise")
    print ("4 = Lower Right Anti-Clockwise")
    print ("5 = Lower Left Clockwise")
    print ("6 = Lower Left Anti-Clockwise")
    print ("7 = Upper Left Clockwise")
    print ("8 = Upper Left Anti-Clockwise")
    print('-' * 50)

# Main menu function
def menu():
    print('\nWelcome to Pentago')
    pentago_on = True
    while pentago_on:
        menu_input_choice = menu_input()
        if menu_input_choice == "1":
            game_state = True
            #Enter Game State
            while game_state:

                #Requests player for game type (PvP, PvE Lvl 1, PvE Lvl 2), and triggers game
                computer_input_choice = computer_input()
                if computer_input_choice == "a":
                    start_game()
                elif computer_input_choice == "b":
                    start_game_computer(1)
                else:
                    start_game_computer(2)
                
                #Asks if player would like to restart
                restart = restart_procedure()
                if restart == 0:
                    game_state = False

        elif menu_input_choice == "2":
            instruction()
        elif menu_input_choice == "3":
            pentago_on = False
            print("Shutting Off... Good Bye")


if __name__ == "__main__":
    menu()