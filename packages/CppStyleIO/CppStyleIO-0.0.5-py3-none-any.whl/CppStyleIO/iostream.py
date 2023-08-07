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
            while not self.buf:
                tmp = stdin.readline()
                if not tmp:
                    raise EOFError
                self.buf += tmp[:-1]
                
            if var.type == 'char':
                var.load(self.buf)
                self.buf = self.buf[1:]
                return
                
            self.buf = self.buf.strip()
            pp = self.buf.find(' ')
            if pp != -1:
                var.load(self.buf[p:pp])
                self.buf = self.buf[pp + 1:]
            elif self.buf:
                var.load(self.buf)
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
