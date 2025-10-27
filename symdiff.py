from abc import ABC, abstractmethod
from typing import Any

class Expression(ABC):
    
    @abstractmethod
    def differentiate(self, var: str = 'x'):
        """Return the derivative of the expression with respect to var"""
        raise NotImplementedError("Differentiate method not implemented")
    
    @abstractmethod
    def __str__(self):
        """String representation of the expression"""
        raise NotImplementedError("String representation not implemented")
    
    def simplify(self):
        """Simplify the expression"""
        return self
    
    def __add__(self, other: Any):
        """Overload + operator"""
        return Add(self, to_expression(other))
    
    def __radd__(self, other: Any):
        """Reverse + operator"""
        return Add(to_expression(other), self)
    
    def __sub__(self, other: Any):
        """Overload - operator"""
        return Add(self, Multiply(Constant(-1), to_expression(other)))
    
    def __rsub__(self, other: Any):
        """Reverse - operator"""
        return Add(to_expression(other), Multiply(Constant(-1), self))
    
    def __mul__(self, other: Any):
        """Overload * operator"""
        return Multiply(self, to_expression(other))
    
    def __rmul__(self, other: Any):
        """Reverse * operator"""
        return Multiply(to_expression(other), self)
    
    def __pow__(self, other: Any):
        """Overload ** operator"""
        return Power(self, to_expression(other))
    
    def __repr__(self):
        return f"{self.__class__.__name__}: {self.__str__()}"

class Constant(Expression):
    def __init__(self, value):
        self.value = value
    
    def differentiate(self, var: str = 'x'):
        return Constant(0)
    
    def __str__(self):
        return str(self.value)

class Variable(Expression):
    def __init__(self, name='x'):
        self.name = name
    
    def differentiate(self, var: str = 'x'):
        return Constant(1) if self.name == var else Constant(0)
    
    def __str__(self):
        return self.name

class Add(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def differentiate(self, var: str = 'x'):
        left = self.left.simplify()
        right = self.right.simplify()
        # Use sum rule of differentiation
        return Add(left.differentiate(var), right.differentiate(var))
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left, Constant) and left.value == 0:
            return right
        if isinstance(right, Constant) and right.value == 0:
            return left
        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value + right.value)
        
        return Add(left, right)
    
    def __str__(self):
        return f"({self.left} + {self.right})"

class Multiply(Expression):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def differentiate(self, var: str = 'x'):
        left = self.left.simplify()
        right = self.right.simplify()
        # Use product rule of differentiation
        return Add(
            Multiply(left.differentiate(var), right),
            Multiply(left, right.differentiate(var))
        )
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left, Constant) and left.value == 0:
            return Constant(0)
        if isinstance(right, Constant) and right.value == 0:
            return Constant(0)
        if isinstance(left, Constant) and left.value == 1:
            return right
        if isinstance(right, Constant) and right.value == 1:
            return left
        if isinstance(left, Constant) and isinstance(right, Constant):
            return Constant(left.value * right.value)
        
        return Multiply(left, right)
    
    def __str__(self):
        return f"({self.left} * {self.right})"

class Power(Expression):
    def __init__(self, base, exponent):
        self.base = base
        self.exponent = exponent
    
    def differentiate(self, var: str = 'x'):
        base = self.base.simplify()
        exponent = self.exponent.simplify()
        # Use power rule of differentiation
        return Multiply(
            Multiply(exponent, Power(base, Add(exponent, Constant(-1)))),
            base.differentiate(var)
        )
    
    def simplify(self):
        base = self.base.simplify()
        exponent = self.exponent.simplify()
        
        if isinstance(exponent, Constant) and exponent.value == 0:
            return Constant(1)
        if isinstance(exponent, Constant) and exponent.value == 1:
            return base
        if isinstance(base, Constant) and isinstance(exponent, Constant):
            return Constant(base.value ** exponent.value)
        
        return Power(base, exponent)
    
    def __str__(self):
        return f"({self.base}^{self.exponent})"

def to_expression(value: Any) -> Expression:
    """Convert a value to an Expression if it isn't already"""
    if isinstance(value, Expression):
        return value
    return Constant(value)

if __name__ == "__main__":
    print("Symbolic Differentiation System\n")
    print("-" * 60)
    
    # Create a variable
    x = Variable('x')
    
    # Example 1: f(x) = 3x^2 + 2x + 1
    print("Example Polynomial\n")
    f1 = 3 * x**2 + 2 * x + 1
    print(f"f(x) = {f1}")
    df1 = f1.differentiate()
    print(f"f'(x) [raw] = {df1}")
    print(f"f'(x) [simplified] = {df1.simplify()}")