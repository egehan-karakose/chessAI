####################################################
# You may only change the initial board here       #
# Any change other than board may result in crash  #
####################################################

from gui import App
from PyQt5 import QtWidgets
import sys
import chess

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # initial board is created here
    board = chess.Board(
        "1Q6/8/8/2R3K1/8/8/8/k7 w - - 0 1")
    ex = App(board)
    app.exec_()
