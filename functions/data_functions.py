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

