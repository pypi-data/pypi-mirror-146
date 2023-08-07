class WrappingValueError(ValueError):
    def __init__(self, wrappingType, string):
        super().__init__(f"\nCan not wrap {repr(string)} to \'{wrappingType}\':\n"
                         f"This Exception might be caused by wrong format char\n"
                         f" when using pscanf to input a variable.\n")


class WrappingTypeError(TypeError):
    def __init__(self, wrappingType, obj):
        super().__init__(f"\nCan not wrap {type(obj)} to \'{wrappingType}\':\n"
                         f"This Exception might be caused by directly use \n"
                         f"the Variable.load to load a fake cpp variable\n")


class StringCharConfusingError(TypeError):
    def __init__(self, string):
        super().__init__(f'\nCan not use {string} as char:\n'
                         f"string length must be 1\n")


class InvalidASCIICharError(ValueError):
    def __init__(self, string):
        super().__init__(f"\nCan not decode {string} as char:\n"
                         f"CHAR object can only contains ascii characters, try 'UCHAR' or 'CodedCHAR' instead.\n")


class OperateTypeError(TypeError):
    def __init__(self, obj2):
        super().__init__(f"\nFake Cpp Variable can not operate with {type(obj2)}, which is a default Python Object\n"
                         f"try 'Variable.Load(var)' instead of barely 'var'"
                         )


class IncorrectParamError(TypeError):
    def __init__(self, ParamName, ParamPos, ParamType, RealType):
        super().__init__(f"\nParam {ParamName} (at pos {ParamPos}) should be {ParamType} or its subclass, not {RealType}\n"
                         f"If you're using default Python objects, try Variable.Load(obj) instead."
                         )
