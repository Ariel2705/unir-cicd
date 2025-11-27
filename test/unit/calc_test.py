import unittest
from unittest.mock import patch
import pytest

from app.calc import Calculator


def mocked_validation(*args, **kwargs):
    return True


@pytest.mark.unit
class TestCalculate(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add_method_returns_correct_result(self):
        self.assertEqual(4, self.calc.add(2, 2))
        self.assertEqual(0, self.calc.add(2, -2))
        self.assertEqual(0, self.calc.add(-2, 2))
        self.assertEqual(1, self.calc.add(1, 0))

    def test_subtract_return_correct_result(self):
        self.assertEqual(4, self.calc.subtract(6, 2))
        self.assertEqual(-6, self.calc.subtract(-3, 3))
        self.assertEqual(9, self.calc.subtract(7, -2))
        self.assertEqual(6, self.calc.subtract(6, 0))

    def test_divide_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.divide(2, 2))
        self.assertEqual(1.5, self.calc.divide(3, 2))

    def test_power_method_returns_correct_result(self):
        self.assertEqual(8, self.calc.power(2, 3))
        self.assertAlmostEqual(9.261, self.calc.power(2.1, 3), places=3)

    def test_sqrt_method_returns_correct_result(self):
        self.assertEqual(3, self.calc.sqrt(9))
        self.assertAlmostEqual(1.4142135, self.calc.sqrt(2), places=6)

    def test_log10_method_returns_correct_result(self):
        self.assertEqual(1, self.calc.log10(10))
        self.assertAlmostEqual(0.3010299, self.calc.log10(2), places=6)

    def test_add_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.add, "2", 2)
        self.assertRaises(TypeError, self.calc.add, 2, "2")
        self.assertRaises(TypeError, self.calc.add, "2", "2")
        self.assertRaises(TypeError, self.calc.add, None, 2)
        self.assertRaises(TypeError, self.calc.add, 2, None)
        self.assertRaises(TypeError, self.calc.add, object(), 2)
        self.assertRaises(TypeError, self.calc.add, 2, object())

    def test_subtract_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.subtract, "2", 2)
        self.assertRaises(TypeError, self.calc.subtract, 2, "2")
        self.assertRaises(TypeError, self.calc.subtract, "2", "2")
        self.assertRaises(TypeError, self.calc.subtract, None, 2)
        self.assertRaises(TypeError, self.calc.subtract, 2, None)
        self.assertRaises(TypeError, self.calc.subtract, object(), 2)
        self.assertRaises(TypeError, self.calc.subtract, 2, object())

    def test_divide_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.divide, "2", 2)
        self.assertRaises(TypeError, self.calc.divide, 2, "2")
        self.assertRaises(TypeError, self.calc.divide, "2", "2")

    def test_power_method_fails_with_nan_parameter(self):
        self.assertRaises(TypeError, self.calc.power, "2", 2)
        self.assertRaises(TypeError, self.calc.power, 2, "2")

    def test_sqrt_method_fails_with_invalid_parameter(self):
        self.assertRaises(TypeError, self.calc.sqrt, "9")
        self.assertRaises(TypeError, self.calc.sqrt, None)
        self.assertRaises(TypeError, self.calc.sqrt, -1)

    def test_log10_method_fails_with_invalid_parameter(self):
        self.assertRaises(TypeError, self.calc.log10, "10")
        self.assertRaises(TypeError, self.calc.log10, 0)
        self.assertRaises(TypeError, self.calc.log10, -10)

    def test_divide_method_fails_with_division_by_zero(self):
        self.assertRaises(TypeError, self.calc.divide, 2, 0)
        self.assertRaises(TypeError, self.calc.divide, 2, -0)
        self.assertRaises(TypeError, self.calc.divide, 0, 0)
        self.assertRaises(TypeError, self.calc.divide, "0", 0)

    @patch('app.util.validate_permissions', side_effect=mocked_validation, create=True)
    def test_multiply_method_returns_correct_result(self, _validate_permissions):
        self.assertEqual(4, self.calc.multiply(2, 2))
        self.assertEqual(0, self.calc.multiply(1, 0))
        self.assertEqual(0, self.calc.multiply(-1, 0))
        self.assertEqual(-2, self.calc.multiply(-1, 2))

    @patch('app.util.validate_permissions', return_value=True, create=True)
    def test_multiply_method_fails_with_nan_parameter(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.multiply, "2", 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, "2")
        self.assertRaises(TypeError, self.calc.multiply, "2", "2")
        self.assertRaises(TypeError, self.calc.multiply, None, 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, None)
        self.assertRaises(TypeError, self.calc.multiply, object(), 2)
        self.assertRaises(TypeError, self.calc.multiply, 2, object())

    @patch('app.util.validate_permissions', return_value=False, create=True)
    def test_multiply_method_fails_without_permissions(self, _validate_permissions):
        self.assertRaises(TypeError, self.calc.multiply, 2, 2)

    @patch('app.util.validate_permissions', return_value=True, create=True)
    def test_multiply_method_calls_validate_permissions(self, mock_validate_permissions):
        self.calc.multiply(2, 3)
        mock_validate_permissions.assert_called_once_with("2 * 3", "user1")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
