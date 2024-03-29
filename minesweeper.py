import itertools
import random

class Minesweeper():
    def __init__(self, height=8, width=8, mines=8):
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

        self.mines_found = set()

    def print(self):
        """ Prints where mines are located. """
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
        
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                if (i, j) == cell:
                    continue
                    
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """ Checks if all mines have been flagged. """
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
        """ Returns the set of all cells in self.cells known to be mines. """
        if len(self.cells) == self.count:
            return self.cells

    def known_safes(self):
        """ Returns the set of all cells in self.cells known to be safe. """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
    
    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """ Minesweeper game player """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        
        self.mines = set()
        self.safes = set()
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
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)
        self.knowledge.append(Sentence(set([cell]), 0))
        self.add_neighbours(cell, count)
        self.make_inferences()


    def make_safe_move(self):
        """ Returns a safe cell to choose on the Minesweeper board. """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell 

    def make_random_move(self):
        """ Returns a move to make on the Minesweeper board. """
        for _ in range(self.width * self.height):
            row = random.randrange(self.height)
            column = random.randrange(self.width)

            if (row, column) not in self.mines | self.moves_made:
                return (row, column)
    
    def add_neighbours(self, cell, count):
        cells = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                c = (cell[0] + i, cell[1] + j)
                if c[0] < 0 or c[0] >= self.height or c[1] < 0 or c[1] >= self.width:
                    continue
                if c in self.mines:
                    count -= 1
                    continue
                if c in self.safes:
                    continue
                cells.add(c)

        if len(cells) != 0:
            self.knowledge.append(Sentence(cells, count))

    def make_inferences(self):
        breaker = True
        while True:
            breaker = True
            for s in self.knowledge:
                if s.known_safes():
                    breaker = False
                    for cell in s.cells.copy():
                        self.mark_safe(cell)
                if s.known_mines():
                    breaker = False
                    for cell in s.cells.copy():
                        self.mark_mine(cell)

            for sen1 in self.knowledge:
                if len(sen1.cells) == 0:
                    continue
                for sen2 in self.knowledge:
                    if sen1 == sen2 or len(sen2.cells) == 0:
                        continue
                    if sen2.cells.issubset(sen1.cells) and len(sen2.cells) != 0 and len(sen1.cells) != 0:
                        new_sentence = Sentence(sen2.cells - sen1.cells, abs(sen1.count - sen2.count))
                        if new_sentence not in self.knowledge:
                            self.knowledge.append(new_sentence)
                            breaker = False
            
            if breaker:
                break
        
