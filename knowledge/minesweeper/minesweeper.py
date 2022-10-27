from ast import Or
import itertools
import random


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

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return set(self.cells)
        else:
            return set()
        

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count-=1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)

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
        self.allCells = self.init_all_cells()

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
        #mark safe
        self.mark_safe (cell)

        self.update_knowledge_base (cell, count)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safeMovesAvail = self.safes.difference(self.moves_made)

        if len(safeMovesAvail) > 0:
            return safeMovesAvail.pop()
        else:
            return

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        availableCells = self.allCells
        availableCells.difference_update (self.moves_made)
        availableCells.difference_update (self.mines)
        indexToReturn = 0

        # TODO: would be nice - prefer empty cell surrounded by 1s than one surrounded by 3s
        return availableCells.pop()

    # new methods added by jason
    def update_knowledge_base (self, cell, count):
        """
            1) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            2) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            3) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        unknownCells = self.get_unknown_cells (cell, count)

        newSentence = Sentence (unknownCells, count)


        # iterate through knowledge - end to front append at end
        numSentences = len(self.knowledge)
        index = numSentences - 1
        while index >= 0:
            currSentence = self.knowledge[index]
            # check if num cells matches count - if so mark them all as mines
            numCells = len(currSentence.cells)
            if numCells == currSentence.count:
                j = 0
                while j < numCells:
                    self.mark_mine(currSentence.cells.pop())
                    j += 1
                currSentence.count = 0
            # check if count = 0, mark them all as safe
            elif currSentence.count == 0:
                l = 0
                numCells = len(currSentence.cells)
                while l < numCells:
                    self.mark_safe(currSentence.cells.pop())
                    l += 1
            # check if new sentence is subset of current sentence, if so add new sentence to knowledge base
            if len(currSentence.cells) != 0 and len(newSentence.cells) != 0:
                if newSentence.cells.issuperset(currSentence.cells):
                    difference = Sentence(newSentence.cells.difference(currSentence.cells), newSentence.count-currSentence.count)
                    self.knowledge.append(difference)
                elif currSentence.cells.issuperset(newSentence.cells):
                    difference = Sentence(currSentence.cells.difference(newSentence.cells), currSentence.count-newSentence.count)
                    self.knowledge.append(difference)

            index -= 1

        # lastly append new sentence
        if newSentence.count == 0:
            k=0
            numCells = len(newSentence.cells)
            while k < numCells:
                self.mark_safe(newSentence.cells.pop())
                k += 1
        if len(newSentence.cells) > 0:
            self.knowledge.append(newSentence)

    def get_unknown_cells (self, cell, count):
        unknownCells = self.get_surrounding_cells (cell, count)
        """
        1) omit safe cells - remove self.safes
        2) omit mines and deduct from count - remove self.mines
        """

        unknownCells.difference (self.safes)
        unknownCells.difference (self.mines)
        count = len(unknownCells)
        return unknownCells

    def get_surrounding_cells (self, cell, count):
        # get max. 8 surrounding cells minIndex = 0 
        # maxIndex = self.height and self.width
        # 
        # 
        #init count to zero
        count = 0
        surroundingCells = set()
        row = cell[0]
        col = cell[1]

        if row-1 < 0 :
            minRowIndex = 0
        else: 
            minRowIndex = row-1

        if col-1 < 0:
            minColIndex = 0
        else :
            minColIndex = col-1


        # in case game is not square use heigt for rows and width for cols
        if row+1 <= self.height-1:
            maxRowIndex = row+1
        else:
            maxRowIndex = self.height-1

        if col+1 <= self.width-1:
            maxColIndex = col+1
        else:
            maxColIndex = self.width-1

        i = minRowIndex
        while i <= maxRowIndex:
            j = minColIndex
            while j <= maxColIndex:
                if i != row or j != col:
                    surroundingCells.add ((i,j))
                j += 1
                count += 1
            i += 1

        return surroundingCells

    def init_all_cells (self):

        allCells = set()

        i = 0
        while i <= self.height-1:
            j = 0
            while j <= self.width-1:
                allCells.add ((i,j))
                j += 1
            i += 1

        return allCells
