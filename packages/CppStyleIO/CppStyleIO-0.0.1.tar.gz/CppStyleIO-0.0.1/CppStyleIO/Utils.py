from CppStyleIO.Ctype import Variable


class Block:
    def __init__(self, glo=None, **kwargs):
        self.glo = glo
        self.kw = kwargs

    def __enter__(self):
        if self.glo:
            for k, v in self.kw.items():
                self.glo[k] = Variable.Load(v)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False if exc_type else None
