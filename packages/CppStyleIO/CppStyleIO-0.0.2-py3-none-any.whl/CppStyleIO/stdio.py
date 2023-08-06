from sys import stdin as wrapped_stdin, stdout
from warnings import warn
from _io import TextIOWrapper

from CppStyleIO.Ctype import CHAR
from CppStyleIO.Exceptions import IncorrectParamError
from CppStyleIO.PycharmFakeStdinFix import StdinStream

stdin = wrapped_stdin
if not isinstance(stdin, TextIOWrapper):

    stdin = StdinStream(stdin)


def _get_string_from_stream(stream, split=('\n', ' ')):
    buf = []
    read = stream.read(1)
    while read in split:
        read = stream.read(1)
    if not read:
        return '', read
    while read not in split:
        buf.append(read)
        read = stream.read(1)
    string = ''.join(buf)
    buf.clear()
    return string, read


def pscanf(format_string, *variables):
    """
    usage: pscanf(format_string, ...)
    :param format_string: typical C format string, Only format char accepted
    :param ...: unlimited amount of Varibles, No '&' Required!
    :return: Number of successfully read variables
    samples:
    >>> a = INT()
    >>> pscanf("%d",a) # 'a' instead of '&a'
    15
    >>> a
    15
    """
    p_format = 0
    p_input = 0

    cnt = 0

    fmt = format_string.split('%')
    N1 = len(fmt)
    N2 = len(variables)
    split = '\n '
    _ = ''
    while p_format < N1 and p_input < N2:
        ch = fmt[p_format]
        p_format += 1
        if len(ch) == 1:
            if ch == 'c':
                if _:
                    variables[p_input].load(_)
                    _ = ''
                else:
                    variables[p_input].load(stdin.read(1))
                p_input += 1
                cnt += 1
            else:
                string, _ = _get_string_from_stream(stdin, split)
                if ch in 'dfsox':
                    variables[p_input].load(string)
                    p_input += 1
                    cnt += 1
        elif ch:
            if ch[0] == 'c':
                variables[p_input].load(stdin.read(1))
                p_input += 1
                cnt += 1
            else:
                string, _ = _get_string_from_stream(stdin, split + ch[1:])
                if ch[0] in 'dfsox':
                    variables[p_input].load(string)
                    p_input += 1
                    cnt += 1
            warn('Fixed Formal Char Not Recommended')
            chs = _
            chs += stdin.read(len(ch) - 2)
            if ch[1:] != chs:
                return cnt
    return cnt


def pprintf(format_string, *variables):
    """
    usage: pprintf(format_string, ...)
    :param format_string: typical C format string
    :param ...: unlimited amount of Varibles
    :return: numbers of successfully output variables
    samples:
    >>> a = INT(15)
    >>> pprintf("%d",a)
    15
    >>> pprintf("%d%d",a)
    1515
    >>> pprintf('1%d6\\n',a)
    1156

    p.s.:
    work same as print(format_string % variables)
    """
    stdout.write(format_string % tuple(var.val for var in variables))
    stdout.flush()


def getc():
    return CHAR(stdin.read(1))


def putc(ch):
    if isinstance(ch, CHAR):
        stdout.write(ch.__str__())
    else:
        raise IncorrectParamError('ch', 0, 'CHAR', type(ch))
