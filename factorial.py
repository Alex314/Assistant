from math import factorial as f
import sys


def factorial(n):
    """
    Calculate n!

    :param n: int, argument to factorial
    :return: string with roughly answer
    """
    string_f = str(f(n))
    ans = str(n) + '!=' + (string_f[:20] + '...' if len(string_f) > 20 else string_f)
    return ans


if __name__ == '__main__':
    i = 100
    arg = sys.argv
    if len(arg) == 2 and arg[1].isnumeric():
        i = int(arg[1])
    string = factorial(i)
    print(string)
