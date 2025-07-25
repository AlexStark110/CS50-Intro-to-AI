"""
Crossword Puzzle Generator

Generate crossword puzzles using constraint satisfaction algorithms
"""

import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment of variables.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k, (i, j) in enumerate(variable.cells):
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables:
            self.domains[var] = {
                word for word in self.domains[var] 
                if len(word) == var.length
            }

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False otherwise.
        """
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return False
        
        i, j = overlap
        revised = False
        
        # Check each word in x's domain
        words_to_remove = set()
        for word_x in self.domains[x]:
            # Check if there's any word in y's domain that satisfies the constraint
            has_consistent_word = False
            for word_y in self.domains[y]:
                if word_x[i] == word_y[j]:
                    has_consistent_word = True
                    break
            
            if not has_consistent_word:
                words_to_remove.add(word_x)
                revised = True
        
        self.domains[x] -= words_to_remove
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is provided, make each arc in `arcs` arc consistent.
        Otherwise, make all arcs in the CSP arc consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if an inconsistency is found.
        """
        if arcs is None:
            arcs = []
            for x in self.crossword.variables:
                for y in self.crossword.neighbors(x):
                    arcs.append((x, y))
        
        queue = arcs[:]
        
        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return set(assignment.keys()) == self.crossword.variables

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit their spots
        and do not conflict with each other); return False otherwise.
        """
        # Check that all values are distinct
        if len(set(assignment.values())) != len(assignment.values()):
            return False
        
        # Check that every word is the correct length
        for var, word in assignment.items():
            if len(word) != var.length:
                return False
        
        # Check that there are no conflicts between neighboring variables
        for var1, word1 in assignment.items():
            for var2, word2 in assignment.items():
                if var1 != var2:
                    overlap = self.crossword.overlaps[var1, var2]
                    if overlap:
                        i, j = overlap
                        if word1[i] != word2[j]:
                            return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value should be the one that rules out the fewest
        values among the neighbors of `var`.
        """
        def count_conflicts(value):
            """Count how many values this choice eliminates from neighbors."""
            conflicts = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        for neighbor_value in self.domains[neighbor]:
                            if value[i] != neighbor_value[j]:
                                conflicts += 1
            return conflicts
        
        return sorted(self.domains[var], key=count_conflicts)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not in `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [var for var in self.crossword.variables if var not in assignment]
        
        if not unassigned:
            return None
        
        # Sort by domain size (ascending), then by degree (descending)
        return min(unassigned, key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            
            if self.consistent(new_assignment):
                # Save current domains
                saved_domains = {v: domain.copy() for v, domain in self.domains.items()}
                
                # Make arc consistent
                arcs = [(neighbor, var) for neighbor in self.crossword.neighbors(var)]
                if self.ac3(arcs):
                    result = self.backtrack(new_assignment)
                    if result is not None:
                        return result
                
                # Restore domains
                self.domains = saved_domains
        
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()