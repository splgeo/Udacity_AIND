from utils import *

def cross(a, b):
    return [s+t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'
cols_rev = cols[::-1]
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
columns = [cross(rows, c) for c in cols]
squares = [cross(rs, cs) for rs in ('ABC','DEF','GHI') 
            for cs in ('123','456','789')]
diagonals = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'],
        ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + columns + squares + diagonals
units = dict((box, [u for u in unitlist if box in u]) 
            for box in boxes)
peers = dict((box, set(sum(units[box],[]))-set([box]))    
            for box in boxes)

def naked_twins(values):
    pairs = [box for box in values.keys() if len(values[box]) == 2]
    twins = [[box0,box1] for box0 in pairs for box1 in peers[box0]
             if values[box0] == values[box1]]
    for box0, box1 in twins:
        digit0 = peers[box0]
        digit1 = peers[box1]
        for peer in digit0 & digit1:
                for digit in values[box1]:
                    values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
  
def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for solved_val in solved_values:
        digit = values[solved_val]
        peers_solv = peers[solved_val]
        for peer in peers_solv:
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
# TODO: Copy your code from the classroom to complete this function

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
# TODO: Copy your code from the classroom to complete this function
  
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
# TODO: Copy your code from the classroom and modify it to complete this function
  
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values 

    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) == 0)
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

# TODO: Copy your code from the classroom to complete this function         
          
def solve(grid):
    values = grid2values(grid)
    values = search(values)
    return values

if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)
    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')