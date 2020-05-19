import chess
import random

'''
	Your Code Will Come Here
'''

# this function should always be named as ai_play and
# this function's return value is used as AI's move so it will AI's your final decision.
# You can add as many function as you want to above.
# At each turn you will get a board to ai_play and calculate best move and return it.

""" MY CODES AND COMMENTS """
# Source of evaluation function and tables
# Simplified Evaluation Function
# https: // www.chessprogramming.org/Simplified_Evaluation_Function
#
# this table prepared for each piece and
# which square is the most sensible for the pieces

# for example knight must avoid from edges of table
# because number available movement are decreasing in edges


pTable = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, -20, -20, 10, 10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5,  5, 10, 25, 25, 10,  5,  5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0,  0,  0,  0,  0,  0,  0,  0]

kTable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -30,  5, 10, 15, 15, 10,  5, -30,
    -30,  0, 15, 20, 20, 15,  0, -30,
    -30,  5, 15, 20, 20, 15,  5, -30,
    -30,  0, 10, 15, 15, 10,  0, -30,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

bTable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10,  0, 10, 10, 10, 10,  0, -10,
    -10,  5,  5, 10, 10,  5,  5, -10,
    -10,  0,  5, 10, 10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

rTable = [
    0,  0,  0,  5,  5,  0,  0,  0,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    5, 10, 10, 10, 10, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0]

qTable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  5,  5,  5,  5,  5,  0, -10,
    0,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

xTable = [
    20, 30, 10,  0,  0, 10, 30, 20,
    20, 20,  0,  0,  0,  0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]


turn = True
# turn is a global value that hold what color ai plays


def ai_play(board):
    global turn
    # set the first movement as ai and color as boolean value
    # if white => turn = True
    # if black => trun = False
    turn = board.turn
    try:
        move = minimaxRoot(3, board, True)
        return str(move)
    except:
        move = ""


# PAWN function is used for exchange if pawn is near to exchange its value increasing
def PAWN(piece, i):
    value = 0
    if piece == "P":
        value = -10*i
    elif piece == "p":
        value = 10*i
    return value

# exchange for each pawn increase value for its place
# if it is near to exchange location value of pawn is increasing


def exchange(board):
    value = 0
    i = 0
    while i < 63:
        i += 1
        value += PAWN(str(board.piece_at(i)), int(i/8))
    return value


# value function evaluates the board according to pieces and where they stand
# The function returns -9999 if white is mated, 9999 if black is mated and 0 for a draw.


def valueFunction(board):
    exchangeVal = exchange(board)

    if board.is_checkmate():
        exchangeVal = 0
        if board.turn:
            return -999999
        else:
            return 999999

    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    # pieceValues = number of difference for each piece and multiplied by their value in board
    # for pawn (5-3)*100 = 200
    pValue = 100  # pawn value
    nValue = 320  # knight value
    bValue = 330  # bishop value
    rValue = 500  # rook value
    qValue = 900  # queen value

    pieceValues = pValue*(wp-bp)+nValue*(wn-bn)+bValue * \
        (wb-bb)+rValue*(wr-br)+qValue*(wq-bq)

    # for each piece evaluate values for where in piece-square tables
    # and difference between opponents pieces values for where in piece-square tables

    pawnSquare = sum([pTable[i]
                      for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnSquare = pawnSquare + sum([-pTable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.PAWN, chess.BLACK)])
    nightSquare = sum([kTable[i]
                       for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    nightSquare = nightSquare + sum([-kTable[chess.square_mirror(i)]
                                     for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopSquare = sum([bTable[i]
                        for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopSquare = bishopSquare + sum([-bTable[chess.square_mirror(i)]
                                       for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rookSquare = sum([rTable[i]
                      for i in board.pieces(chess.ROOK, chess.WHITE)])
    rookSquare = rookSquare + sum([-rTable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.ROOK, chess.BLACK)])
    queenSquare = sum([qTable[i]
                       for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queenSquare = queenSquare + sum([-qTable[chess.square_mirror(i)]
                                     for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingSquare = sum([xTable[i]
                      for i in board.pieces(chess.KING, chess.WHITE)])
    kingSquare = kingSquare + sum([-xTable[chess.square_mirror(i)]
                                   for i in board.pieces(chess.KING, chess.BLACK)])

    # eval function is sum of pieceValues
    # and evaluated value for each piece
    # according to piece square table
    eval = pieceValues + pawnSquare + nightSquare + bishopSquare + \
        rookSquare + queenSquare + kingSquare + exchangeVal
    if board.turn:
        return eval
    else:
        return -eval

# minimaxRoot funtion run minimax function according to depth and isMax variables depth is
# depth of tree and isMax is boolean that responsible to minimax funtion for maximizing or minimizing
# if we want to minimum we can give isMax = False
# if we want to maximum we can give isMax = True


# it actually like 0 depth minimax funtion looks just own children and takes the max or min according to our mention


def minimaxRoot(depth, board, isMax):
    canMove = board.legal_moves
    best = -9999
    best2 = -9999
    best3 = -9999
    bestFinal = None
    for i in canMove:
        move = chess.Move.from_uci(str(i))
        board.push(move)
        value = max(best, minimax(depth - 1, board, not isMax))
        board.pop()

        if(value > best):
            best3 = best2
            best2 = best
            best = value
            bestFinal = move

    print("secondBest: ", best2)
    print("Best: ", best)
    print("best: " + str(bestFinal))
    return bestFinal


# minimax function is for minimizing the possible loss for a worst case (maximum loss) scenario.
# When dealing with gains, it is referred to as "maximin"—to maximize the minimum gain.

# minimax do a move in legalMoves and evaluate the board it does this evaluation and creates a tree width given depth
# and selects minimum loss for worst case scenerio.
# and returns highest value evaluated by valueFunction and which move that has.
def minimax(depth, board, isMax):
    global turn

    # check any position is checkmate for ai (if ai wins) and use this move
    # otheswise if checkmate is not in last depth they may not be max value
    # unless did checkmate ai may not use this movements

    if board.is_checkmate():
        if board.turn != turn:
            return 999999
        else:
            return -999999

    # and ai mustn't to stalemate
    if board.is_stalemate():
        return 0

    if(depth == 0):
        return -valueFunction(board)
    canMove = board.legal_moves
    if(isMax):
        best = -9999
        for i in canMove:
            move = chess.Move.from_uci(str(i))
            board.push(move)
            best = max(best, minimax(depth - 1, board, not isMax))
            board.pop()
        return best
    else:
        best = 9999
        for x in canMove:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            best = min(best, minimax(depth - 1, board, not isMax))
            board.pop()
        return best
