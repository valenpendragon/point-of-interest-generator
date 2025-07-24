from abc import ABC, abstractmethod
from entities import Dice, return_die_roll
from functions import return_range, get_table_result, get_dice_info
import pandas as pd
import numpy as np


class PointOfInterest(ABC):
    """
    This abstract class creates the basic framework for PointOfInterest
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
        if debug:
            print(f"PointOfInterest.__init__: discoverability_table| "
                  f"{discoverability_table}, debug: {debug}.")
        self.discoverability_table = discoverability_table
        cols = list(self.discoverability_table.columns)
        if debug:
            print(f"PointOfInterest.__init__: table: {self.discoverability_table}")
            print(f"PointOfInterest.__init__: cols: {cols}.")
        die_info = cols[0].lower()
        if debug:
            print(f"PointOfInterest.__init__: die_info: {die_info}.")
        die_no, die_size = get_dice_info(die_info, debug=debug)
        die = Dice(dice_size=die_size, dice_number=die_no)
        roll = die.roll()
        result = get_table_result(self.discoverability_table, roll)
        if result is None:
            error_msg = (f"Table format was invalid. No result could be "
                         f"determined")
            print(f"PointOfInterest.__init__: {error_msg}")
            raise ValueError(error_msg)
        else:
            self.discoverability = result
        if debug:
            print(f"PointOfInterest.__init__: die_size: {die_size}. "
                  f"die: {die}, roll: {roll}, result{result}.")

        self.debug = debug
        
    @abstractmethod
    def __str__(self):
        """
        Each version of __str__() has to be different due to changing attributes.
        :return: str
        """
        pass
    
    @abstractmethod
    def __repr__(self):
        """
        Each version __repr__() has to be difference due to changing attributes.
        :return: str
        """
        pass

    def redo_discoverability(self):
        """
        This method uses the attribute self.discoverability_table to rerun
        the assignment of self.discoverability. All changes are internal.
        :return:
        """
        cols = self.discoverability_table.columns
        if self.debug:
            print(f"PointOfInterest.redo_discoverability: cols: {cols}.")
        die_info = cols[0].lower()
        if self.debug:
            print(f"PointOfInterest.redo_discoverability: die_info: {die_info}.")
        die_no, die_size = get_dice_info(die_info, debug=debug)
        die = Dice(dice_size=die_size, dice_number=die_no)
        roll = die.roll()
        result = get_table_result(self.discoverability_table, roll)
        if self.debug:
            print(f"PointOfInterest.redo_discoverability: die_size: "
                  f"{die_size}. die: {die}, roll: {roll}, result{result}.")
        if result is None:
            error_msg = (f"Table format was invalid. No result could be "
                         f"determined")
            print(f"PointOfInterest.redo_discoverability: {error_msg}")
            raise ValueError(error_msg)
        else:
            self.discoverability = result



class AdventureSite(PointOfInterest):
    """
    This subclass of PointOfInterest generates the simplest type of POI:
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
            print(f"AdventureSite: discoverability: {discoverability_table}. "
                  f"debug: {debug}")
        super().__init__(discoverability_table, debug=debug)
        self.next_action = next_action
        
    def __str__(self):
        output = f"discoverability: {self.discoverability}\n" \
                 f"next_action: {self.next_action}\n" \
                 f"discoverability_table: {self.discoverability_table}"
        return output
    
    def __repr__(self):
        output = (f"AdventureSite(pd.DataFrame(dict(d2= ['1-2'], "
                  f"results=[\'{self.discoverability}\']), index=None), "
                  f"next_action=\'{self.next_action}\', "
                  f"debug={self.debug})")
        return output


if __name__ == "__main__":
    print(f"main: Beginning testing")
    debug = True
    ws_name = "POI Discoverability"
    fp = "../data_orig/tables.xlsx"
    discoverability_table = pd.read_excel(fp, sheet_name=ws_name, index_col=None, na_values=True)
    adv01 = AdventureSite(discoverability_table, debug=debug)
    adv02 = AdventureSite(discoverability_table, next_action="testing", debug=debug)
    print(f"main: Printing tests:")
    print(f"main: adv01: {adv01}")
    print(f"main: adv02: {adv02}")
    print(f"main: Repr tests:")
    print(f"main: adv01: {repr(adv01)}")
    print(f"main: adv02: {repr(adv02)}")
    print(f"main: Testing redo_discoverability().")
    adv01.redo_discoverability()
    adv02.redo_discoverability()
    print(f"main: adv01: {adv01}")
    print(f"main: adv02: {adv02}")
    print(f"main: adv01: {repr(adv01)}")
    print(f"main: adv02: {repr(adv02)}")
