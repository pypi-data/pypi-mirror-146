from ..commands import print_lines
import click
import sys


def validate_col_nums(ctx, param, value):
    """Validate the col_nums argument and return a sorted list of unique numbers.

    A valid number should be able to be converted into an integer. A valid number
    range should not contain multiple dashes or non integers, and for now it
    should contain less than 1000 integers.
    """
    nums = []
    for val in value.split(","):
        if "-" in val:
            try:
                start, end = val.split("-")
            except ValueError:
                raise click.BadParameter(f"`{val}' is not a valid number range!")

            try:
                start = int(start)
                end = int(end)
            except ValueError:
                raise click.BadParameter(f"`{val}' is not a number range!")

            if len(range(start, end + 1)) > 1000:
                raise click.BadParameter(
                    f"The range `{val}' is too large! It should be no greater than 1 thousand."
                )

            # Here we add one to the end because the list the range() function generates
            # doesn't include the "end" number. However for this program's purpose it
            # should be included.
            nums += list(range(start, end + 1))
        else:
            try:
                num = int(val)
            except ValueError:
                raise click.BadParameter(f"`{val}' is not a number!")
            if num not in nums:
                nums.append(num)

    return sorted(list(set(nums)))


@click.command()
@click.option("--delimiter", "-d", default=" ", show_default=True, help="Delimiter.")
@click.argument("col_nums", callback=validate_col_nums)
def main(col_nums, *args, **kwargs):
    """Remove columns from a file.

    This utility mimics what colrm does. One of the differences is that columns
    are separated by delimiters instead of each single character representing one
    column.

    Like colrm, this utility reads its input from the standard input and writes
    its output to the standard output.

    COL_NUMS is a list of comma separated column numbers that are to be removed.
    You can use '-' to specify a range. For example, 1,2,4 or 1-2,4 etc.

    Column numbering starts with one, not zero.
    """
    # Remove all arguments from sys.argv before calling print_lines. This is
    # because Click doesn't remove processed arguments and the fileinput module
    # reads from sys.argv for file names.
    sys.argv = [sys.argv[0]]
    print_lines(delimiter=kwargs["delimiter"], rm_columns=col_nums)
