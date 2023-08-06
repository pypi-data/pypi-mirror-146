from sys import stdin, stdout
from warnings import warn

from CppStyleIO.Ctype import Variable


class IStream:
    '''
    Fake istream class from cpp
    use stdin.read to fill buffer
    load fake cpp object from string(butter)
    Can Not Input Python Vars
    '''
    def __init__(self):
        self.buf = ''

        def Read(var):
            if var.type == 'char':
                var.load(self.buf)
                self.buf = self.buf[1:]
            p = 0
            while not self.buf:
                self.buf += stdin.readline()
                if not self.buf:
                    raise EOFError
                if self.buf == '\n':
                    self.buf = ''
            while self.buf[p] == ' ':
                p += 1
            if ' ' in self.buf:
                pp = self.buf.index(' ', p)
                var.load(self.buf[p:pp])
                self.buf = self.buf[pp + 1:]
            elif self.buf:
                var.load(self.buf[p:])
                self.buf = ''

        self.R = Read

    def __rshift__(self, other):
        if isinstance(other, Variable):
            self.R(other)
            return self
        else:
            raise TypeError('Can Not Input Python Vars')

    def __repr__(self):
        return ''


class OStream:
    def __init__(self):
        def Write(var):
            stdout.write(f'{var}')
            stdout.flush()

        self.W = Write

    def __lshift__(self, other):
        self.W(other)
        return self

    def __repr__(self):
        return ''


pin = IStream()
pout = OStream()
