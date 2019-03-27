import re

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Diagonal units are units on the two long diagonals of Sudoku
diagonal_units = [[row + col for row, col in zip(rows, cols)], [row + col for row, col in zip(rows, cols[::-1])]]

unitlist = row_units + column_units + square_units + diagonal_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find instances of naked twins and eliminate them in the same unit
    # A naked twin should have two properties: 
    # 1. It should have only two possible solutions
    # 2. It should have an identical twin
    for unit in unitlist:
        boxes_with_two_solns = {}
        for box in unit:
            value = values[box]
            if len(value) == 2: # Taking care of constraint 1 
                if value in boxes_with_two_solns:
                    # Found two such entries with same values, eliminate them (Constraint 2)
                    for peer in unit:
                        #Ignore the twin and self
                        if peer == boxes_with_two_solns[value] or peer == box: continue
                        else: 
                        # Eliminate each digit from rest of the peers of the unit
                            for digit in value: 
                                if digit in values[peer]:
                                    assign_value(values, peer, re.sub(digit, '', values[peer]))
                else:
                    boxes_with_two_solns[value] = box
    return values

  
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)

    return

def eliminate(values):
    for box in boxes:
        digit = values[box]
        if len(digit) == 1:
            for peer in peers[box]:
                assign_value(values, peer, re.sub(digit, '', values[peer]))
    return values  

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            digit_count = 0
            for box in unit:
                if digit in values[box]: 
                    digit_count = digit_count + 1
                    box_with_only_choice = box
            if digit_count == 1 : assign_value(values, box_with_only_choice, digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = naked_twins(values)
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False : return False
    
    if all(len(values[box]) == 1 for box in boxes): 
        return values 
        
    # Choose one of the unfilled squares with the fewest possibilities
    min_values, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[box]:
        sudoku_copy = values.copy()
        assign_value(sudoku_copy, box, value)
        soln = search(sudoku_copy)
        if soln : return soln

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    if values is False:
        print('Unable to find a solution!!')
    return values

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
