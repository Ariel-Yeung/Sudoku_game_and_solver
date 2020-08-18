# Man Yi (Ariel) Yeung Personal Project

# This is the main code to be ran.
# It uses model from "sudoku_solver.py", view and controller from "sudoku_solv_gui.py" and data from "./data/sudoku.csv"

import pandas as pd
import random

import sys
from queue import Queue
from PyQt5.QtWidgets import QApplication

from sudoku_solver import solv_sudoku
from sudoku_solv_gui import (SudokuUI, SudokuCtrl)

                             
sdk=QApplication([])

# "sudoku.csv" from Kyuyong Park at https://www.kaggle.com/bryanpark/sudoku
sudoku_src=pd.read_csv("./data/sudoku.csv")

# randomly choose 20 puzzles
index=random.sample(range(sudoku_src.shape[0]), 20)     
puzzle_src=sudoku_src.iloc[index,0].tolist()

# create queue of puzzles
puzzle_queue=Queue()
for i in range(len(puzzle_src)):
    puzzle_flat=list([int(j) for j in list(puzzle_src[i])])
    puzzle=[]
    for i in range(9):
        puzzle.append(puzzle_flat[9*i:9*(i+1)])
    puzzle_queue.put(puzzle)
    
view=SudokuUI(puzzle_queue)
view.show()
SudokuCtrl(view=view, solver=solv_sudoku)#, puzzle=sudoku_list)
sys.exit(sdk.exec_())