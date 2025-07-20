from functions import return_range
import pandas as pd


def get_table_result(table: pd.DataFrame, roll: int, result_col_header='Results',
                     debug=False):
    """
    This function takes the roll integer, finds the value in the dXX columns
    that contains that value (or is in the range of values) and returns the
    corresponding result text.
    This function optionally needs the name of the results column if it is not
    'Results', which is the default value.
    The table requires a worksheet in the following format:
        1) There must be at least 2 columns.
        2) The first column must be rolls outcomes. The format for this column
            is that the header must be in the form 'nDm', 'ndm', 'Dm', or 'dm;
            where d/D is the character 'd' or 'D' and n and m are integers.
            The content of this column must in the form 'r-s', 'r', or '-', where
            '-' is the dash character and r and s are integers such that r<=s.
            The dash means that the result will be ignored. All entries with
            must ascend going down the column without a gap.
        3) One of the remaining columns must be named 'Results' or its header
            specified as a argument.
        4) All other columns will be ignored.
    :param table: pandas Dataframe
    :param roll: int
    :param result_col_header: str, defaults to 'Results'
    :return: str, if successful, or NoneType if not
    """
    if debug:
        print(f"get_table_result: result_col_header; {result_col_header}, "
              f"roll: {roll}.")
        print(f"get_table_result: table: {table}.")
    col_names = list(table.columns)
    roll_col_name = col_names[0]
    roll_col = table[roll_col_name]
    if len(col_names) == 2:
        result_col_name = col_names[1]
    elif len(col_names) < 2:
        print(f"get_table_result: table has incorrect format. Retuning None.")
        return None
    else:
        try:
            result_col = table[result_col_header]
        except KeyError:
            print(f"get_table_result: table has incorrect format. Retuning None.")
            return None
    if debug:
        print(f"get_table_result: roll_col_name: {roll_col_name}, "
              f"roll_col: {roll_col}.")
        print(f"get_table_result: result_col_name: {result_col}, "
              f"result_col: {result_col}")
    roll_idx = None

    # Sometimes, there is a error converting a '1' string at the top of the table.
    # Instead of a '1' or 1, it becomes NoneType or NaN. This has to handled here.
    ctr = 0
    for idx, item in roll_col.items():
        print(f"get_table_result: item: {item}, idx: {idx}.")
        if ctr == 0 and item is None:
            m, n = (1, 1)
        else:
            m, n = return_range(item)
        print(f"get_table_result: m: {m}, n: {n}.")
        if m <= roll <= n:
            roll_idx = idx
            break

    if roll_idx is None:
        print(f"get_table_result: The table provided in invalid. No result "
              f"could be returned.")
        result = None
    else:
        result = result_col.loc[roll_idx]

    if result == "-":
        result = "nothing"
    print(f"get_table_result: result: {result}.")
    return result


def get_dice_info(s, debug=False):
    """
    This function requires a string in the following format:
        1) ndm or nDm, where n and m are integers and d/D are those characters
        2) dm or Dm, where m is an integer and d/D are those characters
    For case 1), it will return (n, m). For case 2), it will return (1, m).
    Otherwise, it will raise a ValueError.
    :param s: str
    :param debug: bool, controls print output of debug messages
    :return: tuple of int, (n, m)  or (1, m)
    """
    error_msg = (f"Format of the string, {s}, is invalid.\n"
                 f"Correct format is 'ndm' or 'dm, where n and m are integers "
                 f"and d is case-insensitive character d.")
    die_info = s.lower()
    if debug:
        print(f"get_dice_info: die_info: {die_info}.")
    if 'd' not in die_info:
        raise ValueError(error_msg)

    l = die_info.split('d')
    if debug:
        print(f"get_dice_info: l {l}.")
    if l[0] == "":
        # There is no first integer.
        n = 1
    else:
        try:
            n = int(l[0])
        except ValueError:
            raise ValueError(error_msg)
    if debug:
        print(f"get_dice_info: n {n}.")
    try:
        m = int(l[1])
    except ValueError:
        raise ValueError(error_msg)
    if debug:
        print(f"get_dice_info: m {m}.")

    return (n, m)


if __name__ == "__main__":
    l = ['2d10', 'D20', 'd12', '3D8']
    for s in l:
        print(f"main: Testing {s}.")
        no_of_dice, die_size = get_dice_info(s, debug=True)
        print(f"main: no_of_dice: {no_of_dice}, die_size: {die_size}.")
    print(f"main: End of testing get_dice_info() function.")