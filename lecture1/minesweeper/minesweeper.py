import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        print(f"cells: {self.cells}")

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if the number of cells in the sentence is equal to the count of the sentence,
        # then all cells are mines
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if the count is 0, then all cells are safe
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        
        """
        The mark_mine function should first check to see if cell is one of the cells included in the sentence.
        If cell is in the sentence, the function should update the sentence so that cell is no longer in the sentence, but still represents a logically correct sentence given that cell is known to be a mine.
        If cell is not in the sentence, then no action is necessary.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        # add a new sentence to the AI's knowledge base based on the value of cell and count
        cells = set()
        neighbors = self.get_neighbors(cell)
        count_copy = copy.deepcopy(count)
        for cl in neighbors:
            if cl in self.mines:
                count_copy -= 1
            elif cl in self.safes:
                continue
            else:
                cells.add(cl)
        new_ai_sentence = Sentence(cells, count_copy)
        if (len(new_ai_sentence.cells) > 0):
            self.knowledge.append(new_ai_sentence)
        
        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        self.check_knowledge()
        
        
        self.update_knowledge()
        return
        
    def check_knowledge(self):
        for sentence in self.knowledge:
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
            known_mines_place = copy.deepcopy(sentence.known_mines())
            known_safes_place = copy.deepcopy(sentence.known_safes())
            if known_mines_place:
                for mine in known_mines_place:
                    self.mark_mine(mine)
                    self.check_knowledge()
            if known_safes_place:
                for safe in known_safes_place:
                    self.mark_safe(safe)
                    self.check_knowledge()
    def update_knowledge(self):
        """
        Update the AI's knowledge base based on the new information given.
        """
        new_knowledge = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2:
                    if sentence1.cells.issubset(sentence2.cells):
                        # if sentence1 is a subset of sentence2, then we can create a new sentence
                        # with the remaining cells and the difference in counts
                        # any time we have two sentences set1 = count1 and set2 = count2
                        # where set1 is a subset of set2, then we can construct
                        # the new sentence set2 - set1 = count2 - count1.
                        new_knowledge.append(Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count))
        self.knowledge += new_knowledge
        return
        
    def get_neighbors(self, cell):
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))
        return neighbors
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.safes) == 0:
            return None
        print("finding safe moves to make")
        print(self.knowledge)
        for cell in self.safes:
            print(".")
            if cell not in self.moves_made:
                return cell
        return


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("Random move function called.")
        if len(self.moves_made) == self.height * self.width:
            return None
        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            move = (i, j)
            if move not in self.moves_made and move not in self.mines:
                print(f"Random move: {move}")
                return move
        
