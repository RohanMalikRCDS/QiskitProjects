
# Imports
import itertools
import os

# Setting up the board and game variables
board = ["", "", "", "", "", "", "", "", ""]  # 9 spaces in which players can move
turnNumber = 1  # counts up every turn (1 turn = each player moves once)
currentPlayer = "X"  # switches depending on whose turn it is
moves = []  # will be a list of [player, square1, square2, turnNum, classicalOrQuantum] for each move


# Visualize the board
def visualizeBoard(state):
    maxLen = max([len(item) for item in state]) + 2
    if maxLen % 2 == 1:
        maxLen += 1
    height = maxLen // 2
    if height % 2 == 0:
        height += 1
    row1 = "|".join([item.center(maxLen) for item in state[:3]])
    row2 = "|".join([item.center(maxLen) for item in state[3:6]])
    row3 = "|".join([item.center(maxLen) for item in state[6:]])

    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)
    print(row1)
    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)
    print("—"*(maxLen*3 + 2))
    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)
    print(row2)
    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)
    print("—"*(maxLen*3 + 2))
    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)
    print(row3)
    for _ in range(height // 2):
        print(" "*maxLen + "|" + " "*maxLen + "|" + " "*maxLen)


# Display all moves so far in the game

def getConnections(moveList):
    print("\n—————— Move List ——————")
    connections = []
    for move in moveList:
        connections.append(f"{move[0]}: {move[1]}—{move[2]}")
    for i, conn in enumerate(connections):
        print(conn, end=";\n" if i % 3 == 2 else "; ")
    if len(connections) % 3 != 0:
        print("\n")


# Check if a closed cyclic loop exists in a game state

def hasLoop(moveList):
    for moveset in itertools.combinations([move for move in moveList if move[4] != "C"], 3):
        if len(set(moveset[0][1:3] + moveset[1][1:3] + moveset[2][1:3])) == 3:
            toPrint = [f"{move[0]}: {move[1]}—{move[2]}" for move in moveset]
            print(f"Loop created: {'; '.join(toPrint)}")
            return moveset
    return None

# ----------------------
# Extract some functions for clarity and readability in game loop
# ----------------------


# Display game state
def showState():
    os.system("clear")
    visualizeBoard(board)
    getConnections(moves)


# End of turn tasks
def endTurn(currPlayer, turnNum):
    # Switch player
    if currPlayer == "X":
        currPlayer = "O"
    else:
        currPlayer = "X"
        turnNum += 1
    return currPlayer, turnNum


# Check whether game is won
def isGameOver():
    global winner
    triplesToCheck = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    winningTriples = []
    for triple in triplesToCheck:
        if "[X" in board[triple[0]] and "[X" in board[triple[1]] and "[X" in board[triple[2]]:
            winner += "X"
            winningTriples.append(triple)
        if "[O" in board[triple[0]] and "[O" in board[triple[1]] and "[O" in board[triple[2]]:
            winner += "O"
            winningTriples.append(triple)
    if len(winner) > 1:
        minSumOfIndices, winningPlayer = 9999, ""
        for player, triple in zip(list(winner), winningTriples):
            sumOfIndices = 0
            for sq in triple:
                start = board[sq].find(f"[{player}")
                sumOfIndices += int(board[sq][start+2:board[sq].find("]", start)])
            if sumOfIndices < minSumOfIndices:
                minSumOfIndices = sumOfIndices
                winningPlayer = player
            elif sumOfIndices == minSumOfIndices:
                winningPlayer += player
        winner = winningPlayer
        return True
    else:
        return False


# Creating the main game loop
winner = ""  # will be populated with "X" or "O"
multipleCompletions = False  # if more than one three-in-a-row was completed at the same time on the winning move

while winner == "":
    showState()  # show state at the start of each turn
    print("\n———————————————————————")
    print("1|2|3")  # Show the layout of the board for reference
    print("—————")
    print("4|5|6")
    print("—————")
    print("7|8|9")
    # Get for the current player's move
    squares = input(f"Player {currentPlayer} — choose two squares for your superposed piece (two numbers, separated by a space): ").split(" ")
    squares[0], squares[1] = int(squares[0]), int(squares[1])  # parse the strings into integers
    # Add the move to the list of moves and change the board state
    moves.append([f"{currentPlayer}", squares[0], squares[1], turnNumber, "Q"])
    board[squares[0]-1] += ("/" if board[squares[0]-1] != "" else "") + f"{currentPlayer}{turnNumber}"
    board[squares[1]-1] += ("/" if board[squares[1]-1] != "" else "") + f"{currentPlayer}{turnNumber}"
    showState()  # Show updated state after each move
    # Check for a loop, and if one exists, prompt a collapse by the player who did not just create the loop
    loop = hasLoop(moves)
    if loop is not None:
        involvedSquares = set(loop[0][1:3] + loop[1][1:3] + loop[2][1:3])  # what 3 squares are involved in this collapse?
        collapseSquare = int(input(f"Player {'X' if currentPlayer == 'O' else 'O'} — choose a square in the loop ({str(involvedSquares)[1:-1]}) to collapse: "))
        # isolate the two relevant markers in the chosen square, then let the player pick which one stays
        relevantSquares = [f"{move[0]}{move[3]}" for move in loop if collapseSquare in move[1:-2]]
        relevantLocations = [(move[1], move[2]) for move in loop if collapseSquare in move[1:-2]]
        collapseChoice = input(f"Player {'X' if currentPlayer == 'O' else 'O'} — pick which marker stays in this square ({relevantSquares[0]} or {relevantSquares[1]}): ")
        if collapseChoice == relevantSquares[0]:
            involvedSquares.remove(collapseSquare)
            board[collapseSquare-1] = board[collapseSquare-1].replace(relevantSquares[1], "")  # remove the other marker
            board[collapseSquare-1] = board[collapseSquare-1].replace(relevantSquares[0], f"[{relevantSquares[0]}]")  # mark the chosen one as collapsed
            for loc in relevantLocations[0]:
                if loc != collapseSquare:
                    board[loc-1] = board[loc-1].replace(relevantSquares[0], "")  # remove chosen marker from its other location
            for square in involvedSquares:  # the other marker is also fixed now, in its other possible square
                if relevantSquares[1] in board[square-1]:
                    board[square-1] = board[square-1].replace(relevantSquares[1], f"[{relevantSquares[1]}]")
                    involvedSquares.remove(square)
                    break
            # now only one square left, and that needs to contain the unused marker of the relevant ones
            lastSquare = involvedSquares.pop()
            for move in loop:
                if collapseSquare not in move[1:3]:
                    board[lastSquare-1] = board[lastSquare-1].replace(f"{move[0]}{move[3]}", f"[{move[0]}{move[3]}]")
                    for sq in move[1:3]:
                        if sq != lastSquare:
                            board[sq-1] = board[sq-1].replace(f"{move[0]}{move[3]}", "")  # and finally remove the third marker from its other place

            # clean up board of extraneous slashes
            for i, sq in enumerate(board):
                if sq.startswith("/"):
                    board[i] = board[i][1:]
                if sq.endswith("/"):
                    board[i] = board[i][:-1]

            # turn the involved moves to classical tokens and show the board
            for move in moves:
                if move in loop:
                    move[4] = "C"
            showState()
        else:
            involvedSquares.remove(collapseSquare)
            board[collapseSquare-1] = board[collapseSquare-1].replace(relevantSquares[0], "")  # remove the other marker
            board[collapseSquare-1] = board[collapseSquare-1].replace(relevantSquares[1], f"[{relevantSquares[1]}]")  # mark the chosen one as collapsed
            for loc in relevantLocations[1]:
                if loc != collapseSquare:
                    board[loc-1] = board[loc-1].replace(relevantSquares[1],
                                                            "")  # remove chosen marker from its other location
            for square in involvedSquares:  # the other marker is also fixed now, in its other possible square
                if relevantSquares[0] in board[square-1]:
                    board[square-1] = board[square-1].replace(relevantSquares[0], f"[{relevantSquares[0]}]")
                    involvedSquares.remove(square)
                    break

            lastSquare = involvedSquares.pop()
            for move in loop:
                if collapseSquare not in move[1:3]:
                    board[lastSquare-1] = board[lastSquare-1].replace(f"{move[0]}{move[3]}", f"[{move[0]}{move[3]}]")
                    for sq in move[1:3]:
                        if sq != lastSquare:
                            board[sq-1] = board[sq-1].replace(f"{move[0]}{move[3]}", "")  # and finally remove the third marker from its other place

            # clean up board of extraneous slashes
            for i, sq in enumerate(board):
                if sq.startswith("/"):
                    board[i] = board[i][1:]
                if sq.endswith("/"):
                    board[i] = board[i][:-1]

            # turn the involved moves to classical tokens and show the board
            for move in moves:
                if move in loop:
                    move[4] = "C"
            showState()

    currentPlayer, turnNumber = endTurn(currentPlayer, turnNumber)
    print("\n———————————————————————")
    multipleCompletions = isGameOver()

if len(winner) > 1:
    print(f"Both players completed a tic-tac-toe with equal sums of piece indices: the game is a draw!")
else:
    if multipleCompletions:
        print(f"Both players completed a tic-tac-toe, but player {winner} wins because they had the smallest sum of piece indices!")
    else:
        print(f"Player {winner} has completed a tic-tac-toe!")
