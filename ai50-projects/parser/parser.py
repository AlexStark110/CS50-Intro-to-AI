"""
Natural Language Parser

Parse sentences and extract noun phrases using natural language processing
and context-free grammars
"""

import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "man" | "morning" | "mother" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det Adj N | NP PP | Adj NP
VP -> V | V NP | V NP PP | V PP | Adv VP | VP Adv
PP -> P NP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            s = f.read()
    
    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize the sentence
    words = nltk.word_tokenize(sentence.lower())
    
    # Filter out words that don't contain at least one alphabetic character
    words = [word for word in words if any(c.isalpha() for c in word)]
    
    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrases = []
    
    def extract_np(subtree):
        """Recursively extract noun phrases from a tree."""
        if subtree.label() == "NP":
            # Check if this NP contains any other NPs
            contains_np = False
            for child in subtree:
                if hasattr(child, 'label') and child.label() == "NP":
                    contains_np = True
                    break
            
            # If this NP doesn't contain other NPs, it's a chunk
            if not contains_np:
                noun_phrases.append(subtree)
            else:
                # If it does contain NPs, recursively process children
                for child in subtree:
                    if hasattr(child, 'label'):
                        extract_np(child)
        else:
            # For non-NP nodes, recursively check children
            for child in subtree:
                if hasattr(child, 'label'):
                    extract_np(child)
    
    extract_np(tree)
    return noun_phrases


if __name__ == "__main__":
    main()