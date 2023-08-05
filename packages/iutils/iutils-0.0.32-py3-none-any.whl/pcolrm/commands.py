import fileinput


def get_column_markers(line, delimiter):
    column_marker = []

    skip_delimiter = False
    skip_non_delimiter = False
    for idx, val in enumerate(line):
        if not skip_delimiter and not skip_non_delimiter:
            column_marker.append(idx)
            if val == delimiter:
                skip_delimiter = True
            else:
                skip_non_delimiter = True
            continue

        if val == delimiter:
            if skip_delimiter and not skip_non_delimiter:
                continue
            if not skip_delimiter and skip_non_delimiter:
                skip_delimiter = True
                skip_non_delimiter = False
                continue
        else:
            if skip_delimiter and not skip_non_delimiter:
                column_marker.append(idx)
                skip_delimiter = False
                skip_non_delimiter = True
                continue
            if not skip_delimiter and skip_non_delimiter:
                continue

    if column_marker[0] != 0:
        column_marker.insert(0, 0)

    return column_marker


def print_lines(delimiter, rm_columns):
    """Read from STDIN, remove specified columns and output to STDOUT.

    rm_columns: a sorted list of unique numbers that denotes the columns to be
                removed.
    """
    column_marker = []

    for line in fileinput.input():
        # scan the first line and get the column markers
        if not column_marker:
            column_marker = get_column_markers(line, delimiter)

            # from the rm_columns, remove values
            #   * that are less than or equal to 0
            #   * that are greater than the number of columns
            for idx, val in enumerate(rm_columns):
                if val <= 0:
                    del rm_columns[idx]
                    continue
                if val > len(column_marker):
                    del rm_columns[idx]
                    continue

        new_line = ""

        # For each column of the line, check the rm_columns list to see if it
        # needs to be removed. If it does, do nothing. If it doesn't,
        # concatenate it in a new string.
        for col in range(len(column_marker)):
            if col + 1 not in rm_columns:
                if col + 1 < len(column_marker):
                    new_line += line[column_marker[col] : column_marker[col + 1]]
                else:
                    new_line += line[column_marker[col] :]

        print(new_line.rstrip())
