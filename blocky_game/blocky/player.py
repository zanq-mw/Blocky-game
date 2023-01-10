"""CSC148 Assignment 2

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, David Liu, Mario Badr, Sophia Huynh, Misha Schwartz,
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) Diane Horton, David Liu, Mario Badr, Sophia Huynh,
Misha Schwartz, and Jaisie Sin.

=== Module Description ===

This file contains the hierarchy of player classes.
"""
from __future__ import annotations
from typing import List, Optional, Tuple
import random
import pygame

from block import Block
from goal import Goal, generate_goals

from actions import KEY_ACTION, ROTATE_CLOCKWISE, ROTATE_COUNTER_CLOCKWISE, \
    SWAP_HORIZONTAL, SWAP_VERTICAL, SMASH, PASS, PAINT, COMBINE


def create_players(num_human: int, num_random: int, smart_players: List[int]) \
        -> List[Player]:
    """Return a new list of Player objects.

    <num_human> is the number of human players, <num_random> is the number of
    random players, and <smart_players> is a list of difficulty levels for each
    SmartPlayer that is to be created.

    The list should contain <num_human> HumanPlayer objects first, then
    <num_random> RandomPlayer objects, then the same number of SmartPlayer
    objects as the length of <smart_players>. The difficulty levels in
    <smart_players> should be applied to each SmartPlayer object, in order.
    """

    goals = generate_goals(num_human + num_random + len(smart_players))
    players = []

    for i in range(num_human):
        players.append(HumanPlayer(i, goals[i]))

    for i in range(num_human, num_human + num_random):
        players.append(RandomPlayer(i, goals[i]))

    for i in range(num_human + num_random,
                   num_human + num_random + len(smart_players)):
        players.append(SmartPlayer(i, goals[i],
                                   smart_players[i - num_human - num_random]))

    return players


def _get_block(block: Block, location: Tuple[int, int], level: int) -> \
        Optional[Block]:
    """Return the Block within <block> that is at <level> and includes
    <location>. <location> is a coordinate-pair (x, y).

    A block includes all locations that are strictly inside of it, as well as
    locations on the top and left edges. A block does not include locations that
    are on the bottom or right edge.

    If a Block includes <location>, then so do its ancestors. <level> specifies
    which of these blocks to return. If <level> is greater than the level of
    the deepest block that includes <location>, then return that deepest block.

    If no Block can be found at <location>, return None.

    Preconditions:
        - 0 <= level <= max_depth
    """
    # Base case: If the Block <block> is found at <location> return None
    if location[0] >= block.size + block.position[0] or\
       location[1] >= block.size + block.position[1] or\
       location[0] < block.position[0] or\
       location[1] < block.position[1]:
        return None

    elif not block.children or level == block.level:
        return block

    else:
        for child in block.children:
            x = _get_block(child, location, level)
            if x is not None:
                return x

    return None


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    id:
        This player's number.
    goal:
        This player's assigned goal for the game.
    """
    id: int
    goal: Goal

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.id = player_id

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.

        If no block is selected by the player, return None.
        """
        raise NotImplementedError

    def process_event(self, event: pygame.event.Event) -> None:
        """Update this player based on the pygame event.
        """
        raise NotImplementedError

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a potential move to make on the game board.

        The move is a tuple consisting of a string, an optional integer, and
        a block. The string indicates the move being made (i.e., rotate, swap,
        or smash). The integer indicates the direction (i.e., for rotate and
        swap). And the block indicates which block is being acted on.

        Return None if no move can be made, yet.
        """
        raise NotImplementedError


def _create_move(action: Tuple[str, Optional[int]], block: Block) -> \
        Tuple[str, Optional[int], Block]:
    """Return a tuple representation of the <action> and block.
    Where:
            (action[0], action[1], block)
    action[0]: The type of move being performed
    action[1]: Direction indicator. Else, None.
    block: The block the <action> is applied to.
    """
    return action[0], action[1], block


class HumanPlayer(Player):
    """A human player.
    """
    # === Private Attributes ===
    # _level:
    #     The level of the Block that the user selected most recently.
    # _desired_action:
    #     The most recent action that the user is attempting to do.
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _level: int
    _desired_action: Optional[Tuple[str, Optional[int]]]

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        Player.__init__(self, player_id, goal)

        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._desired_action = None

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player based on
        the position of the mouse on the screen and the player's desired level.

        If no block is selected by the player, return None.
        """
        mouse_pos = pygame.mouse.get_pos()
        block = _get_block(board, mouse_pos, self._level)

        return block

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the relevant keyboard events made by the player based on
        the mapping in KEY_ACTION, as well as the W and S keys for changing
        the level.
        """
        if event.type == pygame.KEYDOWN:
            if event.key in KEY_ACTION:
                self._desired_action = KEY_ACTION[event.key]
            elif event.key == pygame.K_w:
                self._level = max(0, self._level - 1)
                self._desired_action = None
            elif event.key == pygame.K_s:
                self._level += 1
                self._desired_action = None

    def generate_move(self, board: Block) -> \
            Optional[Tuple[str, Optional[int], Block]]:
        """Return the move that the player would like to perform. The move may
        not be valid.

        Return None if the player is not currently selecting a block.
        """
        block = self.get_selected_block(board)

        if block is None or self._desired_action is None:
            return None
        else:
            move = _create_move(self._desired_action, block)
            self._desired_action = None
            return move


def _valid_move(player: Player, board: Block, copy: Block) -> \
        Optional[Tuple[str, Optional[int], Block]]:
    """Return a valid move <move>, and update the input <executable> to True
        Precondition: <board_copy> is a copy of <board>.
    """
    executable = False
    while not executable:
        move1 = random.choice(list(KEY_ACTION.keys())[:-1])
        move = KEY_ACTION[move1]

        location = (random.randint(copy.position[0],
                                   copy.position[0] + copy.size - 1),
                    random.randint(copy.position[0],
                                   copy.position[0] + copy.size - 1))

        level = random.randint(copy.level, copy.max_depth)
        block = _get_block(copy, location, level)
        original_board_block = _get_block(board, location, level)

        if move == COMBINE:
            if block.combine():
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == SMASH:
            if block.smash():
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == ROTATE_CLOCKWISE:
            if block.rotate(1):
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == ROTATE_COUNTER_CLOCKWISE:
            if block.rotate(3):
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == SWAP_HORIZONTAL:
            if block.swap(0):
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == SWAP_VERTICAL:
            if block.swap(1):
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move

        if move == PAINT:
            if block.paint(player.goal.colour):
                executable = True
                executed_move = _create_move(move, original_board_block)
                return executed_move


class RandomPlayer(Player):
    """A RandomPlayer AI."""
    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool

    def __init__(self, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
        and <goal>."""
        Player.__init__(self, player_id, goal)
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.
        For RandomPlayer, this should always return None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the left click made by the user to initiate RandomPlayer's
        move.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid, randomly generated move.

        A valid move is a move other than PASS that can be successfully
        performed on the <board>.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None

        copy = board.create_copy()
        self._proceed = False
        return _valid_move(self, board, copy)


