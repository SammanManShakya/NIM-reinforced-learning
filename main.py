import random


# Player move function
def player_move(move, sticks, max_sticks):
    if move < 1 or move > min(sticks, max_sticks):  # Check if move is valid
        print("Invalid move")
        move = int(input("Enter your move: "))
        return player_move(move, sticks, max_sticks)
    else:
        return move  # Return how many sticks the player takes

# MAX-Value function
# def max_value(sticks, alpha, beta, max_sticks):
#     if sticks <= 0:
#         return -1
#     value = -1
#     for move in range(1, min(sticks,max_sticks)+1):
#         v = min_value(sticks - move, alpha, beta, max_sticks)
#         value = max(value, v)
#         if value >= beta:
#             return value
#         alpha = max(alpha, value)
#
#     return value


# MIN-Value function
# def min_value(sticks, alpha, beta, max_sticks):
#     if sticks <= 0:
#         return 1
#     value = 1
#     for move in range(1, min(sticks, max_sticks) + 1):
#         v = max_value(sticks - move, alpha, beta, max_sticks)
#         value = min(value, v)
#         if value <= alpha:
#             return value
#         beta = min(value, beta)
#
#     return value



# def computer_move(sticks, max_sticks):
#     best_move = None
#     alpha = -1
#     beta = 1
#     value = -1
#     for move in range(1, min(sticks, max_sticks) + 1):
#         v = min_value(sticks - move, alpha, beta, max_sticks)
#         if v > value:
#             value = v
#             best_move = move
#         if value >= beta:
#             return best_move
#         alpha = max(alpha, value)
#
#     if best_move is None:
#         best_move = random.randint(1,min(sticks, max_sticks))
#         return best_move
#     else:
#         return best_move


def create_matrix(max_sticks, sticks):
    return [[0] * sticks for _ in range(max_sticks)]


def computer_move(matrix,max_sticks,sticks):
    max_index = None
    max_value = float('-inf')

    for i, row in enumerate(matrix):
        if row[9] > max_value:
            max_value = row[9]
            max_index = i

    if max_index is not None:
        return min(max_index,sticks)
    else:
        # If no valid move is found, return a random move
        return min(random.randint(0, 2),sticks)


def update_Qvalues(move_index, matrix, computer_win, index_when_move):
    print("Move index:", move_index)
    print("Matrix:", matrix)
    print("Index when move:", index_when_move)
    for i in index_when_move:
        print(i)
        print(move_index)
        if computer_win:
            matrix[move_index][i] += 1
        else:
            matrix[move_index][i] -= 1

    with open("training_data.txt", "w") as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')



def nim():
    max_sticks = 3
    sticks = 10
    matrix = []
    print('|' * sticks)
    print(f"There are {sticks} sticks left")
    try:
        with open("training_data.txt", 'r') as file:
            for line in file:
                row = list(map(int, line.strip().split()))
                matrix.append(row)
    except FileNotFoundError:
        print("File not found. Creating a new file...")
        matrix = create_matrix(max_sticks, sticks)
        with open("training_data.txt", 'w') as file:
            for row in matrix:
                file.write(' '.join(map(str, row)) + '\n')

    move = computer_move(matrix,max_sticks,sticks)
    computer_win = True
    index_sticks_when_move = [9]
    while sticks > 0:
        c_move = move + 1  # Increment move by 1 to match expected indexing
        c_move = computer_move(matrix,max_sticks,sticks) + 1
        print(f"The computer takes {c_move} sticks")
        sticks -= c_move
        print('|' * sticks)
        print(f"There are {sticks} sticks left")
        if sticks == 0:
            print("Computer wins!")
            break
        player_input = int(input("Enter how many sticks you want to take: "))
        p_move = player_move(player_input, sticks, max_sticks)
        sticks -= p_move
        print('|' * sticks)
        print(f"There are {sticks} sticks left")
        if sticks == 0:
            index_sticks_when_move.append(sticks)
        else:
            index_sticks_when_move.append(sticks - 1)
        if sticks == 0:
            print("You Win!")
            computer_win = False
            break

    update_Qvalues(move, matrix, computer_win, sorted(index_sticks_when_move))


nim()