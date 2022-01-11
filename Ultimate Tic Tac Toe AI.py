'''
I wrote this program with the intention to have my robot play against you.  However, after finishing this AI, I realized that my Raspberry Pi 3 did not have the power to run this code with a high enough depth (aka "thinkPower") in a reasonable time.  So I decided to write an AI for "Sim," a less computationally complex game, and use that instead.
'''

from array import *
from random import *

thinkPower = 5

#for issues with twoempty stuff


twoempty = 3
twoemptymax = 6
twofull = 2
center = 1
three = 10
twoemptybig = 15
twofullbig = 10
centerbig = 5

board = [[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
         [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]




bigboard = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'a']



def printBoard(board):
    print("\n")
    print(board[0][0] + '|' + board[0][1] + '|' + board[0][2] + ' + ' + board[1][0] + '|' + board[1][1] + '|' + board[1][2] + ' + ' + board[2][0] + '|' + board[2][1] + '|' + board[2][2])
    print(board[0][3] + '|' + board[0][4] + '|' + board[0][5] + ' + ' + board[1][3] + '|' + board[1][4] + '|' + board[1][5] + ' + ' + board[2][3] + '|' + board[2][4] + '|' + board[2][5])
    print(board[0][6] + '|' + board[0][7] + '|' + board[0][8] + ' + ' + board[1][6] + '|' + board[1][7] + '|' + board[1][8] + ' + ' + board[2][6] + '|' + board[2][7] + '|' + board[2][8])
    print("+++++++++++++++++++++")
    print(board[3][0] + '|' + board[3][1] + '|' + board[3][2] + ' + ' + board[4][0] + '|' + board[4][1] + '|' + board[4][2] + ' + ' + board[5][0] + '|' + board[5][1] + '|' + board[5][2])
    print(board[3][3] + '|' + board[3][4] + '|' + board[3][5] + ' + ' + board[4][3] + '|' + board[4][4] + '|' + board[4][5] + ' + ' + board[5][3] + '|' + board[5][4] + '|' + board[5][5])
    print(board[3][6] + '|' + board[3][7] + '|' + board[3][8] + ' + ' + board[4][6] + '|' + board[4][7] + '|' + board[4][8] + ' + ' + board[5][6] + '|' + board[5][7] + '|' + board[5][8])
    print("+++++++++++++++++++++")
    print(board[6][0] + '|' + board[6][1] + '|' + board[6][2] + ' + ' + board[7][0] + '|' + board[7][1] + '|' + board[7][2] + ' + ' + board[8][0] + '|' + board[8][1] + '|' + board[8][2])
    print(board[6][3] + '|' + board[6][4] + '|' + board[6][5] + ' + ' + board[7][3] + '|' + board[7][4] + '|' + board[7][5] + ' + ' + board[8][3] + '|' + board[8][4] + '|' + board[8][5])
    print(board[6][6] + '|' + board[6][7] + '|' + board[6][8] + ' + ' + board[7][6] + '|' + board[7][7] + '|' + board[7][8] + ' + ' + board[8][6] + '|' + board[8][7] + '|' + board[8][8])
    print("\n")

printBoard(board)

def spaceIsFree(board, box, position):
    if board[box][position] == ' ':
        return True
    else:
        return False

def spaceCheck(board, box, positions):
    playerCount = 0
    aiCount = 0
    for square in positions:
        if board[box][square] == player:
            playerCount += 1
        elif board[box][square] == ai:
            aiCount += 1
    return [playerCount, aiCount]

def spaceCheckOnBigBoard(bigboard, positions):
    
    playerCount = 0
    aiCount = 0
    for square in positions:
        if bigboard[square] == player:
            playerCount += 1
        elif bigboard[square] == ai:
            aiCount += 1
    return [playerCount, aiCount]
    
def checkForWin(bigboard):
    if bigboard[0] == bigboard[1] and bigboard[0] == bigboard[2] and bigboard[0] != ' ':
        return True
    elif bigboard[3] == bigboard[4] and bigboard[3] == bigboard[5] and bigboard[3] != ' ':
        return True
    elif bigboard[6] == bigboard[7] and bigboard[6] == bigboard[8] and bigboard[6] != ' ':
        return True
    elif bigboard[0] == bigboard[3] and bigboard[0] == bigboard[6] and bigboard[0] != ' ':
        return True
    elif bigboard[1] == bigboard[4] and bigboard[1] == bigboard[7] and bigboard[1] != ' ':
        return True
    elif bigboard[2] == bigboard[5] and bigboard[2] == bigboard[8] and bigboard[2] != ' ':
        return True
    elif bigboard[0] == bigboard[4] and bigboard[0] == bigboard[8] and bigboard[0] != ' ':
        return True
    elif bigboard[2] == bigboard[4] and bigboard[2] == bigboard[6] and bigboard[2] != ' ':
        return True
    else:
        return False


def checkWhichMarkWonInBox(board, box, mark):
    if board[box][0] == board[box][1] and board[box][0] == board[box][2] and board[box][0] == mark:
        return True
    elif board[box][3] == board[box][4] and board[box][3] == board[box][5] and board[box][3] == mark:
        return True
    elif board[box][6] == board[box][7] and board[box][6] == board[box][8] and board[box][6] == mark:
        return True
    elif board[box][0] == board[box][3] and board[box][0] == board[box][6] and board[box][0] == mark:
        return True
    elif board[box][1] == board[box][4] and board[box][1] == board[box][7] and board[box][1] == mark:
        return True
    elif board[box][2] == board[box][5] and board[box][2] == board[box][8] and board[box][2] == mark:
        return True
    elif board[box][0] == board[box][4] and board[box][0] == board[box][8] and board[box][0] == mark:
        return True
    elif board[box][2] == board[box][4] and board[box][2] == board[box][6] and board[box][2] == mark:
        return True
    else:
        return False

    
def checkWhichMarkWon(bigboard, mark):
    if bigboard[0] == bigboard[1] and bigboard[0] == bigboard[2] and bigboard[0] == mark:
        return True
    elif bigboard[3] == bigboard[4] and bigboard[3] == bigboard[5] and bigboard[3] == mark:
        return True
    elif bigboard[6] == bigboard[7] and bigboard[6] == bigboard[8] and bigboard[6] == mark:
        return True
    elif bigboard[0] == bigboard[3] and bigboard[0] == bigboard[6] and bigboard[0] == mark:
        return True
    elif bigboard[1] == bigboard[4] and bigboard[1] == bigboard[7] and bigboard[1] == mark:
        return True
    elif bigboard[2] == bigboard[5] and bigboard[2] == bigboard[8] and bigboard[2] == mark:
        return True
    elif bigboard[0] == bigboard[4] and bigboard[0] == bigboard[8] and bigboard[0] == mark:
        return True
    elif bigboard[2] == bigboard[4] and bigboard[2] == bigboard[6] and bigboard[2] == mark:
        return True
    else:
        return False

def checkForDrawInBox(board, box):
    
    for i in board[box]:
        if i == ' ':
            return False
    return True

def checkForDraw(bigboard):
    for i in bigboard:
        if i == ' ':
            return False
    return True

player = 'X'
ai = 'O'
currentBox = 9

def insertLetter(bigboard, board, letter, box, position):
    global currentBox
    if spaceIsFree(board, box, position):
        board[box][position] = letter
        if checkForDraw(bigboard):
            print("Draw")
            exit()
        if checkWhichMarkWonInBox(board, box, letter): 
            bigboard[box] = letter
            for i in range(0, 9):
                board[box][i] = letter
            if checkWhichMarkWon(bigboard, letter):
                printBoard(board)
                if letter == player:
                    print("Player wins")
                else:
                    print("AI wins")
                exit()    
        elif checkForDrawInBox(board, box):
            bigboard[box] = "-"
        printBoard(board)

        currentBox = position

    else:
        print("Invalid move")
        if bigboard[currentBox] != ' ':
            currentBox = int(input("Enter the box you'd like to play in "))
        position = int(input("Enter the position for 'X' in the box: "))
        insertLetter(bigboard, board, letter, currentBox, position)
        return



def playerMove(bigboard, board):
    global currentBox
    if bigboard[currentBox] != ' ':
        currentBox = int(input("Enter the box you'd like to play in "))
    position = int(input("Enter the position for 'X' in the box: "))
    insertLetter(bigboard, board, player, currentBox, position)

def aiMove(bigboard, board):

    if checkForDraw(bigboard):
        print ("draw")
        exit()
        
    global currentBox

    bestScore = -10000
    bestMove = [0,0]  #WHERES THE BEST BOX STUFF

    if bigboard[currentBox] != ' ':
        for boxTemp in range (0, 9):
            if bigboard[boxTemp] == ' ':
                for square in range (0, 9):
                    if board[boxTemp][square] == ' ':
                        board[boxTemp][square] = ai
                        move = [boxTemp, square]
                        #this stuff for win/draw cases in a box
                        if checkWhichMarkWonInBox(board, boxTemp, ai):
                            bigboard[boxTemp] = 'O'
                        elif checkWhichMarkWonInBox(board, boxTemp, player):
                            bigboard[boxTemp] = 'X'
                        elif checkForDrawInBox(board, boxTemp):
                            bigboard[boxTemp] = '-'
                        #end of stuff
                        score = minimax(board, bigboard, square, thinkPower, -100000, 100000, False)
                        board[boxTemp][square] = ' '
                        bigboard[boxTemp] = ' ' #reset
                        if score[0] > bestScore:
                            bestScore = score[0]
                            bestMove = move

    else:
        for square in range (0, 9):
            if board[currentBox][square] == ' ':
                board[currentBox][square] = ai
                move = [currentBox, square]
                #this stuff for win/draw cases in a box
                if checkWhichMarkWonInBox(board, currentBox, ai):
                    bigboard[currentBox] = 'O'
                elif checkWhichMarkWonInBox(board, currentBox, player):
                    bigboard[currentBox] = 'X'
                elif checkForDrawInBox(board, currentBox):
                    bigboard[currentBox] = '-'
                score = minimax(board, bigboard, square, thinkPower, -100000, 100000, False)
                #end of stuff
                board[currentBox][square] = ' '
                bigboard[currentBox] = ' ' #reset
                if score[0] > bestScore:
                    bestScore = score[0]
                    bestMove = move

    print(bestMove)
    print(bestScore)
    print(bigboard)
    insertLetter(bigboard, board, ai, bestMove[0], bestMove[1])


def minimax(board, bigboard, box, depth, alpha, beta, maximizingPlayer):
    global currentBox
    
    if depth == 0 or checkForWin(bigboard) or checkForDraw(bigboard):
        score = evaluatePosition(bigboard, board, box, depth)
        if score[0] == -1000:
            print(depth)
        return score

    if maximizingPlayer: #look at this later about the currentBox losing thingy
        bestScore = -10000
        bestBox = 0

        if bigboard[box] != ' ':
            for boxTemp in range (0, 9):
                if bigboard[boxTemp] == ' ':
                    for square in range (0, 9):
                        if board[boxTemp][square] == ' ':
                            board[boxTemp][square] = ai
                            #this stuff for win/draw cases in a box
                            if checkWhichMarkWonInBox(board, boxTemp, ai):
                                bigboard[boxTemp] = 'O'
                            elif checkWhichMarkWonInBox(board, boxTemp, player):
                                bigboard[boxTemp] = 'X'
                            elif checkForDrawInBox(board, boxTemp):
                                bigboard[boxTemp] = '-'
                            #end of stuff
                            score = minimax(board, bigboard, square, depth-1, alpha, beta, False)
                            board[boxTemp][square] = ' '
                            bigboard[boxTemp] = ' ' #reset
                            if score[0] > bestScore:
                                bestScore = score[0]
                                bestBox = boxTemp
                            alpha = max(alpha, score[0])
                            if beta <= alpha:
                                break
            return [bestScore, bestBox]

        else:
            for square in range (0, 9):
                if board[box][square] == ' ':
                    board[box][square] = ai
                    #this stuff for win/draw cases in a box
                    if checkWhichMarkWonInBox(board, box, ai):
                        bigboard[box] = 'O'
                    elif checkWhichMarkWonInBox(board, box, player):
                        bigboard[box] = 'X'
                    elif checkForDrawInBox(board, box):
                        bigboard[box] = '-'
                    #end of stuff
                    score = minimax(board, bigboard, square, depth-1, alpha, beta, False)
                    board[box][square] = ' '
                    bigboard[box] = ' ' #reset
                    if score[0] > bestScore:
                        bestScore = score[0]
                        bestBox = box
                    alpha = max(alpha, score[0])
                    if beta <= alpha:
                        break
            return [bestScore, bestBox]

    
    else:
        bestScore = 10000
        bestBox = 0

        if bigboard[box] != ' ':
            for boxTemp in range (0, 9):
                if bigboard[boxTemp] == ' ':
                    for square in range (0, 9):
                        if board[boxTemp][square] == ' ':
                            board[boxTemp][square] = player
                            #this stuff for win/draw cases in a box
                            if checkWhichMarkWonInBox(board, boxTemp, ai):
                                bigboard[boxTemp] = 'O'
                            elif checkWhichMarkWonInBox(board, boxTemp, player):
                                bigboard[boxTemp] = 'X'
                            elif checkForDrawInBox(board, boxTemp):
                                bigboard[boxTemp] = '-'
                            #end of stuff
                            score = minimax(board, bigboard, square, depth-1, alpha, beta, True)
                            board[boxTemp][square] = ' '
                            bigboard[boxTemp] = ' ' #reset
                            if score[0] < bestScore:
                                bestScore = score[0]
                                bestBox = boxTemp
                            beta = min(beta, score[0])
                            if beta <= alpha:
                                break
            return [bestScore, bestBox]
    
        else:
            for square in range (0, 9):
                if board[box][square] == ' ':
                    board[box][square] = player
                    #this stuff for win/draw cases in a box
                    if checkWhichMarkWonInBox(board, box, ai):
                        bigboard[box] = 'O'
                    elif checkWhichMarkWonInBox(board, box, player):
                        bigboard[box] = 'X'
                    elif checkForDrawInBox(board, box):
                        bigboard[box] = '-'
                    #end of stuff
                    score = minimax(board, bigboard, square, depth-1, alpha, beta, True)
                    board[box][square] = ' '
                    bigboard[box] = ' ' #reset
                    if score[0] < bestScore:
                        bestScore = score[0]
                        bestBox = box
                    beta = min(beta, score[0])
                    if beta <= alpha:
                         break
            return [bestScore, bestBox]
    

def evaluatePosition(bigboard, board, boxPlayedIn, depth):
    scoreEval = 0 

    twoemptyAi = 0
    twoemptyPlayer = 0

    if checkForWin(bigboard):
        if checkWhichMarkWon(bigboard, player):
            return [-1000-depth, boxPlayedIn]
        else:
            return [1000-depth, boxPlayedIn]

    if checkForDraw(bigboard):
            return[0, boxPlayedIn]
    
    for box in range (0, 9): #all the analysis for the boxes:
        if (bigboard[box] == ' '):
            #two in a row, with open square
            for row in range (0, 3): #row
                if (spaceCheck(board, box, [3*row, 3*row+1, 3*row+2]) == [0, 2]): #ai
                    twoemptyAi += twoempty
                    
                if (spaceCheck(board, box, [3*row, 3*row+1, 3*row+2]) == [2, 0]): #player
                    twoemptyPlayer += twoempty

            for col in range (0, 3): #col
                if (spaceCheck(board, box, [col, col+3, col+6]) == [0, 2]): #ai
                    twoemptyAi += twoempty
                if (spaceCheck(board, box, [col, col+3, col+6]) == [2, 0]): #player
                    twoemptyPlayer += twoempty

            if (spaceCheck(board, box, [0, 4, 8]) == [0, 2]): #diag1 ai
                    twoemptyAi += twoempty
            if (spaceCheck(board, box, [0, 4, 8]) == [2, 0]): #diag1 player
                    twoemptyPlayer += twoempty
            if (spaceCheck(board, box, [2, 4, 6]) == [0, 2]): #diag2 ai
                    twoemptyAi += twoempty
            if (spaceCheck(board, box, [2, 4, 6]) == [2, 0]): #diag2 player
                    twoemptyPlayer += twoempty

            if twoemptyAi > 9:
                twoemptyAi = 9
            if twoemptyPlayer > 9:
                twoemptyPlayer = 9
            scoreEval = twoemptyAi - twoemptyPlayer

            #two in a row, with closed square
            for row in range (0, 3): #row
                if (spaceCheck(board, box, [3*row, 3*row+1, 3*row+2]) == [2, 1]): #ai
                    scoreEval += twofull
                if (spaceCheck(board, box, [3*row, 3*row+1, 3*row+2]) == [1, 2]): #player
                    scoreEval -= twofull

            for col in range (0, 3): #col
                if (spaceCheck(board, box, [col, col+3, col+6]) == [2, 1]): #ai
                    scoreEval += twofull
                if (spaceCheck(board, box, [col, col+3, col+6]) == [1, 2]): #player
                    scoreEval -= twofull

            if (spaceCheck(board, box, [0, 4, 8]) == [2, 1]): #diag1 ai
                scoreEval = scoreEval + twofull
            if (spaceCheck(board, box, [0, 4, 8]) == [1, 2]): #diag1 player
                scoreEval = scoreEval - twofull
            if (spaceCheck(board, box, [2, 4, 6]) == [2, 1]): #diag2 ai
                scoreEval = scoreEval + twofull
            if (spaceCheck(board, box, [2, 4, 6]) == [1, 2]): #diag2 player
                scoreEval = scoreEval - twofull

            #center square positional thingy
            if (spaceCheck(board, box, [4]) == [0, 1]): #center ai
                scoreEval += center
            if (spaceCheck(board, box, [4]) == [1, 0]): #center player
                scoreEval -= center

    for box in range(0, 9):
        if bigboard[box] == 'O':
            scoreEval += three
        elif bigboard[box] == 'X':
            scoreEval -= three
    
    #analysis on the bigboard
    #two in a row, open
    for row in range (0, 3): #row
        if (spaceCheckOnBigBoard(bigboard, [3*row, 3*row+1, 3*row+2]) == [0, 2]): #ai
            scoreEval += twoemptybig
        if (spaceCheckOnBigBoard(bigboard, [3*row, 3*row+1, 3*row+2]) == [2, 0]): #player
            scoreEval -= twoemptybig

    for col in range (0, 3): #col
        if (spaceCheckOnBigBoard(bigboard, [col, col+3, col+6]) == [0, 2]): #ai
            scoreEval += twoemptybig
        if (spaceCheckOnBigBoard(bigboard, [col, col+3, col+6]) == [2, 0]): #player
            scoreEval -= twoemptybig

    if (spaceCheckOnBigBoard(bigboard, [0, 4, 8]) == [0, 2]): #diag1 ai
        scoreEval = scoreEval + twoemptybig
    if (spaceCheckOnBigBoard(bigboard, [0, 4, 8]) == [2, 0]): #diag1 player
        scoreEval = scoreEval - twoemptybig
    if (spaceCheckOnBigBoard(bigboard, [2, 4, 6]) == [0, 2]): #diag2 ai
        scoreEval = scoreEval + twoemptybig
    if (spaceCheckOnBigBoard(bigboard, [2, 4, 6]) == [2, 0]): #diag2 player
        scoreEval = scoreEval - twoemptybig

    #two in a row, with closed square
    for row in range (0, 3): #row
        if (spaceCheckOnBigBoard(bigboard, [3*row, 3*row+1, 3*row+2]) == [2, 1]): #ai
            scoreEval += twofullbig
        if (spaceCheckOnBigBoard(bigboard, [3*row, 3*row+1, 3*row+2]) == [1, 2]): #player
            scoreEval -= twofullbig

    for col in range (0, 3): #col
        if (spaceCheckOnBigBoard(bigboard, [col, col+3, col+6]) == [2, 1]): #ai
            scoreEval += twofullbig
        if (spaceCheckOnBigBoard(bigboard, [col, col+3, col+6]) == [1, 2]): #player
            scoreEval -= twofullbig

    if (spaceCheckOnBigBoard(bigboard, [0, 4, 8]) == [2, 1]): #diag1 ai
        scoreEval = scoreEval + twofullbig
    if (spaceCheckOnBigBoard(bigboard, [0, 4, 8]) == [1, 2]): #diag1 player
        scoreEval = scoreEval - twofullbig
    if (spaceCheckOnBigBoard(bigboard, [2, 4, 6]) == [2, 1]): #diag2 ai
        scoreEval = scoreEval + twofullbig
    if (spaceCheckOnBigBoard(bigboard, [2, 4, 6]) == [1, 2]): #diag2 player
        scoreEval = scoreEval - twofullbig

    #center square positional thingy
    if (spaceCheckOnBigBoard(bigboard, [4]) == [0, 1]): #center ai
        scoreEval += centerbig
    if (spaceCheckOnBigBoard(bigboard, [4]) == [1, 0]): #center player
        scoreEval -= centerbig

    

    return [scoreEval, boxPlayedIn]

while not checkForWin(bigboard):
    playerMove(bigboard, board)
    aiMove(bigboard, board)

