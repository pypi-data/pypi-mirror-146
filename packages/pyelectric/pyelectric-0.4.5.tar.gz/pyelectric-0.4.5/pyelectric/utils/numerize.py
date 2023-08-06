import math
from typing import List, Union

decimal_separator = '.'
positive_suffixes: List[Union[str, List[str]]] = ['', ['k', 'K'], 'M', 'G', 'T', 'P']
negative_suffixes: List[Union[str, List[str]]] = ['m', 'u', 'n', 'p']


def ends_with_suffix(number_str: str, suffixes: Union[str, List[str]]) -> bool:
    if isinstance(suffixes, str):
        suffixes = [suffixes]
    for suffix in suffixes:
        if number_str.endswith(suffix):
            return True
    return False


def format(number: float, unit='', decimal: int = 2) -> str:
    suffixes = positive_suffixes + negative_suffixes[::-1]
    if number == 0:
        return '0'
    magnitude = int(math.floor(math.log(abs(number), 1e3)))
    if magnitude <= len(positive_suffixes) - 1 and magnitude >= -len(negative_suffixes):
        number_str = f'{number/1e3**magnitude:.{decimal}f}'
        number_str = number_str.strip('0').strip('.')
        suffix_or_suffixes = suffixes[magnitude]
        suffix = suffix_or_suffixes if isinstance(suffix_or_suffixes, str) else suffix_or_suffixes[0]
        number_str = f'{number_str}{suffix}{unit}'
    else:
        number_str = f'{number:.{decimal}e}{unit}'
    return number_str.replace('.', decimal_separator)


def revert(number_str: str, unit: str = '') -> float:
    suffixes = positive_suffixes + negative_suffixes[::-1]
    number_str = number_str.replace(decimal_separator, '.')
    number_str = number_str.replace(' ', '')
    if len(unit) > 0 and number_str.endswith(unit):
        number_str = number_str[:-len(unit)]
    for i, suffix in enumerate(suffixes):
        if ends_with_suffix(number_str, suffix):
            sorted_sufixes = negative_suffixes[::-1] + positive_suffixes
            magnitude = sorted_sufixes.index(suffix) - len(negative_suffixes)
            if magnitude != 0:
                return float(number_str[:-len(suffix)]) * 1e3**magnitude
    return float(number_str)
