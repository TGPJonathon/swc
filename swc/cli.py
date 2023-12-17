"""
This module provides a reimplementation of the classic Linux 'wc' (word count) 
command with additional functionalities. It uses the Click library to handle 
command-line interface interactions, enabling users to count bytes, lines, words, 
and characters in a given text file. The key feature of this implementation is the 
OrderedOptionsCommand class, which allows the order of command-line options to 
affect the output, mimicking the behavior of the Linux 'wc' command.

The module consists of several key functions:
- cli: The main entry point for the Click command-line interface.
- parse_file: Reads the text from the file and generates output based on the 
  provided parameters and their order.
- get_wc_values: Computes byte, line, word, and character counts for a given 
  text string.
- byte_or_char: Determines the last recognized parameter from a list of ordered 
  parameters, used to decide whether to count bytes or characters when both 
  options are specified.
- create_output: Formats the counts into a string for output based on specified 
  parameters and their order.

This module exemplifies advanced usage of the Click library to implement 
command-line utilities with behavior dependent on the order of options.

Example:
    Running the script from the command line with various options:
    $ python script.py -l -w -c file.txt
    $ python script.py -m -l file.txt

Note:
    This module requires the 'click' package to be installed.
"""

import click
import io
import sys

from click.core import Context
from typing import List, Tuple


class OrderedOptionsCommand(click.Command):
    """
    Click package doesn't offer a built-in way of finding out the order of
    parameters passed to program. The Linux WC command's output varies
    depending on the order -c and -m are passed to it.

    This class will help output the correct values
    """

    _options = []

    def parse_args(self, ctx: Context, args: List[str]) -> List[str]:
        parser = self.make_parser(ctx)
        _, _, param_order = parser.parse_args(args=list(args))
        for param in param_order:
            self._options.append(param.name)

        return super().parse_args(ctx, args)


@click.command(cls=OrderedOptionsCommand)
@click.argument("file", type=click.File("r"), default=sys.stdin)
@click.option("-c", "--count", is_flag=True, help="Count number of bytes in file")
@click.option("-l", "--lines", is_flag=True, help="Count number of lines in file")
@click.option("-w", "--words", is_flag=True, help="Count number of words in file")
@click.option("-m", "--chars", is_flag=True, help="Count number of characters in file")
@click.version_option()
def cli(file: io.TextIOWrapper, count: bool, lines: bool, words: bool, chars: bool):
    "Reimplementing the wc linux command for a challenge"
    params = (count, lines, words, chars)
    output = parse_file(file, params, OrderedOptionsCommand._options)
    click.echo(output)


def parse_file(
    file: io.TextIOWrapper,
    params: Tuple[bool, bool, bool, bool],
    ordered_params: List[str],
):
    text = file.read()
    last_param = byte_or_char(ordered_params)
    output = create_output(params, get_wc_values(text), last_param)
    output_w_filename = output + f" {file.name}"

    return output_w_filename


def get_wc_values(text: str):
    """Calculates various counts (byte, line, word, and character) for the given text.

    This function computes four different counts for a given string: the byte count
    when encoded in UTF-8, the line count, the word count, and the character count.
    The line count is determined based on the number of newline characters. The
    word count is based on the number of words separated by whitespace. The
    character count is simply the length of the text. The byte count is calculated
    by encoding the text as UTF-8 and counting the number of bytes.

    Args:
        text (str): The input text for which the counts are to be computed.

    Returns:
        tuple: A tuple containing four string elements in the following order:
            - byte_count: The number of bytes in the text when encoded in UTF-8.
            - line_count: The number of lines in the text.
            - word_count: The number of words in the text.
            - char_count: The number of characters in the text.

    Example:
        >>> get_wc_values("Hello world\nThis is a test")
        ('27', '1', '5', '23')

    """
    byte_count = str(len(text.encode("utf-8")))
    line_count = str(len(["c" for c in text if c == "\n"]))
    word_count = str(len(text.split()))
    char_count = str(len(text))

    return byte_count, line_count, word_count, char_count


def byte_or_char(ordered_params: List[str]):
    """Determines the last recognized parameter from a list of ordered parameters.

    This function iterates over a list of parameters and identifies the last
    recognized parameter, either 'count' or 'chars'. It ignores any unrecognized
    parameters. The Linux WC command's output varies depending on the order
    -c and -m are passed to it.

    Args:
        ordered_params (List[str]): A list of parameters, where each parameter
            is a string. The function recognizes 'count' and 'chars' as valid
            parameters.

    Returns:
        str: The last recognized parameter ('count' or 'chars'). If neither is
            found, returns None.

    Example:
        >>> byte_or_char(["size", "count", "volume", "chars"])
        'chars'
        >>> byte_or_char(["size", "volume", "shape"])
        None

    """
    last_param = None

    for param in ordered_params:
        if param == "count":
            last_param = "count"
        if param == "chars":
            last_param = "chars"

    return last_param


def create_output(
    params: Tuple[bool, bool, bool, bool],
    values: Tuple[int, int, int, int],
    last_param: str,
):
    """Formats the word count values into a tab-separated string for output.

    This function takes the count parameters (bytes, lines, words, characters),
    their respective values, and the last recognized parameter to format the
    output string. The function checks which parameters are set to True and
    includes their corresponding values in the output. If both 'count' and 'chars'
    are specified, it uses the value of the last parameter to determine which
    count to include. If none of the parameters are set, it defaults to showing
    line, word, and byte counts.

    Args:
        params (Tuple[bool, bool, bool, bool]): A tuple of booleans indicating
            which counts to include in the output. The order is:
            - count: Include byte count if True.
            - lines: Include line count if True.
            - words: Include word count if True.
            - chars: Include character count if True.
        values (Tuple[int, int, int, int]): A tuple containing the counts for
            bytes, lines, words, and characters, in that order.
        last_param (str): The last recognized parameter ('count' or 'chars')
            used to resolve the precedence between byte and character counts.

    Returns:
        str: A tab-separated string of the requested counts.

    Example:
        >>> create_output((True, True, False, False), (1024, 50, 200, 980), "count")
        '50\t1024'
        >>> create_output((True, False, True, True), (1024, 50, 200, 980), "chars")
        '200\t980'

    """
    count, lines, words, chars = params
    byte_count, line_count, word_count, char_count = values

    if not any([count, lines, words, chars]):
        return f"{line_count}\t{word_count}\t{byte_count}"

    output = []
    if lines:
        output.append(line_count)
    if words:
        output.append(word_count)
    if count and chars:
        output.append(byte_count if last_param == "count" else char_count)
    else:
        if count:
            output.append(byte_count)
        if chars:
            output.append(char_count)

    return "\t".join(output)
