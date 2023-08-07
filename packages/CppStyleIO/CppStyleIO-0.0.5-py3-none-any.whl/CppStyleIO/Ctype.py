from CppStyleIO.Exceptions import WrappingTypeError, WrappingValueError, OperateTypeError, StringCharConfusingError, \
    InvalidASCIICharError

DEFAULT_CHARSET = 'ascii'


class Variable:
    def __init__(self, T):
        self.val = 'Error'
        self.type = T

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __neg__(self):
        pass

    def __truediv__(self, other):
        pass

    def __str__(self):
        return self.val.__str__()

    def __repr__(self):
        return self.val.__str__()

    @staticmethod
    def Load(obj):
        if isinstance(obj, int):
            return INT(obj)
        elif isinstance(obj, str):
            if len(obj) == 1:
                return CHAR(obj)


def Operator(func):
    def wrapper(self, other):
        size = {
            "char": 1,
            "int": 4,
            "float": 8,
        }

        if isinstance(other, Variable):
            if size[self.type] >= size[other.type]:
                return func(self, other)
            else:
                return eval(f"Variable.Load({repr(other)})."
                            f"__r{func.__name__[2:]}(Variable.Load({repr(self)}))")
        else:
            raise OperateTypeError(other)

    return wrapper


class INT(Variable):
    def __init__(self, v: int or str or float or Variable = 0):
        super().__init__('int')
        if isinstance(v, int):
            self.val = v
        elif isinstance(v, str) and len(v) == 1:
            self.val = ord(v)
        elif isinstance(v, float):
            self.val = int(v)
        elif isinstance(v, Variable):
            self.val = v.__INT__()
        else:
            raise ValueError(f'Current Type {type(v)} can not convert to Fake Cpp Object')

    @Operator
    def __add__(self, other):
        return INT(self.val + other.val)

    @Operator
    def __radd__(self, other):
        return INT(self.val + other.val)

    @Operator
    def __sub__(self, other):
        return INT(self.val - other.val)

    @Operator
    def __rsub__(self, other):
        return INT(other.val - self.val)

    @Operator
    def __mul__(self, other):
        return INT(self.val * other.val)
    @Operator
    def __rmul__(self, other):
        return INT(self.val * other.val)

    @Operator
    def __neg__(self):
        return INT(-self.val)

    @Operator
    def __truediv__(self, other):
        return INT(self.val // other.val)

    @Operator
    def __rtruediv__(self, other):
        return INT(other.val // self.val)

    def __str__(self):
        return self.val.__str__()

    def __INT__(self):
        return self.val

    def __CHAR__(self):
        if 0 <= self.val < 128:
            return self.val
        else:
            raise InvalidASCIICharError(self.val)

    def load(self, s: str or int or float):
        if not isinstance(s, (int, str, float)):
            self.val = 'err'
            raise WrappingTypeError(self.type, s)
        try:
            self.val = int(s)
        except ValueError as e:
            self.val = 'err'
        finally:
            if self.val == 'err':
                raise WrappingValueError(self.type, s)


Long = INT


class CHAR(Variable):
    def __init__(self, ch: int or str or bytes or Variable = 0):
        super().__init__('char')
        if isinstance(ch, str):
            if len(ch) != 1:
                raise StringCharConfusingError(ch)
            try:
                self.val = ch.encode(DEFAULT_CHARSET)[0]
            except UnicodeEncodeError:
                self.val = 'Invalid'
            finally:
                if self.val == 'Invalid':
                    raise InvalidASCIICharError(ch)
        elif isinstance(ch, int):
            self.val = ch
        elif isinstance(ch, bytes):
            if len(ch) != 1:
                raise StringCharConfusingError(ch)
            if 0 <= ch[0] < 128:
                self.val = ch[0]
            else:
                raise InvalidASCIICharError(ch)
        elif isinstance(ch, Variable):
            self.val = ch.__CHAR__()

    def load(self, char):
        if not isinstance(char, (bytes, str, int)):
            raise WrappingTypeError(self.type, char)
        if isinstance(char, str):
            if len(char) != 1:
                raise StringCharConfusingError(char)
            try:
                self.val = char.encode(DEFAULT_CHARSET)[0]
            except UnicodeEncodeError:
                self.val = 'Invalid'
            finally:
                if self.val == 'Invalid':
                    raise InvalidASCIICharError(char)
        elif isinstance(char, int):
            if 0 <= char < 128:
                self.val = char
            else:
                raise WrappingValueError('char(0~127)', char)
        elif isinstance(char, bytes):
            if len(char) != 1:
                raise StringCharConfusingError(ch)
            if 0 <= char[0] < 128:
                self.val = char[0]
            else:
                raise InvalidASCIICharError(char)

    def __str__(self):
        return chr(self.val)

    def __INT__(self):
        return self.val

    def __CHAR__(self):
        return self.val

    @Operator
    def __add__(self, other):
        return INT(self.val + other.val)

    @Operator
    def __sub__(self, other):
        return INT(self.val - other.val)

    @Operator
    def __mul__(self, other):
        return INT(self.val * other.val)

    @Operator
    def __neg__(self):
        return INT(-self.val)

    @Operator
    def __truediv__(self, other):
        return INT(self.val // other.val)

    def __repr__(self):
        return self.val.__repr__()


endl = CHAR(10)
