from typing import Generic, Tuple, Type, TypeVar
from ..mutable._mutable import Mutable
from ._operators import *
from inspect import signature


T = TypeVar('T')


class Link(Mutable[T], Generic[T]):
    def __init__(self, operator: Type[Operator], *values: "Tuple[T, ...]"):
        assert issubclass(operator, Operator)
        self.operator = operator
        self.inputs = list(values)

        values_given = len(values)
        values_expected = signature(operator._eval).parameters.__len__()
        if values_given != values_expected:
            for attr in signature(operator._eval).parameters.values():
                # If an unpack operation is used, the given arguments will not exceed the expected arguments.
                if str(attr).startswith("*") and not str(attr).startswith("**"):
                    break
            else:
                raise ValueError(f"wrong number of values for {operator.__name__} (expected {values_expected}, got {values_given})")
    
    @property
    def value(self) -> T:
        inputs = (
            value.value 
            if isinstance(value, Mutable) 
            else value
            for value 
            in self.inputs
        )

        return self.operator(*inputs)
    
    @value.setter
    def value(self, value):
        # Modify the first value using the reverse operation
        try:
            value1 = self.operator.reverse(value, *self.inputs[1:])
            if value1 is not None:
                if isinstance(self.inputs[0], Mutable):
                    self.inputs[0].__set__(self, value1)
                else:
                    self.inputs[0] = value1
            else:
                raise ValueError(f"value cannot be set: {self.operator.__name__}({self.inputs[0]}, <Any>) != {value}")
        except NotImplementedError as e:
            print(e.with_traceback())
            print("cannot set value for link without reverse operation")
    
    def __repr__(self):
        return f"{self.__class__.__name__}({', '.join(map(repr, self.inputs))})"
    
    def __add__(self, other):
        return Add(self, other)
    
    def __radd__(self, other):
        return Add(other, self)
    
    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return RSub(self, other)
    
    def __mul__(self, other):
        return Mul(self, other)
    
    def __rmul__(self, other):
        return Mul(other, self)
    
    def __truediv__(self, other):
        return Div(self, other)
    
    def __rtruediv__(self, other):
        return RDiv(self, other)
    
    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return RPow(self, other)
    
    def __mod__(self, other):
        return Mod(self, other)
    
    def __rmod__(self, other):
        return Mod(other, self)

    def __abs__(self):
        return Abs(self)
    
    def __neg__(self):
        return Not(self)

    def __invert__(self):
        return Not(self)
    
    def __eq__(self, other):
        return Eq(self, other)

    def __ne__(self, other):
        return Not(Eq(self, other))
    
    def __gt__(self, other):
        return Gt(self, other)
    
    def __ge__(self, other):
        return Ge(self, other)
    
    def __lt__(self, other):
        return Lt(self, other)
    
    def __le__(self, other):
        return Le(self, other)
    
    def __and__(self, other):
        return And(self, other)
    
    def __rand__(self, other):
        return And(other, self)
    
    def __or__(self, other):
        return Or(self, other)
    
    def __ror__(self, other):
        return Or(other, self)
    
    def __xor__(self, other):
        return Xor(self, other)
    
    def __rxor__(self, other):
        return Xor(other, self)

    
    def __iadd__(self, other):
        other_value = other.value if isinstance(other, Link) else other
        self.value += other_value
        return self


class Value(Link[T]):
    def __init__(self, value: T):
        super().__init__(ValueOperator, value)

class Eq(Link[bool]):
    def __init__(self, a: Link, b: Link):
        super().__init__(EqualOperator, a, b)

class Gt(Link[bool]):
    def __init__(self, a: Link, b: Link):
        super().__init__(GreaterOperator, a, b)

class Ge(Link[bool]):
    def __init__(self, a: Link, b: Link):
        super().__init__(GreaterEqualOperator, a, b)

class Lt(Link[bool]):
    def __init__(self, a: Link, b: Link):
        super().__init__(LessOperator, a, b)

class Le(Link[bool]):
    def __init__(self, a: Link, b: Link):
        super().__init__(LessEqualOperator, a, b)


class Add(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(AdditionOperator, a, b)

class Sub(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(SubtractionOperator, a, b)

class RSub(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(BackwardsSubtractionOperator, a, b)

class Mul(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(MultiplicationOperator, a, b)

class Div(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(DivisionOperator, a, b)

class RDiv(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(BackwardsDivisionOperator, a, b)

class Pow(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(PowerOperator, a, b)

class RPow(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(BackwardsPowerOperator, a, b)

class Root(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(RootOperator, a, b)

class RRoot(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(BackwardsRootOperator, a, b)

class Mod(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(ModuloOperator, a, b)

class Abs(Link[T]):
    def __init__(self, a: "Link[T] | T"):
        super().__init__(AbsoluteOperator, a)


class And(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(AndOperator, a, b)

class Or(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(OrOperator, a, b)

class Xor(Link[T]):
    def __init__(self, a: "Link[T] | T", b: "Link[T] | T"):
        super().__init__(XorOperator, a, b)

class Not(Link[T]):
    def __init__(self, a: "Link[T] | T"):
        super().__init__(NotOperator, a)