import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> MiniS | MiniS Conj MiniS 
MiniS -> NP VP | NP Adv VP | VP | NP
NP -> N | NADJ N
NADJ -> Det | Adj | NADJ NADJ
VP -> V | V VAD
VAD -> NP | P | Adv | VAD VAD | VAD VAD VAD
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
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
    tokenized_words = nltk.tokenize.word_tokenize(sentence)
    for i in range(len(tokenized_words)):
        tokenized_words[i] = tokenized_words[i].lower()
    words = []
    for word in tokenized_words:
        if any(charachter.isalpha() for charachter in word):
            words.append(word)
    return words



def np_chunk(tree: nltk.Tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    trees = []
    for tree in tree.subtrees():
        if tree.label() == "NP":
            if not any(subtree.label() == "NP" for subtree in tree.subtrees() if subtree != tree):
                trees.append(tree)
            else:
                continue
    return trees


if __name__ == "__main__":
    main()
