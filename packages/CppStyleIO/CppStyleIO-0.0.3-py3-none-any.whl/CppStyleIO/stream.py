class IStream:
    def __init__(self, buffer):
        super().__init__(buffer)

    def __rshift__(self, other):
        pass

    def __lshift__(self, other):
        pass
