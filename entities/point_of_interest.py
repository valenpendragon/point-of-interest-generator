from abc import ABC, abstractmethod


class Point_of_Interest(ABC):
    """
    This abstract class creates the basic framework for Point_of_Interest
    objects. These are places that could be used to create steps in an
    RPG quest cycle, start a whole new one, or add milieu to a world.

    The basic attribute that all points of interest have in common is:
        discoverability: str    how easily can it found

    From there, they branch off in attributes based on the type of POI
    and further subtyping in some instances.

    """
    def __init__(self, discoverability:str, debug=False):
        """
        This abstract method assigns the first two
        :param discoverability:
        :param poi_type:
        """
        self.discoverability = discoverability
        self.debug = debug


class Adventure_Site(Point_of_Interest):
    """
    This subclass generates the most basic of points of interest,
    the adventure site. It has the simplest set of attributes:
        discoverability: str    inherited
        next_action: str        what the GM should do next
    """
    def __init__(self, discoverability, next_action='create workup', debug=False):
        if debug:
            print(f"Adventure_Site: discoverability: {discoverability}. "
                  f"debug: {debug}")
        super().__init__(discoverability, debug)
        self.next_action = next_action

