"""Fixture testing for Assignment 2"""


from typing import List, Optional, Tuple
import os
import pygame
import pytest

from block import Block
from blocky import _block_to_squares
from goal import BlobGoal, PerimeterGoal, _flatten
from player import _get_block
from renderer import Renderer
from settings import COLOUR_LIST

"""File: block.py"""

@pytest.fixture
def board_4x4() -> Block:
    big_block = Block((0, 0), 750, None, 0, 2)

    tr_child = Block((0, 375), 375, COLOUR_LIST[0], 1, 2)
    tl_child = Block((0, 0), 375, None, 1, 2)
    bl_child = Block((0, 375), 375, COLOUR_LIST[0], 1, 2)
    br_child = Block((375, 375), 375, COLOUR_LIST[2], 1, 2)

    tl_tr_child = Block((187, 0), 187, COLOUR_LIST[0], 2, 2)
    tl_tl_child = Block((0, 0), 187, COLOUR_LIST[3], 2, 2)
    tl_bl_child = Block((0, 187), 187, COLOUR_LIST[1], 2, 2)
    tl_br_child = Block((187, 187), 187, COLOUR_LIST[2], 2, 2)

    tl_child.children.extend([tl_tr_child, tl_tl_child, tl_bl_child, tl_br_child])
    big_block.children.extend([tr_child, tl_child, bl_child, br_child])

    return big_block

@pytest.fixture
def out_of_range() -> List[Tuple[int, int]]:
    return [(751, 0), (0, 751), (-1, 0), (0, -1)]

@pytest.fixture
def colourless_sample_block() -> Block:
    """A block with no colour, and children."""
    # Initalize the colourless block.
    sample_block = Block((0, 0), 1, 2, 3)

    # Make 4 other blocks with colour at max depth reached.
    child_1 = Block((0, 0), 1, 3, 3)
    child_2 = Block((0, 0), 1, 3, 3)
    child_3 = Block((0, 0), 1, 3, 3)
    child_4 = Block((0, 0), 1, 3, 3)

    # Append each child to the list of children for sample_block.
    sample_block.children.append(child_1)
    sample_block.children.append(child_2)
    sample_block.children.append(child_3)
    sample_block.children.append(child_4)

    # Return the block
    return sample_block

@pytest.fixture
def sample_block() -> Block:
    """A block with colour and no children."""
    sample_block = Block((0, 0), 1, COLOUR_LIST[0], 2, 3)
    return sample_block

class TestBlock:
    """ Tests for all of <class Block> in block.py."""

    def test_1_smash(self) -> None:
        """Smash a smashable block."""
        pass

    def test_2_smash(self) -> None:
        """Smash a non-smashable block."""
        pass

    def test_3_smash(self) -> None:
        """Smash a non-smashable block."""
        pass

    def test_4_smash(self) -> None:
        """Smash a non-smashable block."""
        pass


    def test_1_create_copy(self) -> None:
        """Create a deep copy of a colourless block with 4 children."""
        pass

    def test_2_create_copy(self) -> None:
        """Create a deep copy of a coloured block with no children."""
        pass


    def test_1_swap(self) -> None:
        """Swap a block horizontally when it has no children."""
        pass

    def test_2_swap(self) -> None:
        """Swap a block horizontally when it has 4 children."""
        pass

    def test_3_swap(self) -> None:
        """Swap a block vertically when it has 4 children."""
        pass

    def test_4_swap(self) -> None:
        """Swap a block vertically when it doesn't have 0 or 4 children."""
        pass


    def test_1_paint(self) -> None:
        """Attempt to paint a block with an undefined colour in COLOUR_LIST."""
        pass

    def test_2_paint(self) -> None:
        """Attempt to paint a block with an defined colour in COLOUR_LIST, has:
           self.level == self.max_depth and
           self.colour != colour
        """
        pass

    def test_3_paint(self) -> None:
        """Attempt to paint a block with an defined colour in COLOUR_LIST, has:
           self.level == self.max_depth and
           self.colour == colour
        """
        pass

    def test_4_paint(self) -> None:
        """Attempt to paint a block with an defined colour in COLOUR_LIST, has:
           self.level != self.max_depth and
           self.colour != colour
        """
        pass


    def test_1_update_children_positions(self, board_4x4, out_of_range) -> None:
        """Check location inputs that are out of the dimensions of board_4x4's
        biggest block.

            Precondition: out_of_range only has location inputs (x, y) that are
                          out of range.
        """
        for location in out_of_range:
            board_4x4._update_children_positions(location)
        top_right_child_children_position = board_4x4.children[0]._children_positions()
        top_left_child_children_position = board_4x4.children[0]._children_positions()
        bottom_child_children_position = board_4x4.children[0]._children_positions()
        top_right_child_children_position = board_4x4.children[0]._children_positions()
        child_positions = board_4x4._children_positions()
        more_child_positions = []
        for child in board_4x4.children:
            [child._children_positions()]

        i = 0
        for child in board_4x4.children:
            for child2 in board_4x4.children:
                assert child2.position == child_positions[i]
            i += 1

    def test_2_update_children_positions(self, board_4x4, out_of_range) -> None:
        """Check location inputs that are out of the dimensions of board_4x4's
        max_depth block.

            Precondition: out_of_range only has location inputs (x, y) that are
                          out of range.
        """
        for location in out_of_range:
            for child in board_4x4.children:
                assert board_4x4._update_children_positions(location) == None

    def test_3_update_children_positions(self, board_4x4) -> None:
        """Check location inputs that are in the dimensions of board_4x4's
        block's at block.level = 1
        """
        top_right = (375, 0)
        top_left =  (0, 0)
        bottom_left = (0, 375)
        bottom_right = (375, 375)
        in_range = [top_right, top_left, bottom_left, bottom_right]
        for position in in_range:
            board_4x4._update_children_positions(position)
        

if __name__ == '__main__':
    pytest.main(['personal_tests.py'])
