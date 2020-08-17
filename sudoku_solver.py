# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 18:27:51 2020

@author: Ariel
"""
import math
import time

#main func
def solv_sudoku(puzzle):
    #create list of emptys
    result=[ele[:] for ele in puzzle] #create copy of puzzle
    empty=[]
    for i in range(9):
        for j in range(9):
            if result[i][j]==0:
                empty.append([i,j])
    if empty==[]:
        print('Already finished')
    else:
        if backtrack(result,empty,0):   #start to recur from first empty
            return result
        else:
            print('Solution not found!')

#check the validity of the value in the index position
def checker(v,puzzle,index): 
    i,j=index
    if v in puzzle[i]:   #check row
        return False
    else:
        for r in range(9):   #check column
            if v == puzzle[r][j]:
                return False
        #check squares
        square_r=list(map(lambda x: x+3*math.floor(i/3), [0,1,2]))
        square_c=list(map(lambda x: x+3*math.floor(j/3), [0,1,2]))
        for sr in square_r:
            for sc in square_c:
                if v==puzzle[sr][sc]:
                    return False
        return True

#recursive backtracking, return boolean
def backtrack(puzzle,empty,empty_i): 
    if empty_i>=len(empty):             #finished all emptys
        return True
    else:
        i,j=empty[empty_i]
        #check for valid values, assign, recur to see if works for remaining emptys, otherwise value would be overriden
        for value in range(0,10):       
            if checker(value,puzzle,empty[empty_i]):          
                puzzle[i][j]=value 
                if backtrack(puzzle,empty,empty_i+1)==True:    #recur to see if works for remaining emptys
                    return True
                else:
                    puzzle[i][j]=0
    return False


if __name__=="__main__":
    sudoku1=[[1,0,6, 0,0,2, 3,0,0],
            [0,5,0, 0,0,6, 0,9,1],
            [0,0,9, 5,0,1, 4,6,2],
            
            [0,3,7, 9,0,5, 0,0,0],
            [5,8,1, 0,2,7, 9,0,0],
            [0,0,0, 4,0,8, 1,5,7],
            
            [0,0,0, 2,6,0, 5,4,0],
            [0,0,4, 1,5,0, 6,0,9],
            [9,0,0, 8,7,4, 2,1,0]]
    sudoku2=[[0,0,0, 0,0,0, 2,0,0],
            [0,8,0, 0,0,7, 0,9,0],
            [6,0,2, 0,0,0, 5,0,0],
            
            [0,7,0, 0,6,0, 0,0,0],
            [0,0,0, 9,0,1, 0,0,0],
            [0,0,0, 0,2,0, 0,4,0],
            
            [0,0,5, 0,0,0, 6,0,3],
            [0,9,0, 4,0,0, 0,7,0],
            [0,0,6, 0,0,0, 0,0,0]]
    
    sudoku3=[[0, 0, 4, 3, 0, 0, 2, 0, 9],
             [0, 0, 5, 0, 0, 9, 0, 0, 1],
             [0, 7, 0, 0, 6, 0, 0, 4, 3],
             [0, 0, 6, 0, 0, 2, 0, 8, 7],
             [1, 9, 0, 0, 0, 7, 4, 0, 0],
             [0, 5, 0, 0, 8, 3, 0, 0, 0],
             [6, 0, 0, 0, 0, 0, 1, 0, 5],
             [0, 0, 3, 5, 0, 8, 6, 9, 0],
             [0, 4, 2, 9, 1, 0, 3, 0, 0]]
    start=time.time()
    print('\ns:',solv_sudoku(sudoku3), '\n')
    end=time.time()
    print(end-start)