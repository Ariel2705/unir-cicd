import app
import math


class Calculator:
    def add(self, x, y):
        self.check_types(x, y)
        return x + y

    def subtract(self, x, y):
        self.check_types(x, y)
        return x - y

    def multiply(self, x, y):
        if not app.util.validate_permissions(f"{x} * {y}", "user1"):
            raise TypeError("User has no permissions")

        self.check_types(x, y)
        return x * y

    def divide(self, x, y):
        self.check_types(x, y)
        if y == 0:
            raise TypeError("Division by zero is not possible")

        return x / y

    def power(self, x, y):
        self.check_types(x, y)
        return x ** y

    def sqrt(self, x):
        self.check_single_type(x)
        if x < 0:
            raise TypeError("Square root of negative number is not possible")
        return math.sqrt(x)

    def log10(self, x):
        self.check_single_type(x)
        if x <= 0:
            raise TypeError("Logarithm base 10 requires a positive number")
        return math.log10(x)

    def check_types(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Parameters must be numbers")

    def check_single_type(self, x):
        if not isinstance(x, (int, float)):
            raise TypeError("Parameter must be a number")


if __name__ == "__main__":  # pragma: no cover
    calc = Calculator()
    result = calc.add(2, 2)
    print(result)
