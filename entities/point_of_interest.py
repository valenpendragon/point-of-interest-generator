from abc import ABC, abstractmethod
from .dice import Dice
import pandas as pd
import numpy as np


class Point_of_Interest(ABC):
    """
    This abstract class creates the basic framework for Point_of_Interest
    objects. These are places that could be used to create steps in an
    RPG quest cycle, start a whole new one, or add milieu to a world.

    From there, they branch off in attributes based on the type of POI
    and further subtyping in some instances.

    This class assumes that the DataFrame meets the following criteria:
        1) It has two columns
        2) The first column is a string or an integer. The string format
            is nDm, ndm, or m, d/D are the characters 'd' or 'D'
            and n, m are integers such that n <+ m and can be converted
            to integers using int().
        3) The second column is a string of results  with column header
            'Result' (capitalization is ignored)
        4) Column 1 has no numerical gaps from the m in the one row and n
            in the next row.
        5) Column headers are: Column 1:  DNor dN, where 'D' or 'd' are the characters
            and N is an integer, and Column 2: a string
        6) The first entry in Column 1 should be 1 and the m in the last
            row must equal N in the Column Header.
    """
    def __init__(self, discoverability_table:pd.DataFrame, debug=False):
        """
        This abstract method generates the attribute discoverability
        using the method defined b
        :param discoverability_table:pd.DataFrame
        :param debug: bool, defaults to False
        """
        table = discoverability_table
        cols = list(table.columns)
        die_size = int(cols[0][1:])
        self.debug = debug


class Adventure_Site(Point_of_Interest):
    """
    This subclass of Point_of_Interest generates the simplest type of POI.
    an adventure site.
    """
    def __init__(self, discoverability_table: pd.DataFrame, next_action='create workup', debug=False):
        """
        __init__() requires only discoverability_table.
        :param discoverability_table: pd.DataFrame
        :param next_action: str, defaults to 'create workup'
        :param debug: bool, defaults to False
        """
        if debug:
            print(f"Adventure_Site: discoverability: {discoverability_table}. "
                  f"debug: {debug}")
        super().__init__(discoverability_table, debug)
        self.next_action = next_action

