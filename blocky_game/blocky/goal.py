"""
This file contains the hierarchy of Goal classes.
"""
from __future__ import annotations
import random
from typing import List, Tuple
from block import Block
from settings import colour_name, COLOUR_LIST


def generate_goals(num_goals: int) -> List[Goal]:
    """Return a randomly generated list of goals with length num_goals.

    All elements of the list must be the same type of goal, but each goal
    must have a different randomly generated colour from COLOUR_LIST. No two
    goals can have the same colour.

    Precondition:
        - num_goals <= len(COLOUR_LIST)
    """
    cl_copy = COLOUR_LIST.copy()
    lst = []
    a = bool(random.getrandbits(1))
    for _ in range(num_goals):
        if a is True:
            random_index = random.randint(0, len(cl_copy) - 1)
            lst.append(PerimeterGoal(cl_copy[random_index]))
            cl_copy.pop(random_index)
        else:
            random_index = random.randint(0, len(cl_copy) - 1)
            lst.append(BlobGoal(cl_copy[random_index]))
            cl_copy.pop(random_index)
    return lst


def _flatten(block: Block) -> List[List[Tuple[int, int, int]]]:
    """Return a two-dimensional list representing <block> as rows and columns of
    unit cells.

    Return a list of lists L, where,
    for 0 <= i, j < 2^{max_depth - self.level}
        - L[i] represents column i and
        - L[i][j] represents the unit cell at column i and row j.

    Each unit cell is represented by a tuple of 3 ints, which is the colour
    of the block at the cell location[i][j]

    L[0][0] represents the unit cell in the upper left corner of the Block.
    """
    if not block.children:
        return (2 ** (block.max_depth - block.level)) *\
               [(2 ** (block.max_depth - block.level) * [block.colour])]

    board_colour = []
    total_columns = 2 ** (block.max_depth - block.level)

    for _ in range(total_columns):
        board_colour.append([])
    middle = len(board_colour) // 2

    for child in block.children:
        if child == block.children[0]:
            # Work with board_colour[middle:] and each board from board[:middle]
            flattened_child = _flatten(child)
            for i in range(middle):
                # Figuring our which lists
                board_colour[middle + i].extend(flattened_child[i])

        if child == block.children[1]:
            # Work with board_colour[:middle] and each board from board[:middle]
            flattened_child = _flatten(child)
            for i in range(middle):
                # Figuring our which lists
                board_colour[i].extend(flattened_child[i])

        if child == block.children[2]:
            # Work with board_colour[:middle] and each board from board[middle:]
            flattened_child = _flatten(child)
            for i in range(middle):
                # Figuring our which lists
                board_colour[i].extend(flattened_child[i])

        if child == block.children[3]:
            # Work with board_colour[:middle] and each board from board[middle:]
            flattened_child = _flatten(child)
            for i in range(middle):
                # Figuring our which lists
                board_colour[middle + i].extend(flattened_child[i])
    return board_colour


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class PerimeterGoal(Goal):
    """A type of goal for a player in the game Blocky.
    The player must aim to put the most possible units of a given colour c on
    the outer perimeter of the board.
    """

    def score(self, board: Block) -> int:
        """Return the total amount of unit cells coloured <self.colour> in
        <board> that are along the perimeter of the <board>.

        Note: <self.colour> unit cells positioned along the corners account
              for two points.
        """
        # Store a 2-D representation of the input <board>.
        flattened_board = _flatten(board)
        # First column (all values are considered in PerimeterGoal's score)
        first_column = flattened_board[0]
        score_ = 0
        for i in range(len(first_column)):
            if first_column[i] == self.colour:
                if i in (0, len(first_column) - 1):
                    score_ += 2
                else:
                    score_ += 1
        # Last column (all values are considered in PerimeterGoal's score)
        last_column = flattened_board[-1]
        for i in range(len(last_column)):
            if last_column[i] == self.colour:
                if i in (0, len(last_column) - 1):
                    score_ += 2
                else:
                    score_ += 1
        # Middle columns (First and last entires of columns are considered)
        middle = flattened_board[1: -1]
        for column in middle:
            if self.colour == column[0]:
                score_ += 1
            if self.colour == column[-1]:
                score_ += 1
        return score_

    def description(self) -> str:
        """Return a string representation of the goal <PerimeterGoal>.
        """
        colour = colour_name(self.colour)
        return 'PerimeterGoal: Surround the perimeter of the' +\
            f' board with {colour}.'


class BlobGoal(Goal):
    """A type of goal for the game blocky. The player must aim to get the
    biggest block of a colour c.
    """

    def score(self, board: Block) -> int:
        """Return the total amount of unit cells coloured <self.colour> that
        are in a blob. A blob is a group of connected blocks with the same
        colour. Two blocks are connected if their sides touch; touching corners
        doesn’t count.
        """
        flattened_board = _flatten(board)
        length = len(flattened_board)
        scores = []
        visited = []
        for _ in range(length):
            visited.append([])

        for i in range(length):
            for _ in range(length):
                visited[i].append(-1)

        for i in range(length):
            for j in range(length):
                if visited[i][j] == -1:
                    scores.append(self._undiscovered_blob_size((i, j),
                                                               flattened_board,
                                                               visited))
        return max(scores)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that:
        (a) is of this Goal's target colour,
        (b) includes the cell at <pos>, and
        (c) involves only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
            -1 if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        if pos[0] < 0 or pos[1] < 0 or\
           pos[0] >= len(board) or pos[1] >= len(board):
            return 0
        if visited[pos[0]][pos[1]] == 0:
            return 0
        if visited[pos[0]][pos[1]] == 1:
            return 0
        if visited[pos[0]][pos[1]] == -1 and\
           board[pos[0]][pos[1]] != self.colour:
            visited[pos[0]][pos[1]] = 0
            return 0
        if visited[pos[0]][pos[1]] == -1 and\
           board[pos[0]][pos[1]] == self.colour:
            visited[pos[0]][pos[1]] = 1
            size = 1

            adjacent_cells = []
            if pos[0] > 0 and visited[pos[0] - 1][pos[1]] == -1:
                adjacent_cells.append((pos[0] - 1, pos[1]))
            if pos[1] > 0 and visited[pos[0]][pos[1] - 1] == -1:
                adjacent_cells.append((pos[0], pos[1] - 1))
            if pos[1] + 1 < len(board) and visited[pos[0]][pos[1] + 1] == -1:
                adjacent_cells.append((pos[0], pos[1] + 1))
            if pos[0] + 1 < len(board) and visited[pos[0] + 1][pos[1]] == -1:
                adjacent_cells.append((pos[0] + 1, pos[1]))

            for cell in adjacent_cells:
                size += self._undiscovered_blob_size(cell, board, visited)

            return size

        return 0

    def description(self) -> str:
        """Return a string representation of the goal <BlobGoal>.
        """
        colour = colour_name(self.colour)
        return f'BlobGoal: Make the biggest {colour} blob.'


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'block', 'settings',
            'math', '__future__'
        ],
        'max-attributes': 15
    })