class SmartPlayer(Player):
    """A SmartPlayer AI.
    """
    # === Public Attributes ===
    # difficulty:
    #   The level of difficulty of the SmartPlayer AI.

    # === Private Attributes ===
    # _proceed:
    #   True when the player should make a move, False when the player should
    #   wait.
    _proceed: bool
    difficulty: int

    def __init__(self, player_id: int, goal: Goal, difficulty: int) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>,
        <goal>, and <difficulty>."""
        Player.__init__(self, player_id, goal)
        self.difficulty = difficulty
        self._proceed = False

    def get_selected_block(self, board: Block) -> Optional[Block]:
        """Return the block that is currently selected by the player.
        For SmartPlayer, this should always return None.
        """
        return None

    def process_event(self, event: pygame.event.Event) -> None:
        """Respond to the left click made by the user to initiate SmartPlayer's
        move.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._proceed = True

    def generate_move(self, board: Block) ->\
            Optional[Tuple[str, Optional[int], Block]]:
        """Return a valid move by assessing multiple valid moves and choosing
        the move that results in the highest score for this player's goal (i.e.,
        disregarding penalties).

        A valid move is a move other than PASS that can be successfully
        performed on the <board>. If no move can be found that is better than
        the current score, this player will pass.

        This function does not mutate <board>.
        """
        if not self._proceed:
            return None  # Do not remove

        original_score = self.goal.score(board)
        optimal_score = 0
        optimal_move = None
        for _ in range(self.difficulty):
            copy = board.create_copy()
            x = _valid_move(self, board, copy)
            score = self.goal.score(copy)
            if score > optimal_score:
                optimal_score = score
                optimal_move = x

        self._proceed = False  # Must set to False before returning!
        if original_score >= optimal_score:
            return _create_move(PASS, board)
        return optimal_move


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing', 'actions', 'block',
            'goal', 'pygame', '__future__'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
