# Man Yi (Ariel) Yeung Personal Project

# This file contains the GUI view and controller of the sudoku game.
# It has two classes: 
#      "SudokuUI" for the view, and 
#      "SudokuCtrl" as controller to connect the view to the model (solv_sudoku)


from datetime import datetime

from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtWidgets import (QMainWindow, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton)
from PyQt5.QtGui import QIntValidator

from functools import partial


class SudokuUI(QMainWindow):
    def __init__(self, puzzleQueue):
        super().__init__()
        self.setWindowTitle('Sudoku')
        self.setFixedSize(910,1200)
        
        #Central Widget
        self._centralWidget=QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self.generalLayout=QGridLayout()
        self._centralWidget.setLayout(self.generalLayout)
        self._centralWidget.setFixedSize(910,1100)
        
        # create elements of GUI
        self._createBoard()
        self._createButtons()
        self._createTimer()
        self._createErrCount()
        
        # get puzzle from Queue 
        self.second=0
        self._puzzleQueue=puzzleQueue
        self._puzzle=self._puzzleQueue.get()
        
    def _createButtons(self):
        self.buttons=[]                  
        self.buttons.append(QPushButton('Start'))
        self.buttons.append(QPushButton('Show Solution'))
        self.buttons.append(QPushButton('Clear Board'))
        
        # Add Spacings
        space=QWidget(self)
        space.setFixedSize(10,15)
        self.generalLayout.addWidget(space, 9, 0)
        
        # adding buttons
        a=0
        for b in self.buttons:
            b.setFixedSize(200,40)
            a+=1
            self.generalLayout.addWidget(b, 10+a, 0)

    def _createTimer(self):
        self.timeStarted=False                     
        self.second=0
        self._timer=QLabel('Timer: 00.00')
        self._timer.setFixedSize(200,40)
        self._timer.setStyleSheet("font-size: 25px")
        self.generalLayout.addWidget(self._timer, 11, 4)
        
    def _showTime(self):
        if self.timeStarted:
            self.second+=1  
            self._timer.setText("Timer: {}".format(datetime.fromtimestamp(self.second).strftime("%M:%S")))
        
    def _startTimer(self):
        self.timeStarted=True
        
    def _stopTimer(self):
        self.timeStarted=False
        
    def _resetTimer(self):
        self.timeStarted=False
        self.second=0
        self._timer.setText('Timer: 00.00')
        
    def _createErrCount(self):
        self.errCount=''
        self.errors=QLabel('Error Counts:')
        self.errors.setStyleSheet("font-size: 25px")
        self.errors.setFixedSize(200, 40)
        self.generalLayout.addWidget(self.errors, 12, 4)
        
    def _incrementErrCount(self):
        if self.started:
            self.errCount+='X'
            self.errors.setText('Error Counts: {}'.format(str(self.errCount)))
            
            if len(self.errCount)==3:
                self.errors.setStyleSheet('font-size: 25px; color: red')
                
                # Failed MSG
                self.failedMSG=QLabel('Too Many Errors! Try Again.')
                self.failedMSG.setStyleSheet('font-size: 25px; color: red')
                self.failedMSG.setFixedSize(400,40)
                self.generalLayout.addWidget(self.failedMSG, 13, 4)
                
                # Make Read Only
                for i in range(9):
                    for j in range(9):
                        self.allSpots[i][j].setReadOnly(False)
                        
                # Timer Stopped
                self.timeStarted=False
        
    def _resetErrCount(self):
        if len(self.errCount)>=3:  #remove failedMSG widget
            self.generalLayout.removeWidget(self.failedMSG)
            self.failedMSG.deleteLater()
            self.failedMSG = None
        self.errors.setText('Error Counts:')
        self.errors.setStyleSheet('font-size: 25px; color: black')
        self.errCount=''
                
    # Setup Empty Board
    def _createBoard(self):
        boardLayout = QGridLayout()
        self.allSpots=[]                  #nested list of spots QLineEdit
        for i in range(9):
            rowSpots=[]
            for j in range(9):
                self.spot=QLineEdit()
                self.spot.setReadOnly(True)                                       
                self.spot.setValidator(QIntValidator(1, 9, self))           #Only 1-9 allowed
                rowSpots.append(self.spot)
                self.spot.setAlignment(Qt.AlignCenter)
                self.spot.setFixedSize(100,100)
                if (i//3%2==1) & (j//3%2==0) | (i//3%2==0) & (j//3%2==1):   #different color for 3x3 squares
                    self.spot.setStyleSheet("font-size: 45px; padding-bottom:18px; background-color: #FCDFA6")
                else:
                    self.spot.setStyleSheet("font-size: 45px; padding-bottom:18px; background-color: white")
                boardLayout.addWidget(self.spot, i, j)
            self.allSpots.append(rowSpots)
        self.generalLayout.addLayout(boardLayout, 0,0, 9,9)
    
    def _setBoard(self, puzzle): 
        for i in range(9):
            for j in range(9):
                if puzzle[i][j]!=0:
                    self.allSpots[i][j].setText(str(puzzle[i][j]))
                else:
                    self.allSpots[i][j].setReadOnly(False)
    
    def _clearBoard(self):
        for i in range(9):
            for j in range(9):
                self.allSpots[i][j].clear()
                self.allSpots[i][j].setReadOnly(True)
        
    def _nextPuzzle(self):
        if not self._puzzleQueue.empty():
            self._puzzle=self._puzzleQueue.get()
        
    def displayNumber(self, index):
        i,j=index
        return self.allSpots[i][j].text()
    
    # Clear a particular spot on grid
    def clearSpot(self, index):
        i,j=index
        self.allSpots[i][j].clear()
    
    #change color of number, color is type str
    def changeNumColor(self, index, color):
        i,j=index
        if (i//3%2==1) & (j//3%2==0) | (i//3%2==0) & (j//3%2==1):
            self.allSpots[i][j].setStyleSheet("font-size: 45px; color: {}; padding-bottom:18px; background-color: #FCDFA6".format(color))
        else:
            self.allSpots[i][j].setStyleSheet("font-size: 45px; color: {}; ppadding-bottom:18px; background-color: white".format(color))
    


# Controller class to connect the view SudokuUI and the model solv_sudoku
class SudokuCtrl:
    def __init__(self, solver, view):
        self._view=view
        self._evaluate=solver
        self._puzzle=self._view._puzzle
        self._solution=self._evaluate(self._puzzle)
        
        # Start Button: show puzzle and start timer
        self._view.buttons[0].clicked.connect(self._start)
        self._view.buttons[0].clicked.connect(lambda : self._view._startTimer())
        
        # Text Change on Grid: display and check answers
        self._gridChange()
        
        # Show Solution button: show solution and stop timer
        self._view.buttons[1].clicked.connect(self._showSolution)
        self._view.buttons[1].clicked.connect(lambda : self._view._stopTimer())
        
        # Clear Button: clear grid and stop timer if applicable
        self._view.buttons[2].clicked.connect(self._clear)
    
    def _start(self):
        self._view._setBoard(self._puzzle)
        self._view.started=True
        #self._view.timeStarted=True
        self._cleared=False
        # start timer
        self.timer = QTimer(self._view) 
        self.timer.timeout.connect(self._view._showTime) 
        self.timer.start(1000)

    # Text Change on Grid:
    def _gridChange(self):
        for i in range(9):
            for j in range(9):
                self._view.allSpots[i][j].textChanged[str].connect(partial(self._checkAnswer, [i,j]))
    
    # Check if Right Answer
    def _checkAnswer(self, index):
        i,j = index
        if self._view.displayNumber(index) != str(self._solution[i][j]):
            self._view.changeNumColor(index,'red')
            if self._view.allSpots[i][j].text() != '':
                self._view._incrementErrCount()
        else:
            self._view.changeNumColor(index,'black')
            self._view.allSpots[i][j].setReadOnly(True)
            
    def _showSolution(self):
        # action only when board has started to avoid actions on consecutive clicks
        if self._view.started:        
            self._view._setBoard(self._solution)
            
            #update next puzzle
            self._view._nextPuzzle()
            self._puzzle=self._view._puzzle
            self._solution=self._evaluate(self._puzzle)
            
            #stop timer
            self._view.started=False
            self.timer.timeout.disconnect(self._view._showTime) 
    
    def _clear(self):
        self._cleared=True
        self._view._clearBoard()
        self._view._resetTimer()
        self._view._resetErrCount()
        
        #disconnect timer if show solution not clicked beforehand
        try:
            self.timer.timeout.disconnect(self._view._showTime) 
        except TypeError:
            pass
