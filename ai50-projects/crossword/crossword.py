"""
Crossword Puzzle Generator

Generate crossword puzzles using constraint satisfaction algorithms
"""

from itertools import product


class Variable():
    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with given starting point, direction and length."""
        self.i = i
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []
        for k in range(self.length):
            if self.direction == Variable.ACROSS:
                self.cells.append((self.i, self.j + k))
            else:
                self.cells.append((self.i + k, self.j))

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            self.i == other.i and
            self.j == other.j and
            self.direction == other.direction and
            self.length == other.length
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():

    def __init__(self, structure):
        self.height = len(structure)
        self.width = max(len(row) for row in structure) if self.height else 0
        self.structure = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if j >= len(structure[i]):
                    row.append(False)
                else:
                    row.append(structure[i][j])
            self.structure.append(row)

        # Find all variables (words)
        self.variables = set()
        
        # Find horizontal variables
        for i in range(self.height):
            j = 0
            while j < self.width:
                if self.structure[i][j]:
                    start_j = j
                    while j < self.width and self.structure[i][j]:
                        j += 1
                    if j - start_j > 1:  # At least 2 characters
                        self.variables.add(Variable(i, start_j, Variable.ACROSS, j - start_j))
                else:
                    j += 1
        
        # Find vertical variables
        for j in range(self.width):
            i = 0
            while i < self.height:
                if self.structure[i][j]:
                    start_i = i
                    while i < self.height and self.structure[i][j]:
                        i += 1
                    if i - start_i > 1:  # At least 2 characters
                        self.variables.add(Variable(start_i, j, Variable.DOWN, i - start_i))
                else:
                    i += 1

        # Find overlaps between variables
        self.overlaps = {}
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    self.overlaps[v1, v2] = None
                else:
                    overlap = None
                    for i, cell1 in enumerate(v1.cells):
                        for j, cell2 in enumerate(v2.cells):
                            if cell1 == cell2:
                                overlap = (i, j)
                                break
                        if overlap:
                            break
                    self.overlaps[v1, v2] = overlap

    def neighbors(self, var):
        """Return all variables that overlap with var."""
        neighbors = set()
        for v in self.variables:
            if v != var and self.overlaps[var, v]:
                neighbors.add(v)
        return neighbors