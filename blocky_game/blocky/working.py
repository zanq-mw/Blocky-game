from typing import Tuple


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PACIFIC_POINT = (1, 128, 181)
OLD_OLIVE = (138, 151, 71)
REAL_RED = (199, 44, 58)
MELON_MAMBO = (234, 62, 112)
DAFFODIL_DELIGHT = (255, 211, 92)
TEMPTING_TURQUOISE = (75, 196, 213)

# A pallette of the colours we use in the game
COLOUR_LIST = [PACIFIC_POINT, REAL_RED, OLD_OLIVE, DAFFODIL_DELIGHT]


def _namestr(obj, namespace):
    """A private method for class <Goal> that returns a string representation of
    the variable names game's possible colours in a list.
    """
    return [name for name in namespace if namespace[name] is obj]


if __name__ == '__main__':
    lst = []
    for i in range(len(COLOUR_LIST)):
        lst.extend(_namestr(COLOUR_LIST[i], globals()))
    print(lst)
    #import python_ta
    #python_ta.check_all()

def _namestr(obj, namespace):
    """A private method for class <Goal> that returns a string representation of
    the variable names game's possible colours in a list.
    """
    return [name for name in namespace if namespace[name] is obj]

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

    def _colour(self) -> str:
        """A private method that returns a string representation of the colour
        of the class <goal>."""
        for colour in COLOUR_LIST:
            if colour == self.colour:
                return _namestr(colour, globals())[0]


class PerimeterGoal(Goal):

    def description(self) -> str:
        return f"PerimeterGoal: Surround the perimeter of the board with {self._colour()}."


class BlobGoal(Goal):
    def description(self) -> str:
        return f"BlobGoal: Make the biggest {self._colour()} blob."


if __name__ == '__main__':
    a = PerimeterGoal(PACIFIC_POINT)
    c = BlobGoal(PACIFIC_POINT)
    b = a._colour()
    a.description()
