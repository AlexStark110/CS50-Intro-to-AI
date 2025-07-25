"""
Knights and Knaves Puzzle Solver

Solve logic puzzles involving knights (who always tell the truth) 
and knaves (who always lie)
"""

from logic import *

# Create symbols for characters
AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # Structure of the knowledge base:
    # - For each character, exactly one of knight or knave
    # - Character statements are true if and only if they are knights
    
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # A's statement: "I am both a knight and a knave"
    # This statement is true if A is a knight, false if A is a knave
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # A's statement: "We are both knaves"
    # This statement is true if A is a knight, false if A is a knave
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # A's statement: "We are the same kind"
    # This means both are knights or both are knaves
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    
    # B's statement: "We are of different kinds"
    # This means one is knight and one is knave
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight)))
)

# Puzzle 3
# A says either "I am a knight" or "I am a knave", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # A is either a knight or a knave, but not both
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    
    # B is either a knight or a knave, but not both
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    
    # C is either a knight or a knave, but not both
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    
    # A says either "I am a knight" or "I am a knave"
    # If A is a knight, A would say "I am a knight" (true statement)
    # If A is a knave, A would say "I am a knight" (false statement)
    # A knave cannot say "I am a knave" (would be true)
    # So A must have said "I am a knight"
    
    # B says "A said 'I am a knave'" - this is B claiming A said something A couldn't say
    # This statement by B is false, so B must be a knave
    Not(BKnight),
    
    # B says "C is a knave"
    # Since B is a knave, this statement is false, so C is a knight
    Biconditional(BKnight, CKnave),
    
    # C says "A is a knight"
    # Since C is a knight, this statement is true
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()